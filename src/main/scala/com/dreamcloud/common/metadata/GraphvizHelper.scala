package com.dreamcloud.common.metadata

import guru.nidi.graphviz.attribute.Rank.RankDir.LEFT_TO_RIGHT
import guru.nidi.graphviz.attribute.{Font, Rank}
import guru.nidi.graphviz.engine.{Format, Graphviz}
import guru.nidi.graphviz.model.{Factory, Graph, Node}

import java.io.File

object GraphvizHelper {

  def draw(nodes: Set[Node], path: String) {

    val sortedNodes = nodes.toList.sortWith(_.name.toString < _.name.toString).toArray

    val g: Graph = Factory.graph("example1").directed
      .graphAttr.`with`(Rank.dir(LEFT_TO_RIGHT))
      .nodeAttr.`with`(Font.name("arial"))
      .linkAttr.`with`("class", "link-class")
      .`with`(
        sortedNodes: _*
      )

    Graphviz.fromGraph(g)
      .width(2000)
      .height(1000)
      .render(Format.PNG)
      .toFile(new File(path))
  }
}
