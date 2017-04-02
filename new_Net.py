# coding=utf-8

import time
import random
import socket
import hashlib
import logging
import threading

from collections import deque

DEFAULT_IP = None
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
    s = None
    event = deque([])

    def __init__(self, debug=False):
        super(Server, self).__init__()
        self.debug = debug
        self.startServerStar()

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
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((HOST, PORT))
                self.s.listen(1)
                self.conn, self.addr = self.s.accept()
            except OSError as e:
                print(e)

    def send(self, arg):
        pass

    def recv(self):
        pass


class Client(object):
    """docstring for Client."""
    __author__ = 'miswanting'
    __version__ = '0.1.0-beta'
    isRunning = {}
    HOST = DEFAULT_IP
    PORT = DEFAULT_PORT

    def __init__(self, debug=False):
        super(Client, self).__init__()
        self.debug = debug
        self.startClientStar()

    def startClientStar(self):
        def clientStar():
            self.isRunning['self'] = True
            while self.isRunning['self']:
                try:
                    e = self.event.popleft()
                    if e['request'] == 'connect':
                        self.startClient()
                    elif e['request'] == 'exit':
                        self.isRunning['client'] = False
                        self.isRunning['self'] = False
                except IndexError as e:
                    pass
                time.sleep(0.1)
        self.t_client = threading.Thread(target=clientStar)
        self.t_client.start()

    def startClient(self):
        self.isRunning['client'] = True
        while self.isRunning['client']:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((HOST, PORT))
            except OSError as e:
                print(e)

    def send(self, arg):
        pass

    def recv(self):
        pass


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


class Protocol(object):
    """docstring for Protocol."""

    def __init__(self, debug=False):
        super(Protocol, self).__init__()
        self.debug = debug

if __name__ == '__main__':
    a = Server(True)
    a.startServerStar
