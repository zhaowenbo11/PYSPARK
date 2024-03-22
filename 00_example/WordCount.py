#coding:utf8
from pyspark import SparkConf,SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("local[*]").setAppName("WordCountHelloWord")
    sc = SparkContext(conf=conf)


    # 读取文件获取数据，构建RDD
    flie_rdd = sc.textFile("hdfs://hadoop01:8020/input/word.txt")

    # 通过flatMap API 取出所有的单词
    words_rdd = flie_rdd.flatMap(lambda line: line.split(" "))

    # 将单词转换成元组，k是单词 ， v是1
    words_with_one_rdd = words_rdd.map(lambda x: (x, 1))

    # 用reduceByKey 对单词进行分组 并进行value的聚合
    result_rdd = words_with_one_rdd.reduceByKey(lambda a,b: a + b)

    # 通过collect算子 将RDD的数据上传到Driver中，打印输出
    print(result_rdd.collect())

