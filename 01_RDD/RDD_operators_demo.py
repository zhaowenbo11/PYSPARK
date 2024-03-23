# coding:utf8
import json
from pyspark import SparkConf, SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("local[*]").setAppName("text")
    sc = SparkContext(conf=conf)

    # 读取文件
    file_rdd = sc.textFile("")

    # 进行rdd数据的split 按照|符号切分，得到一个个json数据
    json_rdd = file_rdd.flatMap(lambda line: line.split("|"))

    # 通过python内置的json库，完成json字符串到字典对象的转换
    dict_rdd = json_rdd.map(lambda json_str: json.loads(json_str))

    # 过滤数据，只保留“北京的数据”
    beijing_rdd = dict_rdd.filter(lambda d: d['areaName'] == '北京')

    # 组合 北京 和 商品类型 形成新的字符串
    category_rdd = beijing_rdd.map(lambda x: x['areaName'] + '-' + x['category'])

    # 对结果进行去重
    result_rdd = category_rdd.distinct()

    # 输出
    print(result_rdd.collect())

