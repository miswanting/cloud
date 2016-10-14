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

##### connect

|  名称  |  类型  |  备注  |
| :--: | :--: | :--: |
| data | Node |      |

##### acceptConnect

|  名称  |  类型  |  备注  |
| :--: | :--: | :--: |
| data | Node |      |

##### getCloud
无

##### setCloud
|  名称  |  类型   |  备注  |
| :--: | :---: | :--: |
| data | Cloud |      |


##### setLast

|  名称  |  类型  |  备注  |
| :--: | :--: | :--: |
| data | Node |      |

#### News

##### nodeOnline
|  名称  |  类型  |  备注  |
| :--: | :--: | :--: |
| data | Node |      |

##### nodeOffline

|  名称  |  类型  |  备注  |
| :--: | :--: | :--: |
| data | Node |      |

##### setCloud
|  名称  |  类型   |  备注  |
| :--: | :---: | :--: |
| data | Cloud |      |