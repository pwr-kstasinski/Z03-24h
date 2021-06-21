import { Component, OnInit } from '@angular/core';
import { CalculatorService } from '../../services/calculator.service';
import { BehaviorSubject, Observable } from 'rxjs';

@Component({
  selector: 'app-calculator',
  templateUrl: './calculator.component.html',
  styleUrls: ['./calculator.component.scss'],
})
export class CalculatorComponent implements OnInit {
  currentNumber: string;
  isResult: boolean;
  $expression: Observable<string>;

  constructor(private service: CalculatorService) {}

  ngOnInit(): void {
    this.currentNumber = '0';
    this.isResult = false;
    this.$expression = this.service.$expressionString;
  }

  onOperationButton(val: string) {
    if (this.isResult) {
      this.service.clearExpression();
      this.isResult = false;
    }
    if ((!this.isFirstZero() || val !== '(') && !this.service.isCloseBracketOnEnd()) {
      this.service.updateExpression(this.currentNumber);
      this.currentNumber = '0';
    }
    if (['+', '-', '*', '/', 'mod', '^', '(', ')'].includes(val)) {
      this.service.updateExpression(val);
    } else {
      this.isResult = true;
      this.currentNumber = this.service.calculate(val);
    }
  }

  onNumberButton(val: string) {
    if (val.match(/[0-9]/)) {
      if (this.isResult) {
        this.clearExpression();
      }
      if (this.isFirstZero() && val !== '0') {
        this.currentNumber = val;
      } else if (val !== '0' || !this.isFirstZero()) {
        this.currentNumber += val;
      }
    } else if (val === '.') {
      if (this.isResult) {
        this.clearExpression();
        this.currentNumber = '0.';
      } else if (!this.currentNumber.includes('.')) {
        this.currentNumber += '.';
      }
    } else if (val === '+-') {
      if (!this.isResult && !this.isFirstZero()) {
        if (this.currentNumber.charAt(0) !== '-') {
          this.currentNumber = '-' + this.currentNumber;
        } else {
          this.currentNumber = this.currentNumber.slice(1);
        }
      }
    }
  }

  onClearButton(val: 'C' | 'CE') {
    if (val === 'C') {
      this.clearExpression();
    } else {
      this.clearEntry();
    }
  }

  clearExpression() {
    this.isResult = false;
    this.service.clearExpression();
    this.currentNumber = '0';
  }

  clearEntry() {
    if (this.isResult) {
      this.clearExpression();
    }
    this.currentNumber = '0';
  }

  isFirstZero() {
    return this.currentNumber.length === 1 && this.currentNumber.charAt(0) === '0';
  }
}
