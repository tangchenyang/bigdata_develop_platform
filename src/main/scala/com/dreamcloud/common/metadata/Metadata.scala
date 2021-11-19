package com.dreamcloud.common.metadata

import com.dreamcloud.common.application.SparkApplication
import com.dreamcloud.common.table.Table
import org.apache.spark.internal.Logging

import scala.collection.mutable

/**
 * record metadata for all project .
 */
object Metadata extends Logging{

  var appSet: mutable.Set[SparkApplication] = mutable.LinkedHashSet[SparkApplication]()

  def register(sparkApplication: SparkApplication): Unit = {
    logInfo(s"register application ${sparkApplication.appName}")
    appSet = appSet.+(sparkApplication)
  }

  def allInputTables(): mutable.Set[Table] = {
    appSet
      .filter(_.input != null)
      .flatMap(_.input)
  }

  def allOutputTables(): mutable.Set[Table] = {
    appSet
      .filter(_.output != null)
      .flatMap(x => x.output)
  }
}
