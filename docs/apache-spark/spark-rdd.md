# RDD 简介
RDD(Resilient Distributed Dataset) - 弹性分布式数据集，是 Spark 用来并行操作跨节点数据的主要抽象  
**RDD的五大特性：**
1. 一组分区：每个RDD拥有一组partitions, 每个partition将由一个task来处理
2. 数据血缘：每个RDD记录了其依赖关系，可向上追溯父RDD
3. 计算函数：每个RDD拥有其转换函数，记录了其是怎样通过父RDD转换而来的
4. 分区器：每个RDD拥有一个Partitioner, 记录了其重新分区的规则
5. 数据本地性：移动计算优于移动数据，RDD会尽可能让计算task发生在离数据更近的地方


# 创建 RDD

# Transformation 算子

# Action 算子
