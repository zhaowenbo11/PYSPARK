# coding:utf8
from pyspark import SparkConf, SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("local[*]").setAppName("text")
    sc = SparkContext(conf=conf)

    rdd1 = sc.parallelize([(1001, 'zhangsan'), (1002, 'lisi'), (1003, 'wangwu')])
    rdd2 = sc.parallelize([(1001, '销售'), (1002, 'a'), (1003, 'b')])

    # 通过join算子进行rdd之间的关联
    # 对于join算子来说，关联条件 按照二元元组的key 来进行关联

    print(rdd1.join(rdd2).collect())

    # 左外连接
    print(rdd1.leftOuterJoin(rdd2).collect())