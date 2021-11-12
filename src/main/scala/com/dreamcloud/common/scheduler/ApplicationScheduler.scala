package com.dreamcloud.common.scheduler

import com.dreamcloud.common.application.SparkApplication
import com.dreamcloud.common.table.Table

import scala.collection.mutable

object ApplicationScheduler {

  var appSet: mutable.Set[SparkApplication] = mutable.LinkedHashSet[SparkApplication]()

  def register(sparkApplication: SparkApplication): Unit = {
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
      .flatMap(x=> x.output)
  }
}
