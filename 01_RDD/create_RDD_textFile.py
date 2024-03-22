# coding:utf8
from pyspark import SparkConf,SparkContext
if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster("local[*]")
    sc = SparkContext(conf = conf)

    # 通过text File API 读取数据

    # 读取本地文件数据
    file_rdd1 = sc.textFile("../data/input/words.txt")
    print("默认读取分区数：", file_rdd1.getNumPartitions())
    print("file_rdd1内容", file_rdd1.collect())

    # 加最小分区数参数测试
    file_rdd2 = sc.textFile("../data/input/words.txt", 3)
    # 最小分区数是参考值，spark有自己的判断，给的太大spark不会理会
    file_rdd3 = sc.textFile("../data/input/words.txt", 100)
    print("rdd2分区数", file_rdd2.getNumPartitions())
    print("rdd3分区数", file_rdd3.getNumPartitions())

    # 读取HDFS文件测试
    hdfs_rdd = sc.textFile("hdfs://hadoop01:8020/input/words.txt")
    print("hdfs_rdd内容", hdfs_rdd)
