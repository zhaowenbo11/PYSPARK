# coding:utf8
from pyspark import SparkConf, SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("local[*]").setAppName("text")
    sc = SparkContext(conf=conf)

    rdd1 = sc.parallelize([1, 2, 3, 4])
    rdd2 = sc.parallelize([5, 6, 7, 'a'])
    rdd3 = rdd1.union(rdd2)
    print(rdd3.collect())

"""
1. union算子不会去重
2. RDD的类型不同也可以合并
"""