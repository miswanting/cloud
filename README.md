# lib_Net 文档

## Server 类

服务器模块的底层实现。

### 属性

#### HOST

服务器模块的侦听IP地址。

#### PORT

服务器模块的侦听端口。

#### event

服务器模块的消息队列。

#### passiveSubs

服务器模块的子应答模块。

### 方法

#### addEvent(self, event)

像服务器模块的消息队列中添加消息。

#### send_json(self, h, data)

#### recv_json(self, h)

#### send_str(self, h, data)

#### recv_str(self, h)

#### send(self, h, data)

#### recv(self, h)

## Client 类

客户端模块的底层实现。

### 属性

#### HOST

客户端模块要连接的目标IP地址。

#### PORT

客户端模块要连接的目标端口。

#### event

客户端模块的消息队列。

### 方法

#### addEvent(self, event)

像服务器模块的消息队列中添加消息。

#### send_json(self, data)

#### recv_json(self)

#### send_str(self, data)

#### recv_str(self)

#### send(self, data)

#### recv(self)

## Cloud 类

### 方法

#### startServer(self, host='0.0.0.0', port=8765)

在给定的地址创建侦听服务器。

#### connect(self, host, port=8765)

连接到给定地址的服务器。

#### api(self, arg)

接收返回调用的接口。

### 数据结构

#### Node: Dict

|    名称    |   类型   |  备注  |
| :------: | :----: | :--: |
|   hash   |  Hash  |      |
|    ip    | String |      |
|   port   | Number |      |
| lastNode |  Hash  |      |
| nextNode |  Hash  |      |
| randNode |  Hash  |      |

#### Cloud: Dict

|  名称  |  类型  |  备注  |
| :--: | :--: | :--: |
|  *   | Node |      |

### 网络包命令

#### Package

##### connect——连接云

|  名称  |  类型  |  备注  |
| :--: | :--: | :--: |
| data | Node |      |

##### acceptConnect——同意连接云

|  名称  |  类型  |  备注  |
| :--: | :--: | :--: |
| data | Node |      |

##### getCloud——获取云

无

##### setCloud——设置云

|  名称  |  类型   |  备注  |
| :--: | :---: | :--: |
| data | Cloud |      |

##### setLast——设置上一节点

|  名称  |  类型  |  备注  |
| :--: | :--: | :--: |
| data | Node |      |

##### ping——ping测试

无

#### News

##### nodeOnline——节点上线

|  名称  |  类型  |  备注  |
| :--: | :--: | :--: |
| data | Node |      |

##### nodeOffline——节点下线

|  名称  |  类型  |  备注  |
| :--: | :--: | :--: |
| data | Node |      |

##### setCloud——设置云

|  名称  |  类型   |  备注  |
| :--: | :---: | :--: |
| data | Cloud |      |

## Protocol 类

TODO

## 新类

| NetCore |
| ------- |
|         |
|         |

## 附录

### 附录1——

1. 启动A，建立服务器As。
2. 启动B，建立服务器Bs。
3. B实例化客户端Bc并连接As。
4. As发送欢迎信息。
5. Bc发送认证信息。——verify
6. As发送确认信息。——pass
7. Bc发送连入请求。——join
8. As发送回应信息。——accept
9. A实例化客户端Ac并连接Bs。
10. 启动C，建立服务器Cs。
11. C实例化客户端Cc并连接Bs。
12. Bs发送欢迎信息。
13. Cc发送认证信息。——verify
14. Bs发送确认信息。——pass
15. Cc发送连入请求。——join
16. Bs发送回应信息。——accept
17. B通过Bs向Ac发送请求。——insert
18. Ac与Bs的连接断开。
19. Ac连接Cs。
20. Cs发送欢迎信息。
21. Ac发送认证信息。——verify
22. Cs发送确认信息。——pass
23. A发送全局广播说明相关改动已完成。——overwrite