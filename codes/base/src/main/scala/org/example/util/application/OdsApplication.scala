package org.example.util.application
import org.example.util.table.Table

abstract class OdsApplication extends SparkApplication {
  override val input: Set[Table] = null // todo ODS 类任务的输入应该如何？
}
