var width = window.innerWidth, height = window.innerHeight, sizeDivisor = 100 , nodePadding = 1.5

var svg = d3.select("body")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

var color = d3.scaleOrdinal(["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494", "#b3b3b3"]);

var simulation = d3.forceSimulation()
    .force("forceX", d3.forceX().strength(.2).x(width * .5))
    .force("forceY", d3.forceY().strength(.2).y(height * .5))
    .force("center", d3.forceCenter().x(width * .5).y(height * .5))
    .force("charge", d3.forceManyBody().strength(-100));

d3.csv("futaleufu_palabras.csv",types, function (error,graph){
  if(error) throw error;

//  graph= graph.sort(function(a,b){return b.size - a.size; }) ;
  simulation
    .nodes(graph)
    .force("collide", d3.forceCollide().strength(.5).radius(function(d){ return d.cantidad*10 + nodePadding; }).iterations(1))
    .on("tick", function(d){
      node
          .attr("cx", function(d){ return d.x; })
          .attr("cy", function(d){ return d.y; })
    });
    var node = svg.append("g")
        .attr("class", "node")
      .selectAll("g")
      .data(graph)
      .enter().append("circle")
        .attr("r", function(d) { return d.cantidad*10; })
        .attr("fill", function(d) { return color(d.palabra); })
        .text(function(d){return d.palabra})
        //.attr("cx", function(d){ return d.x; })
        //.attr("cy", function(d){ return d.y; })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));
    var texto = svg.append('g')
      .attr("class","node")
      .selectAll("text")
      .data(graph)
      .enter().append("text")
        .attr('x', function(d) {return d.x*2.5+350})
        .attr('y', function(d) {return d.y*2.5+350})
        .attr('fill','black')
        .text(function(d){return d.palabra})
});

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(.03).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(.03);
  d.fx = null;
  d.fy = null;
}

function types(d){
  d.gdp = +d.gdp;
  d.size = +d.gdp / sizeDivisor;
  d.size < 3 ? d.radius = 3 : d.radius = d.size;
  return d;
}
