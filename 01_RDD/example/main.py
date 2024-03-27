# coding:utf8
from pyspark import SparkConf, SparkContext
from pyspark.storagelevel import StorageLevel
from defs import context_jieba, filter_words, append_words, extract_user_and_word
from operator import add

if __name__ == '__main__':
    conf = SparkConf().setMaster("local[*]").setAppName("test")
    sc = SparkContext(conf = conf)

    # 1. 读取数据文件
    file_rdd = sc.textFile("../../Data/input/SogouQ.txt")

    # 2.对数据进行切分
    split_rdd = file_rdd.map(lambda x: x.split("\t"))

    # 3.因为要做多个需求，split_rdd 作为基础的rdd，需要多次使用
    split_rdd.persist(StorageLevel.DISK_ONLY)

    # TODO: 需求1：用户搜索的关键词分析
    # 主要分析热点词语
    # 将所有搜索内容取出
    # print(split_rdd.takeSample(True, 3))
    context_rdd = split_rdd.map(lambda x: x[2])

    # 对搜索内容进行分词分析
    words_rdd = context_rdd.flatMap(context_jieba)

    # 院校 帮 -> 院校帮
    # 博学 谷 -> 博学谷

    filter_rdd = words_rdd.filter(filter_words)
    # 将关键词转换
    final_words_rdd = filter_rdd.map(append_words)

    # 对单词进行分组聚合排序
    # 求出前五名
    result1 = final_words_rdd.reduceByKey(lambda a, b: a + b).\
        sortBy(lambda x: x[1], ascending=False, numPartitions=1).\
        take(5)
    print("需求1结果：", result1)

    # TODO:需求2：用户和关键词组合分析
    # 1.我喜欢传智播客
    # 1+我 1+喜欢 1+传智播客
    user_content_rdd = split_rdd.map(lambda x: (x[1], x[2]))
    # 对用户的搜索内容进行分词， 分词后和用户ID再次组合
    user_word_onr_rdd = user_content_rdd.flatMap(extract_user_and_word)
    # 对内容进行分组 聚合 排序 求前5
    result2 = user_word_onr_rdd.reduceByKey(lambda a, b: a+b).\
        sortBy(lambda x: x[1], ascending=False, numPartitions=1).\
        take(5)
    print("需求2结果：", result2)

    # TODO:需求3：热门搜索时间段分析
    # 取出所有时间
    time_rdd = split_rdd.map(lambda x: x[0])
    # 对时间进行处理，只保留小时精度即可
    hour_with_one_rdd = time_rdd.map(lambda x: (x.split(":")[0], 1))
    #分组 聚合 排序 求前5
    result3 = hour_with_one_rdd.reduceByKey(add).\
        sortBy(lambda x: x[1], ascending=False, numPartitions=1).\
        collect()
    print("需求3结果：", result3)