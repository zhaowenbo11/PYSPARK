#coding:utf8
from pyspark import SparkConf,SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("local[*]").setAppName("WordCountHelloWord")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([('a', 1), ('a', 1), ('b', 2), ('b', 5)])
    print(rdd.reduceByKey(lambda a,b : a + b).collect())