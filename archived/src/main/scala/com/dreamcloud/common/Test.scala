package com.dreamcloud.common

import guru.nidi.graphviz.model.{Factory, Graph, MutableGraph}
import guru.nidi.graphviz.attribute._
import guru.nidi.graphviz.attribute.Attributes.attr
import guru.nidi.graphviz.attribute.Rank.RankDir.LEFT_TO_RIGHT
import guru.nidi.graphviz.model.Factory._

import java.io.File

object Test {
  def main(args: Array[String]): Unit = {
    import guru.nidi.graphviz.attribute.Font
    import guru.nidi.graphviz.attribute.Rank
    import guru.nidi.graphviz.attribute.Style
    import guru.nidi.graphviz.engine.Format
    import guru.nidi.graphviz.engine.Graphviz
    //## basic
    val g: Graph = Factory.graph("example1").directed
      .graphAttr.`with`(Rank.dir(LEFT_TO_RIGHT))
      .nodeAttr.`with`(Font.name("arial"))
      .linkAttr.`with`("class", "link-class")
      .`with`(
        node("a").`with`(Color.RED)
          .link(node("b")),
        node("b")
          .link(to(node("c")).`with`(attr("weight", 5), Style.DASHED))
      )

    Graphviz.fromGraph(g).height(100).render(Format.PNG).toFile(new File("example/ex1.png"))
  }

}
