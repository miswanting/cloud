# lib_Net 文档

啊啊啊

## Cloud 类

### 数据结构

#### Node

|    名称    |   类型   |  备注  |
| :------: | :----: | :--: |
|   hash   |  Hash  |      |
|    ip    | String |      |
|   port   | Number |      |
| lastNode |  Hash  |      |
| nextNode |  Hash  |      |
| randNode |  Hash  |      |

#### Cloud

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

##### setLast设置上一节点

|  名称  |  类型  |  备注  |
| :--: | :--: | :--: |
| data | Node |      |

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