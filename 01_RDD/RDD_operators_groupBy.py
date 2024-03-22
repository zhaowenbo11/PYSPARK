# coding:utf8
from pyspark import SparkConf, SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("local[*]").setAppName("text")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([('a', 1), ('a', 1), ('a', 1), ('b', 1), ('b', 1), ('b', 1)])

    # 通过groupBy对数据进行分组
    # groupBy传入的函数的意思是：通过这个函数，确定按照谁来分组（返回谁即可）
    # 分组规则和SQL一致（hash）
    result = rdd.groupBy(lambda t: t[0])
    print(result.collect())