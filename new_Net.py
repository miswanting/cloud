# coding=utf-8

import json
import time
import random
import socket
import hashlib
import logging
import threading

from collections import deque

DEFAULT_IP = 'localhost'
DEFAULT_PORT = 8765


def getHash():
    m = hashlib.md5()
    m.update(str(time.time()).encode("utf-8"))
    m.update(str(random.random()).encode("utf-8"))
    return m.hexdigest()


class Server(object):
    """docstring for Server."""
    __author__ = 'miswanting'
    __version__ = '0.1.0-beta'
    isRunning = {}
    HOST = DEFAULT_IP
    PORT = DEFAULT_PORT
    event = deque([])
    passiveSubs = {}

    def __init__(self, debug=False, api=None):
        super(Server, self).__init__()
        self.debug = debug
        self.api = api
        self.startServerStar()

    def addEvent(self, event):
        tmp = {}
        tmp['request'] = event
        self.event.append(tmp)

    def startServerStar(self):
        def serverStar():
            self.isRunning['self'] = True
            while self.isRunning['self']:
                try:
                    e = self.event.popleft()
                    if e['request'] == 'start':
                        self.startServer()
                    elif e['request'] == 'exit':
                        self.isRunning['server'] = False
                        self.isRunning['self'] = False
                except IndexError as e:
                    pass
                time.sleep(0.1)
        self.t_server = threading.Thread(target=serverStar)
        self.t_server.start()

    def startServer(self):
        self.isRunning['server'] = True
        while self.isRunning['server']:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.HOST, self.PORT))
                self.s.listen(1)
                print('server')
                conn, addr = self.s.accept()
                print('server OK')
                newDict = {
                    'conn': conn,
                    'addr': addr
                }
                h = getHash()
                self.passiveSubs[h] = newDict
                if not self.api == None:
                    self.api(h)
                t_tmp = threading.Thread(name=h, target=self.subServer)
                t_tmp.start()

            except OSError as e:
                print(e)

    def subServer(self):
        print(threading.current_thread().name)
        api = {
            'request': 'reg'
        }
        self.api(api)

    def send_json(self, h, data):
        self.send_str(h, json.dumps(data))

    def recv_json(self, h):
        return json.loads(self.recv_str(h))

    def send_str(self, h, data):
        self.send(h, data.encode("utf-8"))

    def recv_str(self, h):
        return self.recv(h).decode("utf-8")

    def send(self, h, data):
        if h in self.passiveSubs.keys():
            self.passiveSubs[h]['conn'].send(data)

    def recv(self, h):
        if h in self.passiveSubs.keys():
            return self.passiveSubs[h]['conn'].recv(4096)


class Client(object):
    """docstring for Client."""
    __author__ = 'miswanting'
    __version__ = '0.1.0-beta'
    isRunning = {}
    HOST = DEFAULT_IP
    PORT = DEFAULT_PORT
    s = None
    event = deque([])

    def __init__(self, debug=False, api=None):
        super(Client, self).__init__()
        self.debug = debug
        self.api = api
        self.startClientStar()

    def addEvent(self, event):
        tmp = {}
        tmp['request'] = event
        self.event.append(tmp)

    def startClientStar(self):
        def clientStar():
            self.isRunning['self'] = True
            while self.isRunning['self']:
                try:
                    e = self.event.popleft()
                    if e['request'] == 'connect':
                        self.connect()
                    elif e['request'] == 'exit':
                        self.isRunning['client'] = False
                        self.isRunning['self'] = False
                except IndexError as e:
                    pass
                time.sleep(0.1)
        self.t_client = threading.Thread(target=clientStar)
        self.t_client.start()

    def connect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('client')
            self.s.connect((self.HOST, self.PORT))
            print('client OK')
            print(self.recv_str())

        except OSError as e:
            print(e)

    def send_json(self, data):
        self.send_str(json.dumps(data))

    def recv_json(self):
        return json.loads(self.recv_str())

    def send_str(self,  data):
        self.send(data.encode("utf-8"))

    def recv_str(self):
        return self.recv().decode("utf-8")

    def send(self, data):
        self.s.send(data)

    def recv(self):
        return self.s.recv(4096)


class Cloud(object):
    """docstring for Cloud."""
    __author__ = 'miswanting'
    __version__ = '0.1.0-beta'

    isRunning = {}

    # 代表自己的节点
    node = {}

    # 云的本地副本
    cloud = {}

    # 状态机
    status = {
        'last': '',
        'rand': ''
    }

    # 延迟列表
    pingDict = {}

    # 消息队列
    event = {}

    socket = {}

    star = {}

    passiveStar = {}

    def __init__(self, debug=False):
        super(Cloud, self).__init__()
        self.debug = debug
        self.isRunning['self'] = True
        self.isRunning['last'] = False
        self.isRunning['rand'] = False
        self.isRunning['serv'] = False

        # 消息队列
        self.event['last'] = deque([])
        self.event['rand'] = deque([])
        self.event['serv'] = deque([])

        # 生成自身Hash
        self.node['hash'] = getHash()
        self.node['last'] = ''
        self.node['rand'] = ''
        self.node['next'] = ''

        # 套接字
        self.socket['last'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket['rand'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket['next'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置Logging
        logging.basicConfig(filename='Cloud.log', level=logging.DEBUG, filemode='w',
                            format='%(relativeCreated)d[%(levelname).4s][%(threadName)-.4s]%(message)s')
        self.log = logging.getLogger(self.node['hash'][:4])
        self.log.setLevel(logging.DEBUG)
        handler = logging.FileHandler(self.node['hash'][:4] + '.log', 'w')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(relativeCreated)d[%(levelname).4s][%(threadName)-.4s]%(message)s')
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.info('Hash: {}'.format(self.node['hash']))

        self.star['self'] = None
        self.star['last'] = None
        self.star['rand'] = None
        self.star['serv'] = None
        self.star['input'] = None

        self.last = Client(api=self.api)
        self.rand = Client(api=self.api)
        self.server = Server(api=self.api)

        self.server.addEvent('start')

    def api(self, arg):
        print(arg)


class Protocol(object):
    """docstring for Protocol."""

    def __init__(self, debug=False):
        super(Protocol, self).__init__()
        self.debug = debug

if __name__ == '__main__':
    def api(arg):
        print(arg)
    a = Server(True, api=api)
    a.addEvent('start')
    time.sleep(1)
    b = Client(True, api=api)
    b.addEvent('connect')
    time.sleep(1)
    b.send_str('123')
