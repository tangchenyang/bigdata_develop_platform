import os.path

from pyspark import SparkConf
from pyspark.sql import SparkSession

from data_warehouse import DW_DIR

SPARK_COMPACT_VERSION = "3.5"  # todo move to a better place
ICEBERG_VERSION = "1.8.1"
SCALA_COMPACT_VERSION = "2.12"


def _build_dependency_coordinators():
    deps = [
        f"org.apache.iceberg:iceberg-spark-runtime-{SPARK_COMPACT_VERSION}_{SCALA_COMPACT_VERSION}:{ICEBERG_VERSION}"
    ]
    return ",".join(deps)


def create_spark_session():
    """
    """
    spark_conf = (
        SparkConf()
        .set("spark.jars.packages", _build_dependency_coordinators())
        .set("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .set("spark.sql.catalog.iceberg_catalog", "org.apache.iceberg.spark.SparkCatalog")
        .set("spark.sql.catalog.iceberg_catalog.type", "hadoop")
        .set("spark.sql.catalog.iceberg_catalog.warehouse", f"{DW_DIR}/iceberg_warehouse")
    )

    spark_session = (
        SparkSession.builder
        .config(conf=spark_conf)
        .master("local[*]")
        .getOrCreate()
    )
    return spark_session
