package com.dreamcloud.common

object LaunchMode extends Enumeration {
  type LaunchMode = Value

  val LOCAL: LaunchMode = Value
  val YARN_CLIENT: LaunchMode = Value
  val YARN_CLUSTER: LaunchMode = Value

  def defaultLaunchMode: LaunchMode = YARN_CLIENT
}
