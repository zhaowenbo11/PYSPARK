# coding:utf8
from pyspark import SparkConf, SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("local[*]").setAppName("text")
    sc = SparkContext(conf=conf)

    rdd = sc.textFile("../Data/input/words.txt")
    rdd2 = rdd.flatMap(lambda x: x.split(" ")).map(lambda x: (x, 1))

    # 通过countByKey对key进行计数,这是个action算子，返回值不是RDD类型
    result = rdd2.countByKey()

    print(result)
    print(type(result))