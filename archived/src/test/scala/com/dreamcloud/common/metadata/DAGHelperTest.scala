package com.dreamcloud.common.metadata

import com.dreamcloud.example.moutai.application.ads.AdsMoutai
import com.dreamcloud.example.moutai.application.dwd.{DwdMoutai, DwdMoutai1}
import org.scalatest.FunSuite

class DAGHelperTest extends FunSuite {

  test("print all nodes") {
    Metadata.register(DwdMoutai)
    Metadata.register(DwdMoutai1)
    Metadata.register(AdsMoutai)

    DAGHelper.initNodes()
//    DAGHelper.nodes.foreach(println)
    DAGHelper.drawDAG("test.png")
  }

}
