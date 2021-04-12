import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { CalculatorComponent } from './core/calculator/calculator.component';
import { CalculatorService } from './services/calculator.service';
import { GraphComponent } from './core/graph/graph.component';

@NgModule({
  declarations: [AppComponent, CalculatorComponent, GraphComponent],
  imports: [BrowserModule],
  providers: [CalculatorService],
  bootstrap: [AppComponent],
})
export class AppModule {}
