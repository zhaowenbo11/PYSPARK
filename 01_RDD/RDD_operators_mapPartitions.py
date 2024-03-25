# coding:utf8
from pyspark import SparkConf, SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("local[*]").setAppName("text")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1, 4, 6, 2, 6, 3, 8, 9], 3)

    def process(iter):
        result = list()
        for it in iter:
            result.append(it * 10)

        return result


    print(rdd.mapPartitions(process).collect())