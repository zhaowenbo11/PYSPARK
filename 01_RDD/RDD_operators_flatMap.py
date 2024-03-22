#coding:utf8
from pyspark import SparkConf,SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("local[*]").setAppName("WordCountHelloWord")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize(["hadoop hadoop spark", "flink spark hadoop", "spark spark hadoop"])
    # 得到所有的单词，组成RDD,flatMap的传入参数和map一致，就是给map逻辑用的，解除嵌套无需逻辑（传参）
    rdd2 = rdd.flatMap(lambda line: line.split(" "))
    print(rdd2.collect())