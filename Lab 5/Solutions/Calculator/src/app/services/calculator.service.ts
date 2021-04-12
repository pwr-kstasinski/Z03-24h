import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export class Node {
  constructor(public value: string, public leftNode: Node = null, public rightNode: Node = null) {}
}

const OPERATORS = ['+', '-', '*', '/', 'mod', '^'];

@Injectable({
  providedIn: 'root',
})
export class CalculatorService {
  private tree: Node;
  private $expression: BehaviorSubject<string[]> = new BehaviorSubject<string[]>([]);

  constructor() {}

  public calculate(type: string) {
    this.closeBrackets();
    const exp = this.rpn(this.$expression.value);
    this.tree = this.prepareTree(exp);

    let result = this.calculateExpression(this.tree);

    switch (type) {
      case 'sqrt':
        result = Math.sqrt(result);
        break;
      case 'fact':
        result = this.factorial(result);
        break;
      case 'abs':
        result = Math.abs(result);
        break;
      case 'rec':
        result = 1 / result;
        break;
      case 'log':
        result = Math.log10(result);
        break;
    }
    if (type !== '=') {
      this.tree = new Node(type, this.tree);
      this.$expression.next([`${type}(`, ...this.$expression.value, ')']);
    }
    return result;
  }
  public updateExpression(val: string) {
    if (val === ')') {
      if (this.countOpenedBrackets() === 0) {
        return;
      }
    }
    this.$expression.next([...this.$expression.value, val]);
  }

  public clearExpression() {
    this.$expression.next([]);
    this.tree = null;
  }

  public get $expressionString(): Observable<string> {
    return this.$expression.pipe(map((val) => val.join(' ')));
  }

  public getTree(): Node {
    return this.tree;
  }

  public isCloseBracketOnEnd(): boolean {
    return this.$expression.value[this.$expression.value.length - 1] === ')';
  }
  private rpn(exp: string[]): string[] {
    const stack = [];
    const res = [];

    for (const el of exp) {
      if (el === '(') {
        stack.push('(');
      } else if (el === ')') {
        while (stack[stack.length - 1] !== '(') {
          res.push(stack.pop());
        }
        stack.pop();
      } else if (OPERATORS.includes(el)) {
        while (stack.length) {
          if (this.priority(el) === 3 || this.priority(el) > this.priority(stack[stack.length - 1])) {
            break;
          }
          res.push(stack.pop());
        }
        stack.push(el);
      } else {
        res.push(el);
      }
    }
    while (stack.length) {
      res.push(stack.pop());
    }

    return res;
  }

  private priority(el: string): number {
    switch (el) {
      case '+':
      case '-':
        return 1;
      case '*':
      case '/':
      case 'mod':
        return 2;
      case '^':
        return 3;
      default:
        return 0;
    }
  }

  private prepareTree(exp: string[]) {
    const nodes: Node[] = [];
    for (const el of exp) {
      if (OPERATORS.includes(el)) {
        const right = nodes.pop();
        const left = nodes.pop();
        const node = new Node(el, left, right);
        nodes.push(node);
      } else {
        nodes.push(new Node(el));
      }
    }
    return nodes[0];
  }

  private calculateExpression(tree: Node) {
    if (!tree.leftNode && !tree.rightNode) {
      return Number.parseFloat(tree.value);
    } else {
      return this.calculateNode(
        this.calculateExpression(tree.leftNode),
        this.calculateExpression(tree.rightNode),
        tree.value,
      );
    }
  }

  private calculateNode(leftValue: number, rightValue: number, operator: string): number {
    switch (operator) {
      case '+':
        return leftValue + rightValue;
      case '-':
        return leftValue - rightValue;
      case '*':
        return leftValue * rightValue;
      case '/':
        return leftValue / rightValue;
      case 'mod':
        return leftValue % rightValue;
      case '^':
        return Math.pow(leftValue, rightValue);
    }
  }

  private factorial(num: number): number {
    if (num > 0 && Number.isInteger(num)) {
      try {
        const helpFactorial = (n, acc) => (n === 0 ? acc : helpFactorial(n - 1, n * acc));
        return helpFactorial(num, 1);
      } catch (e: any) {
        if (e instanceof RangeError) {
          return Number.POSITIVE_INFINITY;
        } else {
          return NaN;
        }
      }
    }
    return NaN;
  }

  private countOpenedBrackets() {
    return this.$expression.value
      .filter((el) => el === '(' || el === ')')
      .reduce((acc, curr) => (curr === '(' ? ++acc : --acc), 0);
  }

  private closeBrackets() {
    const openedBrackets = this.countOpenedBrackets();
    this.$expression.next([...this.$expression.value, ...Array(openedBrackets).fill(')')]);
  }
}
