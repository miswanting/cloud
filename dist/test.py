# coding=utf-8
import time
import threading
import socket
import lib_Net


class Test():
    def __init__(self):
        self.isRunning = True
        ip = socket.gethostbyname(socket.gethostname())
        
        def runA():
            A = lib_Net.Cloud()
            A.start(50000)
        
        def runB():
            B = lib_Net.Cloud()
            B.start(50001)
            B.connect(ip, 50000)
        
        def runC():
            C = lib_Net.Cloud()
            C.start(50002)
            C.connect(ip, 50000)
            # C.disconnect()
        
        def runD():
            D = lib_Net.Cloud()
            D.start(50003)
            D.connect(ip, 50000)
            # D.disconnect()
        
        tA = threading.Thread(name='ThreadA', target=runA)
        tB = threading.Thread(name='ThreadB', target=runB)
        tC = threading.Thread(name='ThreadC', target=runC)
        tD = threading.Thread(name='ThreadC', target=runD)
        tA.start()
        time.sleep(1)
        tB.start()
        time.sleep(1)
        tC.start()
        time.sleep(1)
        tD.start()


if __name__ == '__main__':
    I = Test()
