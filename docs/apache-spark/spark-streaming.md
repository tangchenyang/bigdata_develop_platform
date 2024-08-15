# Spark Streaming

## Spark Streaming 简介
_Spark Streaming 是 Spark 中的上一代流计算引擎，目前作为一个遗留系统，已经停止更新。如果想从零开始一个 Spark 流处理的应用，请使用 Spark Structured String, todo add link_  

Spark Streaming 是基于 Spark RDD API 抽象出来的流处理计算框架，核心思路是将无界的流数据按时间窗口切分成有界的数据集合，再交给 Spark 引擎对每个有界的数据集进行批处理操作。    
因此，Spark Streaming 并不是严格意义上的基于数据流的实时计算引擎，而是基于微批的准实时计算引擎，微批之间的间隔最低为1秒左右。但即便如此，也足以应对除了对大多数秒级或分钟级近实时计算的场景。  
## 创建 DStream 
## Transformation 算子
## Action 算子
## 控制算子 

