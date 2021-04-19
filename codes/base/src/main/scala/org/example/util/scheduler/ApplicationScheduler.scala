package org.example.util.scheduler

import org.example.util.application.SparkApplication
import org.example.util.table.Table

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
