# Spark DataFrame

## DataFrame 简介
Spark DataFrame 是 Spark 基于 [RDD](spark-rdd.md) 实现的面向结构化数据的高阶抽象, 它将分布式的数据集以行列的方式组织起来，并提供了很多关系型操作的 API。  
_Spark 在 1.6 版本还提供了 DataSet 的抽象，对 DataFrame 进行了扩展，支持面向对象的处理。
而本质上 DataFrame 就是对象类型为 Row 的 DataSet, 因此在 Spark 2.0 之后将 DataFrame API 和 DataSet API 进行了统一， 即 DataFrame = DataSet[Row]。_  

## 创建 DataFrame
DataFrame 的创建方式有很多种，通过 RDD 创建、通过读取外部系统创建等
本篇文章的后续实践可在 spark-shell 中完成, 其中会默认实例化一个 SparkContext 实例 `sc` 和 SparkSession 实例 `spark`。
```shell
spark-shell
```
### 通过 Java 集合创建
通过内存中的集合创建 DataFrame
``` 
scala> val scalaList = List(1 -> "A", 2 -> "B", 3 -> "C") 
scalaList: List[(Int, String)] = List((1,A), (2,B), (3,C))

scala> val df = spark.createDataFrame(scalaList)
df: org.apache.spark.sql.DataFrame = [_1: int, _2: string]

scala> val withColNameDF = df.toDF("id", "name")
withColNameDF: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> withColNameDF.show
+---+----+
| id|name|
+---+----+
|  1|   A|
|  2|   B|
|  3|   C|
+---+----+
```

### 通过 RDD 创建
前面我们说过 DataFrame 是架构化的高阶抽象，因此为 Row 类型的 RDD 指定结构(schema)即可得到 DataFrame  
```
scala> import org.apache.spark.sql.Row
scala> val rdd = sc.parallelize(List(Row(1, "A"), Row(2, "B"), Row(3, "C")))

scala> import org.apache.spark.sql.types._
scala> val schema = new StructType() .add(StructField("id", IntegerType)) .add(StructField("name", StringType))
schema: org.apache.spark.sql.types.StructType = StructType(StructField(id,LongType,true),StructField(name,StringType,true))

scala> val df = spark.createDataFrame(rdd, schema)
df: org.apache.spark.sql.DataFrame = [id: , name: string]

scala> df.show()
+---+----+
| id|name|
+---+----+
|  1|   A|
|  2|   B|
|  3|   C|
+---+----+
```
### 读取 Hive 表创建
Spark 通过与 Hive 集成，即可轻松访问 Hive 中的表  
假设 Hive 中有张 test 表, 那么 Spark 可以通过 `table` 或者 `sql` 方法来将表中的数据读取为 DataFrame  
``` 
hive> set hive.cli.print.header=true;
hive> select * from test_table;
OK
test_table.id	test_table.name
1	A
2	B
3	C
```
#### table
指定表名，将整张表返回为 DataFrame 
```
scala> val df = spark.table("default.test_table")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.show
+---+----+
| id|name|
+---+----+
|  1|   A|
|  2|   B|
|  3|   C|
+---+----+
```
#### sql 
执行 SQL 语句，将结果集返回为 DataFrame  
```
scala> val df = spark.sql("SELECT * FROM default.test_table")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.show
+---+----+
| id|name|
+---+----+
|  1|   A|
|  2|   B|
|  3|   C|
+---+----+
```
### 读取外部系统
#### 通过 jdbc 读取数据库 
todo 
#### 读取外部文件系统
todo 

## Transformation 算子
### 基础转换
#### select
选择一组列，或基于列的函数
``` 
scala> val df = spark.sql("select 1 as id, 'A' as name")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.select(df("id"), df("name"), org.apache.spark.sql.functions.lower(df("name")) as "lower_name" ).show
+---+----+----------+
| id|name|lower_name|
+---+----+----------+
|  1|   A|         a|
+---+----+----------+
```
#### selectExpr
选择一组列，或基于列的 SQL 表达式
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.selectExpr("id", "name", "LOWER(name) as lower_name" ).show
+---+----+----------+
| id|name|lower_name|
+---+----+----------+
|  1|   A|         a|
+---+----+----------+
```
#### filter
根据指定的条件过滤出符合条件的数据, 过滤条件也可以是 SQL 表达式
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name UNION SELECT 2 AS id, 'B' AS name ")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.filter(df("id") > 1).show()
+---+----+
| id|name|
+---+----+
|  2|   B|
+---+----+

scala> df.filter("id > 1").show()
+---+----+
| id|name|
+---+----+
|  2|   B|
+---+----+
```
#### where 
与 [filter](#filter) 行为一致，提供与 SQL 语义一致的同名算子
#### sort
根据指定的列对数据进行排序  
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name UNION SELECT 2 AS id, 'B' AS name ")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.sort(df("id").desc).show()
+---+----+
| id|name|
+---+----+
|  2|   B|
|  1|   A|
+---+----+
```
#### orderBy
与 [orderBy](#orderby) 行为一致，提供与 SQL 语义一致的同名算子  

#### na
#### stat

#### hint
#### as 
为 DataFrame 定义别名  
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name UNION SELECT 2 AS id, 'B' AS name ").as("aliasOfDF")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.filter("aliasOfDF.id > 1").show()
+---+----+
| id|name|
+---+----+
|  2|   B|
+---+----+
```
#### alias 
与 [as](#as-) 语义一致  
#### to
将 DataFrame 转换为具有给定 schema 的新 DataFrame
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name UNION SELECT 2 AS id, 'B' AS name ").as("aliasOfDF")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> val schema = new StructType().add(StructField("name", StringType)).add(StructField("id", IntegerType)) 
schema: org.apache.spark.sql.types.StructType = StructType(StructField(name,StringType,true),StructField(id,IntegerType,true))

scala> df.to(schema).show
+----+---+
|name| id|
+----+---+
|   A|  1|
|   B|  2|
+----+---+

```
#### toDF
将 DataFrame 转换为具有指定的列名的新的 DataFrame  
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name UNION SELECT 2 AS id, 'B' AS name ").as("aliasOfDF")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.toDF("name", "id").show
+----+---+
|name| id|
+----+---+
|   1|  A|
|   2|  B|
+----+---+
```
#### unpivot
#### melt
#### observe
#### explode 将弃用
#### withColumn
#### withColumnRenamed
#### withColumns
#### withColumnsRenamed
#### drop
#### transform
#### map
#### flatMap
#### toJSON

### 分区转换
#### sortWithinPartitions
#### mapPartitions
#### repartition
#### repartitionByRange
#### coalesce 

### 集合运算
#### join
#### crossJoin 
#### limit
#### offset
#### union
#### unionAll
#### unionByName
#### intersect
#### intersectAll
#### except
#### exceptAll
#### sample
#### randomSplit
#### randomSplitAsList


### 聚合操作
#### groupBy
#### agg
#### roolup
#### cube
#### groupingSets
#### distinct
#### dropDuplicates
#### describe

## Action 算子
### 转换为内存集合
#### reduce
#### isEmpty
#### head
#### first
#### foreach
#### foreachPartition
#### take
#### tail
#### takeAsList

#### collect
#### collectAsList
#### toLocalIterator
#### count 
#### 

## 控制算子
### createTempView
### createOrReplaceTempView
### createGlobalTempView
### createOrReplaceGlobalTempView

### 写入外部算子
#### write v1 
#### writeTo v2
#### mergeInto spark 4.0 +
#### 


