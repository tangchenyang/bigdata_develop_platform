package com.dreamcloud.common.metadata

import guru.nidi.graphviz.attribute.Attributes.attr
import guru.nidi.graphviz.attribute.Style
import guru.nidi.graphviz.model.Factory.node
import guru.nidi.graphviz.model.{Factory, Node}
import org.apache.spark.internal.Logging

import scala.collection.mutable

object DAGHelper extends Logging {

  var nodes: mutable.Set[Node] = mutable.LinkedHashSet[Node]()

  def buildNode(from: String, to: String): Node = {
    node(from).link(
      Factory.to(node(to)).`with`(attr("weight", 5), Style.DASHED)
    )
  }
  def addSingleNode(node: Node): Unit = {
    logInfo(s"add node: $node")
    nodes += node
  }

  def initNodes() {
    val applications = Metadata.appSet
    applications.foreach { application =>
      application.input.foreach { inputTable =>
        addSingleNode( buildNode(from = inputTable.tableName, to = application.output.head.tableName))
      }
    }
  }

  def drawDAG(path: String) = {
    GraphvizHelper.draw(nodes.toList.sortWith(_.toString < _.toString).toSet, path)
  }

}
