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
- foreach算子
  - 功能：对RDD的每一个元素，执行你提供的逻辑操作（和map一个意思），但是这个方法没有返回值
  - 用法：rdd.foreach(func)
  - **注意**：foreach算子是在executer中执行输出，某种程度上性能较高
- saveAsTextFile算子
  - 功能：将RDD数据写入文本文件中
  - **注意**：和foreach算子一样，结果不经过Driver，直接输出

### 5.分区操作算子 —— Transforamtion

- mapPartitions算子
  - 功能：mapPartitions一次被传递的是一整个分区的数据，作为一个迭代器（一个list）对象传入过来
- foreachPartition算子
  - 功能：和普通foreach一致，一次处理的是一整个分区数据，没有返回值
- partitionBy算子
  - 功能：对RDD进行自定义分区操作
  - 用法：rdd.partitionBy(参数1，参数2)
  - 参数1：重新分区后有几个分区
  - 参数2：自定义分区规则，函数传入
  - 一个传入参数进来，类型无所谓，但返回值一定是int类型，将key传给这个参数，自己写逻辑，决定返回一个分区编号，分区编号从0开始，不要超出分区数-1
- repartition算子
  - 功能：对RDD的分区执行重新分区（仅数量）
  - 用法：rdd.repartition(N)
  - 传入N 决定新的分区数
  - **注意**：对分区数量的操作，一定要慎重，一般情况下，我们写spark代码 除了要求全局排序设置为1个分区外，多数时候所有API中关于分区相关的代码我们都不太理会
  - 分区如果增加，会导致shuffle增加

### 6. 面试题：groupByKey和reduceByKey的区别
- groupByKey仅分组
- reduceByKey除了有**ByKey**的分组功能外，还有reduce聚合功能，所以是一个分组+聚合一体化的算子
- reduceByKey的性能是远大于**groupByKey + 聚合逻辑**的
                                                                                                                                                                                                                                   

## 三、RDD的持久化

### 1. RDD的数据是过程数据

- RDD之间进行相互迭代计算，当执行开启后，新RDD的生成，代表老RDD的消失
- RDD的数据是过程数据，只在处理的过程中存在，一旦处理完成就不见了
- **这个特性可以最大化的利用资源，老旧RDD没用了就从内存中清理，给后续的计算腾出内存空间**

### 2. RDD的缓存

- 缓存是**分散存储**
- RDD的缓存技术：spark提供了缓存API，可以让我们通过调用API，将指定的RDD数据保留在**内存或硬盘上**
    - rdd.cache()  - 缓存到内存中
    - rdd.persist(StorageLevel.MEMORY_ONLY) - 仅内存缓存
    - rdd.persist(StorageLevel.MEMORY_ONLY_2) - 仅内存缓存，2个副本
    - rdd.persist(StorageLevel.DISK_ONLY) - 仅缓存硬盘上
    - rdd.persist(StorageLevel.MEMORY_AND_DISK) - 先进内存，不够再放硬盘
    - rdd.unpersist() - 主动清理缓存的API

### 3. RDD的CheckPoint

- CheckPoint技术，也是将RDD的数据保存起来，但是它**仅支持硬盘存储**并且，它被设计认为是安全的，不保留**血缘关系**
- CheckPoint存储RDD数据，是**集中收集各个分区的数据进行存储**
- CheckPoint和缓存的对比
  - CheckPoint不管分区数量多少，风险是一样的，缓存分区越多，风险越高
  - CheckPoint支持写入HDFS，缓存不行，HDFS是高可靠存储，CheckPoint被认为是安全的
  - CheckPoint不支持写入内存，缓存可以，缓存如果写内存，性能比CheckPoint好一些
  - CheckPoint因为设计认为是安全的，所以**不保留血缘关系**，而缓存因为设计上认为不安全，所以保留
- 代码
  - 设置CheckPoint的第一件事情，选择CP的保存路径
  - 如果是local模式，可以支持本地文件系统，如果是在集群允许，千万要用HDFS
  - sc.setCheckpointDir("hdfs://hadoop01:8020/output/ckp")
  - 用的时候，直接调用CheckPoint算子即可
  - rdd.checkpoint()


## 四、Spark案例练习

### 1. 搜索引擎日志分析
数据来源：搜狗实验室提供【用户查询日志（SogouQ)】数据 http://www.sogou.com/labs/resource/q.php
本实验使用SogouQ.txt文件  文件路径： ../Data/input/SougouQ.txt
- 业务需求：
  - 1. 搜索关键词统计 ：字段：查询词；中文分词jieba
  - 2. 用户搜索点击统计 ：字段：用户ID和查询词 ；分组、统计
  - 3. 搜索时间段统计 ： 字段： 访问时间 ； 统计、排序

### 2. 提交到集群运行
- 榨干集群性能提交
  - 查看CPU核数： cat /proc/cpuinfo | grep processer | wc -l
  - 查看内存有多大： free -g
### 3. 网站日志分析
- 资料：apache.log
- 需求：
  - 1. 计算当前网站访问的PV（被访问次数）
  - 2. 计算当前访问的UV（访问的用户数）
  - 3. 查看有哪些IP访问本网站
  - 4. 哪个页面的访问量最高


## 五、共享变量

### 1. 广播变量
- 问题引出：内存浪费。executor是**进程**，进程内资源共享，两份数据没有必要
- 使用方式：
  - 将本地list标记成广播变量：broadcast = sc.broadcast(stu_info_list)
  - 使用广播变量，从broadcast对象中取出本地list对象即可: value = broadcat.value
  - 也就是 先放进去broadcast内部，然后从broadcast内部取出来用，中间传输的是broadcast这个对象了
  - 只要中间传输的是brodacast对象，spark就会留意，只会给每个executor发一份
- 使用场景：
  - 本地集合对象和分布式集合对象（RDD）进行关联的时候，需要将本地集合对象封装为广播变量
  - 可以节省网络IO的次数和executor内存占用


### 2. 累加器

- 需求：想要对**map**算子计算中的数据，进行技术累加，得到全部数据计算完后的累加结果
- 类似于内存指针
- 使用方式：acmlt = sc.accumulator(0)
- 注意事项：

### 3. 综合案例

## 六、Spark内核调度（重点理解）
### 1. DAG

- **DAG:有向无环图**，有方向没有形成闭环的执行流程图
- spark的核心是根据RDD来实现的，Spark Scheduler则为Spark核心实现的重要一环，其作用就是任务调度
- Spark的任务调度就是如何组织任务去处理RDD每个分区的数据，根据RDD的依赖关系构建DAG，基于DAG划分Stage，将每个Stage中的任务发放到指定节点运行
- 基于Spark的任务调度原理，可以合理规划资源利用，做到尽可能用最少的资源高效的完成计算
- Job和Action：
  - Action是执行链条的开关，RDD迭代链条的开关
  - 一个Action会产生一个Job（一个应用程序内的子任务）
  - **一个Action = 一个DAG = 一个Job**

### 2. DAG的宽窄依赖和阶段划分

- 在SparkRDD前后之间的关系分为：
  - 窄依赖
  - 宽依赖
- 窄依赖：父RDD的一个分区，全部将数据发给子RDD的一个分区
- 宽依赖：父RDD的一个分区，将数据发给子RDD的多个分区
- 宽依赖别名：shuffle
- 阶段划分：
  - 划分依据：从后向前，遇到**宽依赖**就划分出一个阶段，称之为stage
  - stage的内部一定都是窄依赖

### 3. 内存迭代计算

- spark默认受到全局并行度的限制，除了个别算子有特殊分区情况，大部分的算子，都会遵循全局并行度的要求，来规划自己的分区数
- 如果全局并行度是3，大部分算子分区都是3
- **面试题：spark是怎么做内存计算的？DAG的作用？stage阶段划分的作用？**
  - spark会产生DAG图
  - DAG图会基于分区和宽窄依赖关系划分阶段
  - 一个阶段的内部都是窄依赖，窄依赖内，如果形成前后1：1的分区对应关系，就可以产生许多内存迭代计算的管道
  - 这些内存迭代计算的管道，就是一个个具体的执行task
  - 一个task是一个具体的线程，任务跑在一个线程内，就是走内存迭代计算了
- **面试题：spark为什么比MR快？**
  - spark的算子丰富，执行内存迭代计算
  - 算子交互上和计算上可以尽量多的内存计算而非磁盘迭代

### 4.Spark并行度
- **先有并行度，才有分区规划**
- spark的并行：在同一时间内，有多少个task在同时运行
- 并行度：并行能力的设置
- 如何设置并行度（优先级从高到低）：
  - 代码中
  - 客户端提交参数中
  - 配置文件中
  - 默认（1，但是不会全部以1来跑，多数时候基于读取文件的分片数量来作为默认并行度）
- 全局并行度配置的参数： spark.default.parallelism(conf/spark-default.conf)
- 集群中如何规划并行度：
  - 设置为CPU总核心的2-10倍

### 5.Spark任务调度

- spark的任务，由Driver进行调度，这个工作包含：
  - 逻辑DAG产生
  - 分区DAG产生
  - Task划分
  - 将Task分配给Executor并监控其工作

- DAG调度器：将逻辑的DAG图进行处理，最终得到逻辑上的Task划分
- Task调度器：基于DAG Scheduler的产出，来规划这些逻辑的task，应该在哪些物理的executor上运行，以及监控管理它们的运行

### 6.拓展-Spark概念名词大全

- 一个spark环境可以运行多个Application
- 一个代码运行起来，会成为一个Application
- Application内部可以有多个Job
- 每个Job由一个Action产生，并且每个Job有自己的DAG执行图
- 一个Job的DAG图会基于宽窄依赖划分成不同的阶段
- 不同阶段内基于分区数量，形成多个并行的内存迭代管道
- 每一个内存迭代管道形成一个Task（DAG调度器划分将job内划分出具体的task任务，一个Job被划分出来的task在逻辑上称之为这个Job的taskset）
