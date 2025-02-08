package com.dreamcloud.common.application

import com.dreamcloud.common.table.Table

abstract class OdsApplication extends SparkApplication {
  override val input: Set[Table] = null // todo ODS 类任务的输入应该如何？
}
