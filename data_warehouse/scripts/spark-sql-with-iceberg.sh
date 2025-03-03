
CURRENT_DIR=$( cd "$( dirname "$0" )" && pwd )
DW_DIR=$( cd "$CURRENT_DIR/.." && pwd)

spark-sql \
  --conf "spark.executor.memory=1g" \
  --conf "spark.driver.memory=1g" \
  --conf "spark.jars.packages=org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.8.1" \
  --conf "spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions" \
  --conf "spark.sql.catalog.iceberg_catalog=org.apache.iceberg.spark.SparkCatalog" \
  --conf "spark.sql.catalog.iceberg_catalog.type=hadoop" \
  --conf "spark.sql.catalog.iceberg_catalog.warehouse=${DW_DIR}/iceberg_warehouse" \
  --conf "spark.sql.defaultCatalog=iceberg_catalog"

