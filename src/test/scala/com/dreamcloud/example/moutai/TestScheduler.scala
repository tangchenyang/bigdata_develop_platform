package com.dreamcloud.example.moutai

import com.dreamcloud.common.scheduler.ApplicationScheduler
import com.dreamcloud.example.moutai.application.dw.fact.DwFactMoutai


object TestScheduler extends App {
  ApplicationScheduler.register(DwFactMoutai)
  ApplicationScheduler.appSet.foreach(ap => println(ap.appName))
  ApplicationScheduler.allInputTables.foreach(table => println(table.tableName))
  ApplicationScheduler.allOutputTables.foreach(table => println(table.tableName))
}