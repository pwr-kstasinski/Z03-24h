import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { CalculatorService, Node } from '../../services/calculator.service';
import { graphviz } from 'd3-graphviz';
import { wasmFolder } from '@hpcc-js/wasm';

@Component({
  selector: 'app-graph',
  templateUrl: 'graph.component.html',
  styleUrls: ['graph.component.scss'],
})
export class GraphComponent implements OnInit {
  constructor(private service: CalculatorService) {}

  ngOnInit() {
    wasmFolder('/assets/@hpcc-js/wasm/dist/');
  }

  printTree() {
    const root = this.service.getTree();
    const queue: [[Node, number]] = [[root, 0]];
    let graph = '';
    let index = 0;
    while (queue.length) {
      const [node, parentIndex]: [Node, number] = queue.shift();
      if (graph === '') {
        graph = `${index++}[label="${node.value}"]\n`;
      }
      if (node.leftNode) {
        graph += `${index++}[label="${node.leftNode.value}"]\n`;
        graph += `${parentIndex} -> ${index - 1}\n`;
        queue.push([node.leftNode, index - 1]);
      }
      if (node.rightNode) {
        graph += `${index++}[label="${node.rightNode.value}"]\n`;
        graph += `${parentIndex} -> ${index - 1}\n`;
        queue.push([node.rightNode, index - 1]);
      }
    }
    graphviz('div').renderDot(`digraph {${graph}}`);
  }
}
