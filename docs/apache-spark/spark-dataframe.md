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
通过 jdbc 协议将数据从外部数据库系统如 MySQL/Postgres 等读取为 DataFrame  
本例子中先将 DataFrame 通过 [jdbc](#jdbc) 写入 MySQL 后，再从 MySQL 中读取数据，需要使用 MySQL 驱动来连接本地的 MySQL 数据库，因此需要将相应的驱动包加入 classpath，比如：
```shell
spark-shell --packages "mysql:mysql-connector-java:8.0.28" 
```

``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> val connectionProperties = new java.util.Properties()
scala> connectionProperties.put("user", "root")
scala> connectionProperties.put("password", "123456")
scala> connectionProperties.put("driver", "com.mysql.jdbc.Driver")

scala> df.write.jdbc(
  url="jdbc:mysql://localhost:3306/test?createDatabaseIfNotExist=true", 
  table="test_table__jdbc",
  connectionProperties=connectionProperties
)

scala> spark.read.jdbc(
  url="jdbc:mysql://localhost:3306/test?createDatabaseIfNotExist=true", 
  table="test_table__jdbc",
  properties=connectionProperties
).show
+---+-----+
| id| name|
+---+-----+
|  2|Name2|
|  1|Name1|
|  3|Name3|
+---+-----+
```

#### 读取外部文件系统
从外部文件系统（如 HDFS，S3等）将数据读取为 DataFrame
本例子中先将 DataFrame 通过 [csv](#csv) 写入 HDFS 后，再从 HDFS 中读取数据  
``` 
scala> df.write.mode("overwrite").option("header", "true").csv("hdfs:///test_write/test_csv")

scala> spark.read.format("csv").option("header", "true").load("hdfs:///test_write/test_csv").show
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+
```


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
根据指定的条件函数过滤出符合条件的数据, 过滤条件也可以是 SQL 表达式
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
与 [sort](#sort) 行为一致，提供与 SQL 语义一致的同名算子  

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
列转行, 将 DataFrame 的每条记录的每一列转为单独的行  
```  
scala> case class Person(id: Int, name: String, age: Int)
scala> val persons = List(Person(1, "Tom", 30), Person(2, "Jerry", 28))
persons: List[Person] = List(Person(1,Tom,30), Person(2,Jerry,28))

scala> val df = spark.createDataFrame(persons)
df: org.apache.spark.sql.DataFrame = [id: int, name: string ... 1 more field]

scala> df.show
+---+-----+---+
| id| name|age|
+---+-----+---+
|  1|  Tom| 30|
|  2|Jerry| 28|
+---+-----+---+

scala> val unpivotedDF = df.unpivot(ids=Array(df("id")), values=Array(df("name"), df("age").cast("string")), variableColumnName="k", valueColumnName="v")
unpivotedDF: org.apache.spark.sql.DataFrame = [id: int, k: string ... 1 more field]

scala> unpivotedDF.show
+---+----+-----+
| id|   k|    v|
+---+----+-----+
|  1|name|  Tom|
|  1| age|   30|
|  2|name|Jerry|
|  2| age|   28|
+---+----+-----+
```
#### melt
与 [unpivot](#unpivot-) 语义一致  
#### withColumn
根据现有的列或基于现有列的函数，添加或替换一个指定名称的列  
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.withColumn("id_copy", df("id")).withColumn("lower_name", org.apache.spark.sql.functions.lower(df("name"))).show
+---+----+-------+----------+
| id|name|id_copy|lower_name|
+---+----+-------+----------+
|  1|   A|      1|         a|
+---+----+-------+----------+
```
#### withColumnRenamed
重命名现有的列  
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.withColumnRenamed("id", "new_id").show
+------+----+
|new_id|name|
+------+----+
|     1|   A|
+------+----+
```

#### withColumns
对多个列执行 [withColumn](#withcolumn) 操作, 入参是 `新列名` -> `现有列或基于现有列的函数` 的 Map
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.withColumns(Map("id_copy" -> df("id"), "lower_name" -> org.apache.spark.sql.functions.lower(df("name")))).show
+---+----+-------+----------+
| id|name|id_copy|lower_name|
+---+----+-------+----------+
|  1|   A|      1|         a|
+---+----+-------+----------+
```
#### withColumnsRenamed
重命名多个现有的列, 入参是 `现有列的名称` -> `新列名` 的 Map
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.withColumnsRenamed(Map("id"-> "new_id", "name" -> "new_name")).show
+------+--------+
|new_id|new_name|
+------+--------+
|     1|       A|
+------+--------+
```
#### drop
移除指定的列  
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.drop("id").show()
+----+
|name|
+----+
|   A|
+----+
```

#### transform
对当前的 DataFrame 作转换，根据传入的 DataFrame => DataFrame 函数，返回新的 DataFrame 
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.transform(_df => df.drop("id")).show
+----+
|name|
+----+
|   A|
+----+
```
#### map
对 DataFrame 的每一行 row 作转换, 入参是 row => row 的映射函数  
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.map(row => "prefix_" + row.getAs[String]("name")).show
+--------+
|   value|
+--------+
|prefix_A|
+--------+
``` 

#### flatMap
对 DataFrame 的 Array 列作转换, 并将每个元素展开成单独的行, 入参是 arrayItem => arrayItem 的映射函数

```  
scala> val df = spark.sql("SELECT ARRAY(1, 2, 3) as array_column")

scala> df.flatMap(row => row.getAs[Seq[Int]]("array_column").map(_ * 2)).show
+-----+
|value|
+-----+
|    2|
|    4|
|    6|
+-----+
```
#### toJSON
对 DataFrame 的每一行 row 转换为 JSON 字符串  
``` 
scala> val df = spark.sql("SELECT 1 AS id, 'A' AS name UNION SELECT 2, 'B'")
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.toJSON.show
+-------------------+
|              value|
+-------------------+
|{"id":1,"name":"A"}|
|{"id":2,"name":"B"}|
+-------------------+
``` 


### 分区转换
#### sortWithinPartitions
对每个 Partition 中的数据进行排序，与 SQL 中的 `sort by` 语义一致 

``` 
scala> case class Person(id: Int, name: String)
scala> val persons = (1 to 6).toList.map(x => Person(x, "Name" + x))
persons: List[Person] = List(Person(1,Name1), Person(2,Name2), Person(3,Name3), Person(4,Name4), Person(5,Name5), Person(6,Name6))

scala> val df = sc.parallelize(persons, 2).toDF
df: org.apache.spark.sql.DataFrame = [id: int, name: string ... 1 more field]

scala> val sortedDF = df.sortWithinPartitions(df("id").desc)
sortedDF: org.apache.spark.sql.Dataset[org.apache.spark.sql.Row] = [id: int, name: string]

scala> sortedDF.withColumn("partition_id", org.apache.spark.sql.functions.spark_partition_id()).show
+---+-----+------------+
| id| name|partition_id|
+---+-----+------------+
|  3|Name3|           0|
|  2|Name2|           0|
|  1|Name1|           0|
|  6|Name6|           1|
|  5|Name5|           1|
|  4|Name4|           1|
+---+-----+------------+
```
#### mapPartitions
对 DataFrame 的每一个分区做转换操作，每个分区中的记录被封装成一个迭代器，因此这个转换函数应是 iterator => iterator 的映射
``` 
scala> case class Person(id: Int, name: String)

scala> val df =  spark.createDataFrame((1 to 6).toList.map(x => Person(x, "Name" + x)))
df: org.apache.spark.sql.DataFrame = [id: int, name: string ... 1 more field]

scala> val transformed = df.mapPartitions{ iter => val salt = "abcd_"; iter.map( row => salt + row.getAs("name")) }
transformed: org.apache.spark.sql.Dataset[String] = [value: string]

scala> transformed.withColumn("partition_id", org.apache.spark.sql.functions.spark_partition_id()).show
+----------+------------+
|     value|partition_id|
+----------+------------+
|abcd_Name1|           0|
|abcd_Name2|           1|
|abcd_Name3|           2|
|abcd_Name4|           3|
|abcd_Name5|           4|
|abcd_Name6|           5|
+----------+------------+
```

#### repartition
调整 DataFrame 的分区到目标数量，与 [RDD - repartition](spark-rdd.md#repartition) 的行为一致  
#### coalesce
减少 DataFrame 的分区到目标数量，与 [RDD - coalesce](spark-rdd.md#coalesce) 的行为一致
#### repartitionByRange
调整 DataFrame 的分区到目标数量，对数据进行随机重新分布，会产生 Shuffle，重分布的过程将按指定列进行区间采样并进行区间排序（默认升序，空值优先），
因为采样可能返回不同的结果，故多次 repartitionByRange 的最终结果有可能不一致
``` 
scala> case class Person(id: Int, name: String)

scala> val df =  spark.createDataFrame((1 to 6).toList.map(x => Person(x, "Name" + x)))
df: org.apache.spark.sql.DataFrame = [id: int, name: string ... 1 more field]

scala> df.repartitionByRange(3, $"id").withColumn("partition_id", org.apache.spark.sql.functions.spark_partition_id()).show
+---+-----+------------+
| id| name|partition_id|
+---+-----+------------+
|  1|Name1|           0|
|  2|Name2|           0|
|  3|Name3|           1|
|  4|Name4|           1|
|  5|Name5|           2|
|  6|Name6|           2|
+---+-----+------------+
scala> df.repartitionByRange(3, $"id".desc).withColumn("partition_id", org.apache.spark.sql.functions.spark_partition_id()).show
+---+-----+------------+
| id| name|partition_id|
+---+-----+------------+
|  5|Name5|           0|
|  6|Name6|           0|
|  3|Name3|           1|
|  4|Name4|           1|
|  1|Name1|           2|
|  2|Name2|           2|
+---+-----+------------+
```


### 集合运算
#### join
将当前 DataFrame 与另一个 DataFrame 关联，需要自定关联类型，默认为 Inner
##### Inner Join
将当前 DataFrame 与另外的 DataFrame 进行内关联, 结果集中仅包含左右 DataFrame 中的能匹配上的记录, 相同关联键存在重复数据时，将返回其笛卡尔积   
joinType 为 `inner` 即表示 Inner Join
```
scala> case class Person(id: Int, name: String)

scala> val df1 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(3, "Name3")))
df1: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> val df2 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(2, "Name22"), Person(4, "Name4")))

scala> df1.join(df2, "id", joinType="inner").show
+---+-----+------+
| id| name|  name|
+---+-----+------+
|  1|Name1| Name1|
|  2|Name2| Name2|
|  2|Name2|Name22|
+---+-----+------+

scala> df1.join(df2, df1("id") === df2("id")).show
+---+-----+---+------+
| id| name| id|  name|
+---+-----+---+------+
|  1|Name1|  1| Name1|
|  2|Name2|  2| Name2|
|  2|Name2|  2|Name22|
+---+-----+---+------+
```

##### Full Join
将当前 DataFrame 与另外的 DataFrame 进行全关联, 结果集中将包含左右 DataFrame 中的全部记录，匹配不到的数据置为空  
joinType 为 `outer`, `full`, `fullouter`, `full_outer` 均表示 Full Join  
``` 
scala> case class Person(id: Int, name: String)

scala> val df1 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(3, "Name3")))
df1: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> val df2 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(2, "Name22"), Person(4, "Name4")))

scala> df1.join(df2, "id", joinType="full").show
+---+-----+------+
| id| name|  name|
+---+-----+------+
|  1|Name1| Name1|
|  2|Name2| Name2|
|  2|Name2|Name22|
|  3|Name3|  NULL|
|  4| NULL| Name4|
+---+-----+------+
```
##### Left Join
将当前 DataFrame 与另外的 DataFrame 进行左关联, 结果集中仅包含左 DataFrame 中的全部记录，右 DataFrame 中匹配不到的数据置为空
joinType 为 `leftouter`, `left`, `left_outer` 均表示 Left Join
``` 
scala> case class Person(id: Int, name: String)

scala> val df1 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(3, "Name3")))
df1: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> val df2 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(2, "Name22"), Person(4, "Name4")))

scala> df1.join(df2, "id", joinType="left").show
+---+-----+------+
| id| name|  name|
+---+-----+------+
|  1|Name1| Name1|
|  2|Name2|Name22|
|  2|Name2| Name2|
|  3|Name3|  NULL|
+---+-----+------+
``` 
##### Right Join
将当前 DataFrame 与另外的 DataFrame 进行右关联, 结果集中仅包含右 DataFrame 中的全部记录，左 DataFrame 中匹配不到的数据置为空
joinType 为 `rightouter`, `right`, `right_outer` 均表示 Right Join
``` 
scala> case class Person(id: Int, name: String)

scala> val df1 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(3, "Name3")))
df1: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> val df2 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(2, "Name22"), Person(4, "Name4")))

scala> df1.join(df2, "id", joinType="right").show
+---+-----+------+
| id| name|  name|
+---+-----+------+
|  1|Name1| Name1|
|  2|Name2| Name2|
|  2|Name2|Name22|
|  4| NULL| Name4|
+---+-----+------+
``` 
##### Semi Join  
将当前 DataFrame 与另外的 DataFrame 进行(左)半关联, 结果集中仅包含左右 DataFrame 中的能匹配上的记录，并且右表中存在重复时，仅返回第一条记录。 
joinType 为 `leftsemi`, `semi`, `left_semi` 均表示 Semi Join
``` 
scala> case class Person(id: Int, name: String)

scala> val df1 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(3, "Name3")))
df1: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> val df2 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(2, "Name22"), Person(4, "Name4")))

scala> df1.join(df2, "id", joinType="semi").show
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
+---+-----+
```
##### Anti Join  
将当前 DataFrame 与另外的 DataFrame 进行(左)反关联, 结果集中仅包含左 DataFrame 中与右 DataFrame 匹配不上的记录。 相当于用右 DF 对左 DF 求差集。  
joinType 为 `leftanti`, `anti`, `left_anti` 均表示 Anti Join
``` 
scala> case class Person(id: Int, name: String)

scala> val df1 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(3, "Name3")))
df1: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> val df2 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(2, "Name22"), Person(4, "Name4")))

scala> df1.join(df2, "id", joinType="full").show
```
#### crossJoin
将当前 DataFrame 与另外的 DataFrame 进行关联, 返回笛卡尔积  
``` 
scala> case class Person(id: Int, name: String)

scala> val df1 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(3, "Name3")))
df1: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> val df2 = spark.createDataFrame(Seq(Person(1, "Name1"), Person(2, "Name2"), Person(2, "Name22"), Person(4, "Name4")))

scala> df1.crossJoin(df2).show
+---+-----+---+------+
| id| name| id|  name|
+---+-----+---+------+
|  1|Name1|  1| Name1|
|  2|Name2|  1| Name1|
|  3|Name3|  1| Name1|
|  1|Name1|  2| Name2|
|  2|Name2|  2| Name2|
|  3|Name3|  2| Name2|
|  1|Name1|  2|Name22|
|  2|Name2|  2|Name22|
|  3|Name3|  2|Name22|
|  1|Name1|  4| Name4|
|  2|Name2|  4| Name4|
|  3|Name3|  4| Name4|
+---+-----+---+------+
```
#### limit  
取当前 DataFrame 的前 n 条记录，返回一个新的 DataFrame  
```  
scala> case class Person(id: Int, name: String)
scala> val df =  spark.createDataFrame((1 to 6).toList.map(x => Person(x, "Name" + x)))

scala> df.limit(3).show
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+
```
#### offset
跳过当前 DataFrame 的前 n 条记录，返回一个新的 DataFrame  
```  
scala> case class Person(id: Int, name: String)
scala> val df =  spark.createDataFrame((1 to 6).toList.map(x => Person(x, "Name" + x)))

scala> df.offset(2).limit(3).show
+---+-----+
| id| name|
+---+-----+
|  3|Name3|
|  4|Name4|
|  5|Name5|
+---+-----+
```
#### union
两个 DataFrame 求并集，按列的位置进行合并，不会对结果去重，返回一个新的 DataFrame  
```  
scala> case class Person(id: Int, name: String)
scala> val df1 =  spark.createDataFrame((1 to 3).toList.map(x => Person(x, "Name" + x)))

scala> val df2 =  spark.createDataFrame((3 to 5).toList.map(x => Person(x, "Name" + x)))

scala> df1.union(df2).show()
+---+-----+
| id| name|
+---+-----+
|  3|Name3|
|  4|Name4|
|  5|Name5|
+---+-----+
```
#### unionAll
与 [union](#union) 的行为一致，提供与 SQL 语义一致的同名算子
#### unionByName
两个 DataFrame 求并集，按列的名称进行合并，不会对结果去重，返回一个新的 DataFrame  

``` 
scala> case class Person(id: Int, name: String)
scala> val df1 =  spark.createDataFrame((1 to 3).toList.map(x => Person(x, "Name" + x)))

scala> val df2 =  spark.createDataFrame((3 to 5).toList.map(x => Person(x, "Name" + x))).to

scala> df1.union(df2).show()
+---+-----+
| id| name|
+---+-----+
|  3|Name3|
|  4|Name4|
|  5|Name5|
+---+-----+
```
#### intersect
返回两个 DataFrame 的交集，会对结果去重  
``` 
scala> case class Person(id: Int, name: String)
scala> val df1 =  spark.createDataFrame(List(1, 2, 3, 3, 3).map(x => Person(x, "Name" + x)))

scala> val df2 =  spark.createDataFrame(List(3, 3, 4, 5).map(x => Person(x, "Name" + x)))

scala> df1.intersect(df2).show()
+---+-----+
| id| name|
+---+-----+
|  3|Name3|
+---+-----+
```
#### intersectAll
返回两个 DataFrame 的交集，不会对结果去重  
``` 
scala> case class Person(id: Int, name: String)
scala> val df1 =  spark.createDataFrame(List(1, 2, 3, 3, 3).map(x => Person(x, "Name" + x)))

scala> val df2 =  spark.createDataFrame(List(3, 3, 4, 5).map(x => Person(x, "Name" + x)))

scala> df1.intersectAll(df2).show()
+---+-----+
| id| name|
+---+-----+
|  3|Name3|
|  3|Name3|
+---+-----+

```
#### except
返回两个 DataFrame 的差集，不会对结果去重
``` 
scala> case class Person(id: Int, name: String)
scala> val df1 =  spark.createDataFrame(List(1, 2, 2, 3, 3).map(x => Person(x, "Name" + x)))

scala> val df2 =  spark.createDataFrame(List(3, 4, 5).map(x => Person(x, "Name" + x)))

scala> df1.except(df2).show()
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
+---+-----+

```
#### exceptAll
``` 
scala> case class Person(id: Int, name: String)
scala> val df1 =  spark.createDataFrame(List(1, 2, 2, 3, 3).map(x => Person(x, "Name" + x)))

scala> val df2 =  spark.createDataFrame(List(3, 4, 5).map(x => Person(x, "Name" + x)))

scala> df1.exceptAll(df2).show()
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  2|Name2|
|  3|Name3|
+---+-----+
```
#### sample
对 DataFrame 进行采样，返回包含样本记录的新 DataFrame, 参数 fraction 不代表精确的比例，仅代表每条记录被命中的概率  
```  
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame((1 to 100).toList.map(x => Person(x, "Name" + x)))

scala> df.sample(0.05).show()
+---+------+
| id|  name|
+---+------+
|  1| Name1|
| 17|Name17|
| 21|Name21|
| 90|Name90|
+---+------+
```
#### randomSplit
将 DataFrame 切分成一组 DataFrame 的 Array, 切分成多少组由权重 weights 的数组大小决定, 权重不代表精确的比例，仅代表每条记录被命中的概率  
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame((1 to 100).toList.map(x => Person(x, "Name" + x)))

scala> val splitedDFs = df.randomSplit(Array(0.2, 0.8))
splitedDFs: Array[org.apache.spark.sql.Dataset[org.apache.spark.sql.Row]] = Array([id: int, name: string], [id: int, name: string])

scala> splitedDFs.map(_.count)
res0: Array[Long] = Array(16, 84)
```
#### randomSplitAsList
将 DataFrame 切分成一组 DataFrame 的 java List, 切分成多少组由权重 weights 的数组大小决定, 并要求传入种子值 seed。权重不代表精确的比例，仅代表每条记录被命中的概率
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame((1 to 100).toList.map(x => Person(x, "Name" + x)))

scala> val splitedDFs = df.randomSplitAsList(weights=Array(0.2, 0.8), seed=scala.util.Random.nextLong)
splitedDFs: java.util.List[org.apache.spark.sql.Dataset[org.apache.spark.sql.Row]] = [[id: int, name: string], [id: int, name: string]]

scala> splitedDFs.asScala.map(_.count)
res0: scala.collection.mutable.Buffer[Long] = ArrayBuffer(14, 86)
```

### 聚合操作
#### groupBy
将 DataFrame 按指定的列进行分组，返回一个 RelationalGroupedDataset，以便进行后续的聚合操作  
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 1, 2, 2, 2).map(x => Person(x, "Name" + x)))

scala> val groupedDF = df.groupBy(df("id"))
groupedDF: org.apache.spark.sql.RelationalGroupedDataset = RelationalGroupedDataset: [grouping expressions: [id: int], value: [id: int, name: string], type: GroupBy]

scala> groupedDF.count.show
+---+-----+
| id|count|
+---+-----+
|  1|    2|
|  2|    3|
+---+-----+
```

#### agg
将 DataFrame 视为一个整体进行聚合操作  
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 1, 2, 2, 2).map(x => Person(x, "Name" + x)))

scala> df.agg(max("id")).show
+-------+
|max(id)|
+-------+
|      2|
+-------+

scala> df.agg(Map("id" -> "count", "name" -> "max")).show
+---------+---------+
|count(id)|max(name)|
+---------+---------+
|        5|    Name2|
+---------+---------+
```

#### rollup
将 DataFrame 按指定的列进行多维逐级聚合操作，类似与 [groupBy](#groupby)，同样返回一个 RelationalGroupedDataset，以便进行后续的聚合操作。  
但是会以指定的列逐级分组，即： 假设给定维度为 (colA, colB, colC)，则会分别按照如下组合对数据进行汇总：  
- colA, colB, colC
- colA, colB
- colA
- None
```  
scala> case class Person(id: Int, name: String, age: Int)
scala> val df = spark.createDataFrame(List(1, 1, 2, 2, 2).map(x => Person(x, "Name" + x, 50)))

scala> df.rollup("id", "name", "age").count().show
+----+-----+----+-----+
|  id| name| age|count|
+----+-----+----+-----+
|   1|Name1|  50|    2|
|   2|Name2|  50|    3|
|   1|Name1|NULL|    2|
|   2|Name2|NULL|    3|
|   1| NULL|NULL|    2|
|   2| NULL|NULL|    3|
|NULL| NULL|NULL|    5|
+----+-----+----+-----+

```

#### cube
将 DataFrame 按指定的列创建一个多维立方体，类似与 [groupBy](#groupby)，同样返回一个 RelationalGroupedDataset，以便进行后续的聚合操作。  
但是会以指定的列按所有的维度组合进行分组，多维立方体(cube)即： 假设给定维度为 (colA, colB, colC)，则会分别按照如下组合对数据进行汇总：
- colA, colB, colC
- colA, colB
- colA, colC
- colB, colC
- colA
- colB
- colC
- None
```  
scala> case class Person(id: Int, name: String, age: Int)
scala> val df = spark.createDataFrame(List(1, 1, 2, 2, 2).map(x => Person(x, "Name" + x, 50)))

scala> df.cube("id", "name", "age").count().show
+----+-----+----+-----+
|  id| name| age|count|
+----+-----+----+-----+
|   1|Name1|  50|    2|
|   2|Name2|  50|    3|
|   1|Name1|NULL|    2|
|   2|Name2|NULL|    3|
|   1| NULL|  50|    2|
|   2| NULL|  50|    3|
|NULL|Name1|  50|    2|
|NULL|Name2|  50|    3|
|   1| NULL|NULL|    2|
|   2| NULL|NULL|    3|
|NULL|Name1|NULL|    2|
|NULL|Name2|NULL|    3|
|NULL| NULL|  50|    5|
|NULL| NULL|NULL|    5|
+----+-----+----+-----+

```
#### groupingSets  Spark 4.0 + 
todo 待补充

#### distinct
对 DataFrame 进行去重，完全重复的数据将仅保留一条
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(Person(1, "Name1"), Person(2, "Name2"), Person(2, "Name2"), Person(3, "Name3"), Person(3, "Name333")))
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.distinct.show
+---+-------+
| id|   name|
+---+-------+
|  1|  Name1|
|  2|  Name2|
|  3|  Name3|
|  3|Name333|
+---+-------+
```
#### dropDuplicates
对 DataFrame 按指定的列进行去重，相同列的重复记录将仅保留第一条记录
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(Person(1, "Name1"), Person(2, "Name2"), Person(2, "Name2"), Person(3, "Name3"), Person(3, "Name333")))
df: org.apache.spark.sql.DataFrame = [id: int, name: string]

scala> df.dropDuplicates("id").show
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+
```

#### describe
对 DataFrame 的数据进行描述，返回一些常用的统计指标  
``` 
scala> case class Person(id: Int, name: String, age: Int)
scala> val df = spark.createDataFrame(List(1, 1, 2, 2, 2).map(x => Person(x, "Name" + x, 50)))

scala> df.describe().show
+-------+------------------+-----+----+
|summary|                id| name| age|
+-------+------------------+-----+----+
|  count|                 5|    5|   5|
|   mean|               1.6| NULL|50.0|
| stddev|0.5477225575051661| NULL| 0.0|
|    min|                 1|Name1|  50|
|    max|                 2|Name2|  50|
+-------+------------------+-----+----+
```

#### summary 
与 [describe](#describe) 类似，在其基础上增加了 `p25`, `p50`, `p75` 等指标  

``` 
scala> case class Person(id: Int, name: String, age: Int)
scala> val df = spark.createDataFrame(List(1, 1, 2, 2, 2).map(x => Person(x, "Name" + x, 50)))

scala> df.summary().show
+-------+------------------+-----+----+
|summary|                id| name| age|
+-------+------------------+-----+----+
|  count|                 5|    5|   5|
|   mean|               1.6| NULL|50.0|
| stddev|0.5477225575051661| NULL| 0.0|
|    min|                 1|Name1|  50|
|    25%|                 1| NULL|  50|
|    50%|                 2| NULL|  50|
|    75%|                 2| NULL|  50|
|    max|                 2|Name2|  50|
+-------+------------------+-----+----+
```

## Action 算子
### 转换为内存集合
#### reduce
对 DataFrame 进行合并操作, 所有记录按照用户指定的 (left, right) => result 函数从左到右进行合并, 返回一个 Java 集合  
如下面的例子中，仅保留最大的 id 的第一条记录
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(Person(1, "Name1"), Person(2, "Name2"), Person(2, "Name2"), Person(3, "Name3"), Person(3, "Name333")))

scala> df.reduce((row_left, row_right) => if (row_right.getAs[Int]("id") > row_left.getAs[Int]("id")) row_right else row_left)
res0: org.apache.spark.sql.Row = [3,Name3]
```
#### foreach
遍历 DataFrame 中的每一条记录，根据提供的 row => Unit 函数，将记录写入外部系统，或打印到控制台，或添加到其他 Java 集合中等
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2).map(x => Person(x, "Name" + x)))

scala> df.foreach(row => println(s"id: ${row.get(0)}, name: ${row.get(1)}"))
id: 1, name: Name1
id: 2, name: Name2
```
#### foreachPartition
遍历 DataFrame 中的每一个 partition，每个 partition 中的 row 被封装在一个 Iterator 中， 根据提供的 iterator[Row] => Unit 函数，将记录写入外部系统，或打印到控制台，或添加到其他 Java 集合中等
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2).map(x => Person(x, "Name" + x))).repartition(2)

scala> df.foreachPartition{ (iter: Iterator[org.apache.spark.sql.Row]) => 
  val partitionId = org.apache.spark.TaskContext.getPartitionId 
  iter.foreach(row => println(s"partition: ${partitionId}, id: ${row.get(0)}, name: ${row.get(1)}"))
}
partition: 0, id: 1, name: Name1
partition: 1, id: 2, name: Name2
```
#### isEmpty
判断 DataFrame 是否为空, 返回 true 或 false  

``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2).map(x => Person(x, "Name" + x)))

scala> df.isEmpty
res0: Boolean = false
```
#### head
返回 DataFrame 的前 n 条记录，默认为 n = 1  
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.head
res0: org.apache.spark.sql.Row = [1,Name1]

scala> df.head(2)
res1: Array[org.apache.spark.sql.Row] = Array([1,Name1], [2,Name2])
```
#### first
与 [head(1)](#head) 语义一致  

#### take
与 [head(n)](#head) 语义一致
#### tail
返回 DataFrame 的后 n 条记录
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.tail(2)
res0: Array[org.apache.spark.sql.Row] = Array([2,Name2], [3,Name3])
```
#### takeAsList
与 [take](#take) 相似，只是返回返回一个 Java 的 List  
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.takeAsList(2)
res1: java.util.List[org.apache.spark.sql.Row] = [[1,Name1], [2,Name2]]
```
#### collect
将 DataFrame 的所有记录收集起来，返回一个 Java 的 Array 集合到 Driver 端，避免对大数据集使用此操作，以防止 Driver 端 OOM   
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.collect
res0: Array[org.apache.spark.sql.Row] = Array([1,Name1], [2,Name2], [3,Name3])
```

#### collectAsList
与 [collect](#collect) 相似，只是返回一个 Java 的 List，避免对大数据集使用此操作，以防止 Driver 端 OOM  
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.collect
res0: java.util.List[org.apache.spark.sql.Row] = [[1,Name1], [2,Name2], [3,Name3]]
```

#### toLocalIterator
将 DataFrame 的所有记录封装成 Java 的迭代器， Driver 端消耗的内存将与最大的 partition 消耗的内存一致  
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> val rowIterator = df.toLocalIterator
rowIterator: java.util.Iterator[org.apache.spark.sql.Row] = IteratorWrapper(<iterator>)

scala> rowIterator.next
res0: org.apache.spark.sql.Row = [1,Name1]
```
#### count 
返回 DataFrame 的总记录数 
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.count
res0: Long = 3
```
### createOrReplaceGlobalTempView
与 [createGlobalTempView](#createGlobalTempView) 类似，只是视图存在时将覆盖原有视图

### 写入外部算子
#### write v1
DataFrame.write 方法将返回一个 DataFrameWriter 实例，包含以下方法
##### insertInto
将 DataFrame 按写入指定的表中，写入操作是基于列的顺序的，因此要求目标表结构必须与 DataFrame 的 Schema 一致  
不会自动创建表，可根据 [mode](#mode-) 参数来选择写入模式，默认为追加记录  
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> spark.sql("create table test_table__insert_into(id int, name string)")
res0: org.apache.spark.sql.DataFrame = []

scala> df.write.mode("append").insertInto("test_table__insert_into")
scala> df.write.mode("append").insertInto("test_table__insert_into")

scala> spark.table("test_table__insert_into").show()
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  1|Name1|
|  2|Name2|
|  2|Name2|
|  3|Name3|
|  3|Name3|
+---+-----+

scala> df.write.mode("overwrite").insertInto("test_table__insert_into")

scala> spark.table("test_table__insert_into").show()
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+

scala> df.select("name", "id").write.insertInto("test_table__insert_into")
org.apache.spark.sql.AnalysisException: [INCOMPATIBLE_DATA_FOR_TABLE.CANNOT_SAFELY_CAST] Cannot write incompatible data for the table `spark_catalog`.`default`.`test_person`: Cannot safely cast `id` "STRING" to "INT".
  at org.apache.spark.sql.errors.QueryCompilationErrors$.incompatibleDataToTableCannotSafelyCastError(QueryCompilationErrors.scala:2216)
```
##### saveAsTable
将 DataFrame 按写入指定的表中，写入操作是基于列名的，因此不会对 DataFrame 的列顺序有严格要求，只要列存在即可  
表不存在时将自动创建，可根据 [mode](#mode-) 参数来选择写入模式，默认为表存在时报错  

``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.write.mode("overwrite").saveAsTable("test_person_save_as_table")

scala> spark.table("test_person_save_as_table").show()
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+

scala> df.select("name", "id").write.mode("append").saveAsTable("test_person_save_as_table")
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  1|Name1|
|  2|Name2|
|  2|Name2|
|  3|Name3|
|  3|Name3|
+---+-----+
```
##### jdbc
将 DataFrame 按 jdbc 协议写入外部数据库，如 MySQL/Postgres 等, 等效于 [format](#format) 为 `jdbc` 时的 [save](#save) 操作   
表不存在时将自动创建，可根据 [mode](#mode-) 参数来选择写入模式，默认为表存在时报错  
本例子中需要使用 MySQL 驱动来连接本地的 MySQL 数据库，因此需要将相应的驱动包加入 classpath，比如：  
```shell
spark-shell --packages "mysql:mysql-connector-java:8.0.28" 
```

``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> val connectionProperties = new java.util.Properties()
scala> connectionProperties.put("user", "root")
scala> connectionProperties.put("password", "123456")
scala> connectionProperties.put("driver", "com.mysql.jdbc.Driver")

scala> df.write.jdbc(
  url="jdbc:mysql://localhost:3306/test?createDatabaseIfNotExist=true", 
  table="test_table__jdbc",
  connectionProperties=connectionProperties
)

scala> spark.read.jdbc(
  url="jdbc:mysql://localhost:3306/test?createDatabaseIfNotExist=true", 
  table="test_table__jdbc",
  properties=connectionProperties
).show
+---+-----+
| id| name|
+---+-----+
|  2|Name2|
|  1|Name1|
|  3|Name3|
+---+-----+
```
##### save
将 DataFrame 保存到外部存储系统中, 是 [jdbc](#jdbc) 以及各个写文件操作（如 [json](#json), [csv](#csv) 等）的统一抽象 
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> { 
df.write.format("jdbc")
  .option("url", "jdbc:mysql://localhost:3306/test?createDatabaseIfNotExist=true")
  .option("driver", "com.mysql.jdbc.Driver")
  .option("user", "root")
  .option("password", "123456")
  .option("dbtable", "test_table__jdbc_save")
  .save
}

scala> { 
spark.read.format("jdbc")
  .option("url", "jdbc:mysql://localhost:3306/test?createDatabaseIfNotExist=true")
  .option("driver", "com.mysql.jdbc.Driver")
  .option("user", "root")
  .option("password", "123456")
  .option("dbtable", "test_table__jdbc_save")
  .load
}.show
+---+-----+
| id| name|
+---+-----+
|  2|Name2|
|  3|Name3|
|  1|Name1|
+---+-----+

scala> df.write.mode("overwrite").format("csv").option("header", "true").save("hdfs:///test_write/test_csv")

scala> spark.read.format("csv").option("header", "true").load("hdfs:///test_write/test_csv").show
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+
```
##### json
等同于 [format](#format) 为 `json` 时的 [save](#save) 操作  
##### parquet
等同于 [format](#format) 为 `parquet` 时的 [save](#save) 操作
##### orc 
等同于 [format](#format) 为 `orc` 时的 [save](#save) 操作
##### text
等同于 [format](#format) 为 `text` 时的 [save](#save) 操作
##### csv
等同于 [format](#format) 为 `csv` 时的 [save](#save) 操作
##### xml
等同于 [format](#format) 为 `xml` 时的 [save](#save) 操作
##### mode 
指定写入目标资源（表或文件目录等）时的写入模式  
- Overwrite: 将目标资源的原有记录覆盖，saveMode 为 `overwrite` 即表示 Overwrite 语义
- Append: 向目标资源中追加记录，saveMode 为 `append` 即表示 Append 语义
- Ignore: 当目标资源已存在时，将不做任何操作，saveMode 为 `ingore` 即表示 Ignore 语义
- ErrorIfExists: 当目标资源已存在时，将抛出异常，saveMode 为 `error`, `errorifexists`, `default` 均表示 ErrorIfExists 语义

#### writeTo v2
DataFrame.writeTo(tableName) 方法将返回一个 DataFrameWriterV2 实例，用于操作 V2 的表（如 DataLake：Iceberg 等） 
本例子中将采用 Spark Tests 中常用的 InMemoryTable，需先下载 [spark-catalyst_2.12-3.5.1-tests.jar](https://repo1.maven.org/maven2/org/apache/spark/spark-catalyst_2.12/3.5.1/spark-catalyst_2.12-3.5.1-tests.jar)  
启动 spark-shell  
```  
spark-shell --jars spark-catalyst_2.12-3.5.1-tests.jar
```
启动后注册 InMemoryTableCatalog 后，即可正常操作 InMemoryTable  
```
spark.conf().set("spark.sql.catalog.in_mem_catalog", "org.apache.spark.sql.connector.catalog.InMemoryTableCatalog")
```
##### create
将当前 DataFrame 创建为指定名称的表，表存在时将报错 
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.writeTo("in_mem_catalog.test_write_to__create").create()

scala> spark.table("in_mem_catalog.test_write_to__create").show 
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+

scala>  df.writeTo("in_mem_catalog.test_write_to__create").create()
org.apache.spark.sql.catalyst.analysis.TableAlreadyExistsException: [TABLE_OR_VIEW_ALREADY_EXISTS] Cannot create table or view `test_write_to__create` because it already exists.
```
##### replace
用当前 DataFrame 将指定名称的替换，表不存在时将报错  
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.writeTo("in_mem_catalog.test_write_to__replace").replace()
org.apache.spark.sql.catalyst.analysis.CannotReplaceMissingTableException: [TABLE_OR_VIEW_NOT_FOUND] The table or view `test_write_to__replace` cannot be found.

scala> df.writeTo("in_mem_catalog.test_write_to__replace").create()
scala> spark.table("in_mem_catalog.test_write_to__replace").show 
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+

scala> df.select("name", "id").writeTo("in_mem_catalog.test_write_to__replace").replace()
scala> spark.table("in_mem_catalog.test_write_to__replace").show
+-----+---+
| name| id|
+-----+---+
|Name1|  1|
|Name2|  2|
|Name3|  3|
+-----+---+
```

##### createOrReplace
[create](#create) 和 [replace](#replace) 的幂等操作，表不存在时创建，表存在时则替换   
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.writeTo("in_mem_catalog.test_write_to__create_or_replace").createOrReplace()

scala> spark.table("in_mem_catalog.test_write_to__create_or_replace").show 
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+

scala> df.select("name", "id").writeTo("in_mem_catalog.test_write_to__create_or_replace").createOrReplace()
scala> spark.table("in_mem_catalog.test_write_to__create_or_replace").show
+-----+---+
| name| id|
+-----+---+
|Name1|  1|
|Name2|  2|
|Name3|  3|
+-----+---+
```

##### append 
将 DataFrame 中的记录追加写入到目标表中，写入操作是基于列名的，因此不会对 DataFrame 的列顺序有严格要求，只要列存在即可  
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.writeTo("in_mem_catalog.test_write_to__append").createOrReplace()

scala> spark.table("in_mem_catalog.test_write_to__append").show 
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+

scala> df.select("name", "id").writeTo("in_mem_catalog.test_write_to__append").append()
scala> spark.table("in_mem_catalog.test_write_to__append").show
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+

```
##### overwrite
用当前 DataFrame 中的记录将目标表按条件覆盖，匹配的行将被覆盖，其余行将会追加到目标表中  
写入操作是基于列名的，因此不会对 DataFrame 的列顺序有严格要求，只要列存在即可  
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> spark.sql("CREATE TABLE in_mem_catalog.test_write_to__overwrite (id int, name string) USING foo PARTITIONED BY (id)")
scala> df.writeTo("in_mem_catalog.test_write_to__overwrite").append

scala> spark.table("in_mem_catalog.test_write_to__overwrite").show
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+

scala> val df2 = spark.createDataFrame(List(Person(3, "Name333"), Person(4, "Name444")))
scala> df2.writeTo("in_mem_catalog.test_write_to__overwrite").overwrite($"id" === 3)

scala> spark.table("in_mem_catalog.test_write_to__overwrite").show
+---+-------+
| id|   name|
+---+-------+
|  4|Name444|
|  1|  Name1|
|  3|Name333|
|  2|  Name2|
+---+-------+

scala> df2.writeTo("in_mem_catalog.test_write_to__overwrite").overwrite(org.apache.spark.sql.functions.lit(true))

scala> spark.table("in_mem_catalog.test_write_to__overwrite").show
+---+-------+
| id|   name|
+---+-------+
|  4|Name444|
|  3|Name333|
+---+-------+
```
##### overwritePartitions
用当前 DataFrame 对目标表进行分区覆盖操作，匹配的分区将被覆盖  
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 1, 1, 2, 3).map(x => Person(x, "Name" + x)))

scala> spark.sql("CREATE TABLE in_mem_catalog.test_write_to__overwrite_partitions (id int, name string) USING foo PARTITIONED BY (id)")
scala> df.writeTo("in_mem_catalog.test_write_to__overwrite_partitions").append

scala> spark.table("in_mem_catalog.test_write_to__overwrite_partitions").show
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+

scala> val df2 = spark.createDataFrame(List(Person(1, "Name111"), Person(4, "Name444")))
scala> df2.writeTo("in_mem_catalog.test_write_to__overwrite_partitions").overwritePartitions

scala> spark.table("in_mem_catalog.test_write_to__overwrite_partitions").show
+---+-------+
| id|   name|
+---+-------+
|  4|Name444|
|  1|Name111|
|  3|  Name3|
|  2|  Name2|
+---+-------+
```

#### mergeInto spark 4.0 +
DataFrame.mergeInto 方法将返回一个 MergeIntoWriter 实例，包含以下方法
todo 待补充



## 控制算子
DataFrame 提供与 RDD 行为一致的控制算子如:
- [persist](spark-rdd.md#persist)  
- [cache](spark-rdd.md#cache)  
- [unpersist](spark-rdd.md#unpersist)  
- [checkpoint](spark-rdd.md#checkpoint)  
除了这些以外，还提供了一些创建 View 的控制类算子  
### createTempView   
为当前 DataFrame 创建临时视图，可用 SQL 语句对其进行访问，在当前 SparkSession 内有效，视图存在时将报错
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.createTempView("temp_view_person")

scala> spark.sql("SELECT * FROM temp_view_person").show
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+
scala> spark
res4: org.apache.spark.sql.SparkSession = org.apache.spark.sql.SparkSession@5f59d707

scala> val newSpark = spark.newSession
newSpark: org.apache.spark.sql.SparkSession = org.apache.spark.sql.SparkSession@1916f999

scala> newSpark.sql("SELECT * FROM temp_view_person").show
org.apache.spark.sql.catalyst.ExtendedAnalysisException: [TABLE_OR_VIEW_NOT_FOUND] The table or view `temp_view_person` cannot be found.
```
### createOrReplaceTempView
与 [createTempView](#createTempView-) 类似，只是视图存在时将覆盖原有视图
### createGlobalTempView
为当前 DataFrame 创建临时视图，可用 SQL 语句对其进行访问，在当前 Spark Application 内有效，视图存在时将报错
``` 
scala> case class Person(id: Int, name: String)
scala> val df = spark.createDataFrame(List(1, 2, 3).map(x => Person(x, "Name" + x)))

scala> df.createGlobalTempView("temp_view_person")

scala> spark.sql("SELECT * FROM global_temp.temp_view_person").show
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+

scala> spark
res4: org.apache.spark.sql.SparkSession = org.apache.spark.sql.SparkSession@5f59d707

scala> val newSpark = spark.newSession
newSpark: org.apache.spark.sql.SparkSession = org.apache.spark.sql.SparkSession@1916f999

scala> newSpark.sql("SELECT * FROM global_temp.temp_view_person").show
+---+-----+
| id| name|
+---+-----+
|  1|Name1|
|  2|Name2|
|  3|Name3|
+---+-----+
```

