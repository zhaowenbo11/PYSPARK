# Spark Core 

## 一、RDD产生背景

### 1.为什么需要RDD
- 分布式计算需要：
  - 分区控制
  - shuffle控制
  - 数据存储\序列化
  - 数据计算API等功能
- RDD是抽象对象
### 2.什么是RDD
- RDD ***弹性分布式数据集***
- 是spark中最基本的数据抽象，代表一个不可变、可分区、里面元素可并行计算的集合
- RDD中的数据是分布式存储的，可用于分布式计算，可以存储在内存或磁盘中
### 3.RDD的五大特性
- A list of partitions **RDD是有分区的**
- A function for computing each split **计算方法都会作用到每一个分区上**
- A list of dependenceies on other RDDs **RDD之间是有相互依赖的关系的**
- Optionally, a Partitioner for key-value RDDs **KV型RDD可以有分区器**
- Optionally, a list of preferred locations to computr each split on (e.g. block locations for an HDFS file)**RDD分区数据的读取会尽量靠近数据所在地**


## 二、RDD的创建
## 三、RDD的重要算子
## 四、RDD的缓存和检查点机制
## 五、Spark执行的基本原理