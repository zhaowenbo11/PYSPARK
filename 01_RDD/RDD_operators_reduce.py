# coding:utf8
from pyspark import SparkConf, SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("local[*]").setAppName("text")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize(range(1,10))

    print(rdd.reduce(lambda a,b: a + b))