package org.example.util.scheduler

import org.example.util.application.SparkApplication
import scala.collection.mutable

object ApplicationScheduler {

  var appSet: mutable.Set[SparkApplication] = mutable.LinkedHashSet[SparkApplication]()

  def register(sparkApplication: SparkApplication): Unit = {
    appSet = appSet.+(sparkApplication)
  }

  def printAllDependencies() = {
    appSet
      .filter(_.input != null)
      .flatMap(_.input.map(_.tableName))
      .foreach(println)
  }
}
