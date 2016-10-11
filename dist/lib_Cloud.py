# coding=utf-8
import time
import socket
import threading
import json
import hashlib
import os
import random

class Cloud():
    """
    Advanced Cloud Module with Multi-threading.
    """

    def doCloud(self, conn, data):
        pass

    def __init__(self):
        self.isRunning = True
        self.name = '###'
        self.version = '1.0.0'
        self.title = ''
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.info = {}
        self.info['debug'] = False
        # self.info[''] = 'offline'
        self.info['currentChannel'] = []
        self.info['serverThread'] = None
        self.info['connectThread'] = {}
        self.info['clientThread'] = None
        self.info['scannerThread'] = None
        self.info['deleteList'] = []
        self.info['serverTaskList'] = []
        self.info['clientTaskList'] = []
        self.info['scannerTaskList'] = []
        self.info['newsList'] = []
        self.serverConnectionList = {}
        self.cloudStructure = {}
        self.cloudStructure['nodeList'] = {}
        self.hash = self.getHash()

    def startCloud(self, myPort):
        def Star():
            interval = 1
            while self.isRunning:
                if self.info['debug']:
                    self.title = '%s|本机:%s|云端:%s|连接:%s' % (self.hash, self.info['myAddress'][
                                                           0] + ':' + str(self.info['myAddress'][1]), '', len(self.info['connectThread'].keys()))
                    os.system('title "%s"' % self.title)
                if len(self.info['deleteList']) > 0:
                    del self.info['connectThread'][self.info['deleteList'][0]]
                    del self.info['deleteList'][0]
                    interval = interval / 2
                else:
                    interval = 1
                if len(self.info['deleteList']) > 200:
                    for each in self.info['deleteList']:
                        del each
                elif len(self.info['deleteList']) > 100:
                    del self.info['newsList'][0]
                time.sleep(interval)

        def userInput():
            while self.isRunning:
                if self.info['debug']:
                    cmd = input()
                    if cmd == 'exit':
                        print('正在关闭……')
                        self.isRunning = False
                        self.server.close()
                        self.client.close()
                        self.scanner.close()

        def startServer():
            def startConnect():
                handShakeInfo = self.recvJson(conn)
                # json.loads(self.info['connectThread'][threading.current_thread().name]['conn'].recv(4096).decode("utf-8"))
                print('\033[0;37;40m%s from %s' %
                      (handShakeInfo['request'], handShakeInfo['hash']))
                if handShakeInfo['request'] == 'login':
                    self.shakeHand(conn, 'nodeList')
                    newNode = {}
                    newNode['name'] = handShakeInfo['name']
                    newNode['version'] = handShakeInfo['version']
                    newNode['address'] = tuple(handShakeInfo['address'])
                    newNode['hash'] = handShakeInfo['hash']
                    self.sendNews(self.news('newNodeLogin', newNode))
                    newNode['status'] = 'tested'
                    self.cloudStructure['nodeList'][
                        handShakeInfo['hash']] = newNode
                elif handShakeInfo['request'] == 'test':
                    self.shakeHand(conn, 'test')
                elif handShakeInfo['request'] == 'connect':
                    self.shakeHand(conn, 'connect')
                    while self.isRunning:
                        try:
                            data = self.recvJson(conn)
                            if data['request'] == 'exit':
                                break
                            else:
                                self.info['currentChannel'].append(())
                                self.doCloud(self.client, data)
                            self.sendJson(conn, True)
                        except OSError as e:
                            if e.errno == 10053:
                                break
                elif handShakeInfo['request'] == 'sendNews':
                    self.sendJson(conn, True)
                    news = self.recvJson(conn)
                    if news['hash'] in self.info['newsList']:
                        pass
                    elif news['request'] == 'newNodeLogin':
                        node = news['data']
                        print(news['request'], node['hash'])
                        newNode = {}
                        newNode['name'] = node['name']
                        newNode['version'] = node['version']
                        newNode['address'] = tuple(node['address'])
                        newNode['hash'] = node['hash']
                        self.sendNews(news)
                        newNode['status'] = 'unknown'
                        self.cloudStructure['nodeList'][node['hash']] = newNode
                    self.info['newsList'].append(news['hash'])
                else:
                    pass
                self.info['deleteList'].append(threading.current_thread().name)
            self.scan()
            self.server.bind(self.info['myAddress'])
            self.server.listen(1)
            while self.isRunning:
                conn, address = self.server.accept()
                newThread = {}
                newThread['conn'] = conn
                newThread['address'] = address
                newThread['hash'] = self.getHash()
                newThread['thread'] = threading.Thread(
                    name=newThread['hash'], target=startConnect)
                self.info['connectThread'][newThread['hash']] = newThread
                self.info['connectThread'][newThread['hash']]['thread'].start()
        self.info['myAddress'] = (self.getMyIP(), myPort)
        self.info['starThread'] = threading.Thread(name='star', target=Star)
        self.info['starThread'].start()
        if self.info['debug']:
            self.info['inputThread'] = threading.Thread(
                name='input', target=userInput)
            self.info['inputThread'].start()
        self.info['serverThread'] = threading.Thread(
            name='server', target=startServer)
        self.info['serverThread'].start()

    def connect(self, ip, port):
        def startClient():
            time.clock()
            self.client.connect((ip, port))
            ping = time.clock()
            self.shakeHand(self.client, 'login')
            handShakeInfo = json.loads(self.client.recv(4096).decode("utf-8"))
            self.cloudStructure['nodeList'] = handShakeInfo['nodeList']
            if not self.cloudStructure['nodeList'] == {}:
                for each in self.cloudStructure['nodeList']:
                    self.cloudStructure['nodeList'][each]['address'] = tuple(
                        self.cloudStructure['nodeList'][each]['address'])
                    self.cloudStructure['nodeList'][each]['status'] = 'unknown'
            newNode = {}
            newNode['name'] = handShakeInfo['name']
            newNode['version'] = handShakeInfo['version']
            newNode['address'] = (ip, port)
            newNode['status'] = 'tested'
            newNode['ping'] = ping
            newNode['hash'] = handShakeInfo['hash']
            self.cloudStructure['nodeList'][handShakeInfo['hash']] = newNode
            self.client.close()
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((ip, port))
            self.shakeHand(self.client, 'connect')
            handShakeInfo = self.recvJson(self.client)
            while self.isRunning:
                try:
                    data = self.recvJson(self.client)
                    if data['request'] == 'exit':
                        break
                    else:
                        self.doCloud(self.client, data)
                    self.sendJson(self.client, True)
                except OSError as e:
                    print(e.errno)
                    if e.errno == 10053:
                        break
        self.info['clientThread'] = threading.Thread(
            name='client', target=startClient)
        self.info['clientThread'].start()

    def scan(self):
        def startScan():
            while self.isRunning:
                if len(self.info['scannerTaskList']) > 0:
                    if self.info['scannerTaskList'][0]['request'] == 'sendNews':
                        data = self.info['scannerTaskList'][0]['data']
                        self.scanner = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
                        self.scanner.connect(data[0]['address'])
                        self.shakeHand(self.scanner, 'sendNews')
                        if self.recvJson(self.scanner):
                            self.sendJson(self.scanner, data[1])
                    del self.info['scannerTaskList'][0]
                else:
                    if len(self.cloudStructure['nodeList']) > 0:
                        for each in list(self.cloudStructure['nodeList'].keys()):
                            if self.isRunning:
                                if self.cloudStructure['nodeList'][each]['status'] == 'unknown':
                                    self.scanner = socket.socket(
                                        socket.AF_INET, socket.SOCK_STREAM)
                                    time.clock()
                                    self.scanner.connect(self.cloudStructure[
                                                         'nodeList'][each]['address'])
                                    ping = time.clock()
                                    self.cloudStructure['nodeList'][
                                        each]['ping'] = ping
                                    self.shakeHand(self.scanner, 'test')
                                    self.scanner.close()
                                    self.cloudStructure['nodeList'][
                                        each]['status'] = 'tested'
                                else:
                                    self.scanner = socket.socket(
                                        socket.AF_INET, socket.SOCK_STREAM)
                                    try:
                                        time.clock()
                                        self.scanner.connect(self.cloudStructure[
                                                             'nodeList'][each]['address'])
                                        ping = time.clock()
                                        self.cloudStructure['nodeList'][
                                            each]['ping'] = ping
                                        self.shakeHand(self.scanner, 'test')
                                    except OSError as e:
                                        if e.errno == 10061:
                                            del self.cloudStructure[
                                                'nodeList'][each]
                                    self.scanner.close()
                                    time.sleep(2)
                    time.sleep(1)
        self.info['scannerThread'] = threading.Thread(
            name='scanner', target=startScan)
        self.info['scannerThread'].start()

    def shakeHand(self, conn, request):
        newHandShakeInfo = {}
        if request == 'login':
            newHandShakeInfo['name'] = self.name
            newHandShakeInfo['version'] = self.version
            newHandShakeInfo['address'] = self.info['myAddress']
        elif request == 'nodeList':
            newHandShakeInfo['name'] = self.name
            newHandShakeInfo['version'] = self.version
            newHandShakeInfo['nodeList'] = self.cloudStructure['nodeList']
        newHandShakeInfo['hash'] = self.hash
        newHandShakeInfo['request'] = request
        self.sendJson(conn, newHandShakeInfo)

    def getMyIP(self):
        return socket.gethostbyname(socket.gethostname())

    def addTask(self, request, data):
        newTask = {}
        newTask['type'] = 'task'
        newTask['request'] = request
        newTask['hash'] = self.getHash()
        newTask['data'] = data
        self.info['scannerTaskList'].append(newTask)

    def news(self, request, data):
        newNews = {}
        newNews['type'] = 'news'
        newNews['request'] = request
        newNews['hash'] = self.getHash()
        newNews['data'] = data
        newNews['from'] = self.hash
        return newNews

    def sendNews(self, news):
        for each in self.cloudStructure['nodeList'].keys():
            data = (self.cloudStructure['nodeList'][each], news)
            self.addTask('sendNews', data)

    def recvJson(self, conn):
        return json.loads(self.recvMsg(conn))

    def recvMsg(self, conn):
        tmp = self.recv(conn).decode("utf-8")
        # print(tmp)
        return tmp

    def recv(self, conn):
        return conn.recv(8192)

    def sendJson(self, conn, data):
        self.sendMsg(conn, json.dumps(data))

    def sendMsg(self, conn, data):
        self.send(conn, data.encode("utf-8"))

    def send(self, conn, data):
        conn.send(data)

    def getHash(self):
        m = hashlib.md5()
        m.update((str(self.__hash__()) + str(time.monotonic()) +
                  str(random.random()) + self.getMyIP()).encode("utf-8"))
        return m.hexdigest()

    def debug(self):
        self.info['debug'] = True
if __name__ == '__main__':
    C = Cloud()
    C.debug()
    C.startCloud(50000)
    C.connect(C.getMyIP(), 50000)
