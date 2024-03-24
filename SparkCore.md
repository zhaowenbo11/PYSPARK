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

### 1.程序执行入口 SparkContext对象
- 只有构建出SparkContext，才能执行后续的API调用和计算

### 2. RDD的创建
- 通过并行化集合创建（本地对象  转  分布式RDD）
  - API: rdd = sparkcontext.parallelize(参数1，参数2)
  - 参数1 ：集合对象即可，例如list
  - 参数2 ：分区数

- 读取外部数据源创建 （读取文件）
  - API: sparkcontext.textFile(参数1，参数2)
  - 参数1 ： 必填 ，文件路径，支持本地文件，支持HDFS
  - 参数2 ：可选，表示最小分区数量
  - **注意**：参数2 话语权不足，spark有自己的判断，在它允许范围内，参数2有效果，超出spark允许的范围，参数2失效
  - API : wholeTextFile (参数1，参数2) --适合读取小文件，可以减少shuffle的几率

### 3.RDD算子
- 算子：分布式集合对象上的API称之为算子
- 方法/函数 ：本地对象的API
- 算子分类
  - Transformation：转换算子
    - 定义：RDD的算子，返=返回值仍旧是一个RDD的，称之为转换算子
    - 特性：这类算子是**lazy 懒加载**的，如果没有action算子，transformation算子是不工作的
  - Action：动作（行动）算子
    - 定义：返回值**不是RDD**的就是action算子

### 4.常用的Transformation算子

- map算子
  - 功能：是将RDD的数据一条条处理（处理的逻辑 基于map算子中接受的处理函数），返回新的RDD
  - 语法：rdd.map(func)
- flatMap算子
  - 功能：对RDD执行map操作，然后进行**接触嵌套**的操作
- reduceByKey算子
  - 功能：**针对KV型**RDD，自动按照key分组，然后根据你提供的聚合逻辑，完成**组内数据（value）**的聚合操作
  - 用法：rdd.reduceByKey(func)
  - 接受2个传入参数（类型要一致），返回一个返回值，类型和传入要求一致
- mapValues算子
  - 功能：针对**二元元组RDD**，对其内部的二元元组的**Value**执行**map**操作
  - 语法：rdd.mapValues(func)
  - **注意**：传入的参数 是二元元组的value值，只针对value进行处理
- groupBy算子
  - 功能：将RDD的数据进行分组
  - 语法：rdd.groupBy(func)
  - 函数要求传入一个参数，返回一个返回值，类型无所谓
- Filter算子
  - 功能：过滤想要的数据进行保留
  - 语法：rdd.Filter(func)
  - 传入一个参数 进来是随意类型 返回值必须是 True or False
  - 返回是TRUE的结果被保留，False的被丢弃
- distinic算子
  - 功能：对RDD数据进行去重，返回新的RDD
  - 语法：rdd.distinct()
- union算子
  - 功能：将两个RDD合并成一个RDD返回
  - 用法：rdd.union(other_rdd)
  - **注意**：只合并，不去重，不同类型的RDD可以混合
- join算子
  - 功能：对两个RDD执行JOIN操作（可实现SQL的内\外连接）
  - **注意** join算子只能用于二元元组
  - 语法： rdd.join(other_rdd) -- 内连接  
  - rdd.leftOuterJoin(other_rdd)   -- 左外连接
  - rdd.rightOuterJoin(other_rdd)  -- 右外连接
- intersection算子
  - 功能：求2个RDD的交集，返回新的RDD
  - 语法：rdd.intersection(other_rdd)
- glom算子
  - 功能：将RDD的数据加上嵌套，这个嵌套按照分区来进行
  - 语法：rdd.glom()
- groupByKey算子
  - 功能：针对KV型RDD，自动按照key分组
  - 语法：rdd.groupByKey() 自动按照key分组
- sortBy算子
  - 功能：对RDD的数据进行排序，基于自己指定的排序依据
  - 语法：rdd.sort(func,ascending=False,numPartitions = 1)
  - ascending=True 表示升序排序
- sortByKey算子
  - 功能：针对**KV型**RDD，按照KEY进行排序
  - 语法：rdd.sortByKey(ascending=True,numPartitions=None, keyfunc=<function RDD, <lambda> >)

### 4.常用的Action算子

- countByKey算子
  - 功能：统计key出现的次数，一般适用于KV型RDD
- collect算子
  - 功能：将RDD各个分区内的数据，统一收集到Driver中，形成一个List对象
  - **注意**：RDD是分布式对象，其数据量可以很大，所以用这个算子之前要心知肚明的了解结果数据集不会太大，不然会把Driver内存撑爆
- reduce算子
  - 功能：对RDD的数据集按照你传入的逻辑进行聚合
  - 语法：rdd.reduce(func)
- fold算子
  - 功能：和reduce一样，接受传入逻辑进行聚合，聚合是带有初始值的
  - 这个初始值聚合，会作用在：分区内聚合、分区间聚合
- first算子
  - 功能：取出RDD的第一个元素
- takeSample算子
  - 功能：随机抽样RDD的数据
  - 用法：takeSample(参数1：True/False, 参数2：采样数，参数3：随机数种子)
  - 参数1：True表示允许去同一个数据，False表示不允许取同一个数据，和数据内容无关，是否重复表示的是同一个位置的数据
  - 参数2：抽样要几个
  - 参数3：随机数种子，一般参数3我们不传，spark会自动给与随机数种子
- takeOrdered算子
  - 功能：对RDD进行排序取前n个
  - 用法：rdd.takeOrdered(参数1，参数2)
  - 参数1：要几个数据
  - 参数2：对排序的数据进行更改（不会更改数据本身，只是在排序的时候换个样子）
  - 这个方法使用按照元素自然顺序升序排序，如果想要倒序，需要用参数2来对排序的数据进行处理
                                                                                                                                                                                                                                   

## 三、RDD的重要算子
## 四、RDD的缓存和检查点机制
## 五、Spark执行的基本原理