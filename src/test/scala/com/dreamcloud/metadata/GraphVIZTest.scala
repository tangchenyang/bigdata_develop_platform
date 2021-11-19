package com.dreamcloud.metadata

import guru.nidi.graphviz.attribute.Attributes.attr
import guru.nidi.graphviz.attribute.Color
import guru.nidi.graphviz.attribute.Rank.RankDir.LEFT_TO_RIGHT
import guru.nidi.graphviz.model.Factory.{node, to}
import guru.nidi.graphviz.model.{Factory, Graph, Node}
import org.scalatest.FunSuite

import java.io.File

class GraphVIZTest extends FunSuite {

  test(" hello graphviz") {
    import guru.nidi.graphviz.attribute.Font
    import guru.nidi.graphviz.attribute.Rank
    import guru.nidi.graphviz.attribute.Style
    import guru.nidi.graphviz.engine.Format
    import guru.nidi.graphviz.engine.Graphviz


    /**
     * a -> d
     * b -> d
     * a -> c
     * c -> d
     * d -> f
     * a -> e
     * c -> e
     */

    def buildNode(from: String, to: String): Node = {
      node(from).link(
        Factory.to(node(to)).`with`(attr("weight", 5), Style.DASHED)
      )
    }
    val nodes = Set[Node](
      buildNode("a", "d"),
      buildNode("b", "d"),
      buildNode("a", "c"),
      buildNode("c", "d"),
      buildNode("d", "f"),
      buildNode("a", "e"),
      buildNode("c", "e"),
      buildNode("f", "e")
    ).toArray

    //## basic
    val g: Graph = Factory.graph("example1").directed
      .graphAttr.`with`(Rank.dir(LEFT_TO_RIGHT))
      .nodeAttr.`with`(Font.name("arial"))
      .linkAttr.`with`("class", "link-class")
      .`with`(
        nodes: _*
      )

    Graphviz.fromGraph(g)
            .width(2000)
            .height(1000)
      .render(Format.PNG)
      .toFile(new File("ex1.png"))
  }
}
