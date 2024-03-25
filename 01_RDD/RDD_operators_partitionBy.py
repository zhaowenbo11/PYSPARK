# coding:utf8
from pyspark import SparkConf, SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("local[*]").setAppName("text")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([('a', 1), ('a', 1), ('a', 1), ('b', 1), ('b', 1), ('b', 1)])

    # 使用partitionBy算子进行自定义分区
    def process(key):
        if 'a' == key or 'b' == key: return 0
        if 'c' == key: return 1
        return 2


    print(rdd.partitionBy(3, process).glom().collect())
