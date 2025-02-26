import os.path

from pyspark import SparkConf
from pyspark.sql import SparkSession

SPARK_COMPACT_VERSION = "3.5"  # todo move to a better place
ICEBERG_VERSION = "1.6.1"
SCALA_COMPACT_VERSION = "2.12"

PROJECT_DIR = os.path.abspath(__file__).split("bigdata_develop_platform")[0] + "bigdata_develop_platform" # todo
DW_DIR = os.path.join(PROJECT_DIR, "data_warehouse")

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
