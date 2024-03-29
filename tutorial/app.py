from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName('my_app')
sc = SparkContext(conf=conf)

text_file = sc.textFile("hdfs://localhost:9000/user/hadoop/input")
counts = text_file.flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile("hdfs://localhost:9000/user/hadoop/output")
