# Spark SQL

## 一、快速入门
### 1.什么是SparkSQL
- Spark SQL是spark的一个模块，用于处理海量结构化数据

### 2.为什么学习spark SQL
- spark SQL本身十分优秀，支持SQL语言、性能强、可以自动优化、API简单、兼容HIVE等

### 3.spark SQL的特点
- 融合性
  - sql可以无缝集成在代码中，随时用SQL处理数据
- 统一数据访问
- HIVE兼容
  - 可以使用spark SQL直接计算并生成hive数据表
- 标准化连接

## 二、SparkSQL概述

### 1.spark SQL和Hive的异同
- 都是分布式sql计算引擎，用于处理大规模结构化数据，都运行在YARN上
- spark基于内存计算，底层运行SparkRDD，无元数据管理
- hive基于磁盘迭代，底层运行MR，元数据由meta store管理

## 三、DataFrame入门和操作

## 四、SparkSQL函数定义

## 五、SparkSQL的运行流程

## 六、SparkSQL整合Hive

## 七、分布式SQL引擎配置

