package org.example.util.application

import org.example.util.table.AdsTable

abstract class AdsApplication extends SparkApplication {
  override val output: Set[AdsTable]
}
