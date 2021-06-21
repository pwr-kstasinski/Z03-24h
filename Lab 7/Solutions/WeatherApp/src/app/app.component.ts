import { Component, OnInit, ViewChild } from '@angular/core';
import {
  Class16DayDailyForecastService,
  Class120HourHourlyForecastService,
  ForecastDay,
  ForecastHourly,
  ForecastHour,
} from 'RestWeatherApiClient';
import { FormControl } from '@angular/forms';
import { environment } from '../environments/environment';
import { NgbAlert } from '@ng-bootstrap/ng-bootstrap';
import { BehaviorSubject } from 'rxjs';
import { debounceTime } from 'rxjs/operators';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  ViewStateEnum = ViewStateEnum;
  cityControl = new FormControl('');

  dailyData: ForecastDay;
  hourlyData: ForecastHourly;
  currentViewState: ViewStateEnum;

  selectedDay: Date;
  alertMessage$ = new BehaviorSubject<string>('');

  @ViewChild('alert') alert: NgbAlert;

  constructor(private dailyService: Class16DayDailyForecastService,
              private hourlyService: Class120HourHourlyForecastService) {
  }

  ngOnInit(): void {
    this.currentViewState = ViewStateEnum.None;
    this.setAlertTimer();
  }


  search(): void {
    this.dailyService.forecastDailyGet(this.cityControl.value, environment.api_key).subscribe((data) => {
      if (data !== null) {
        this.dailyData = data;
        this.dailyData.data = this.dailyData.data.slice(0, 3);
        this.cityControl.setValue(this.dailyData.city_name);
        this.currentViewState = ViewStateEnum.Daily;
      } else {
        this.currentViewState = ViewStateEnum.None;
        this.runAlert(`Nie znaleziono danych dla miasta: ${this.cityControl.value}`);
      }
    });
  }

  backButton(): void {
    this.currentViewState = ViewStateEnum.Daily;
  }

  getDate(str: string): Date {
    return new Date(str);
  }


  getHourlyData(): Promise<ForecastHourly> {
    return new Promise((res, rej) => {
      this.hourlyService.forecastHourlyGet(this.dailyData.city_name, environment.api_key).subscribe(
        (data) => res(data),
        err => res(null),
      );
    });
  }

  async openHourly(dateString: string): Promise<void> {
    if (!this.hourlyData || this.hourlyData.country_code !== this.dailyData.country_code) {
      this.hourlyData = await this.getHourlyData();
    }

    if (this.hourlyData !== null) {
      this.selectedDay = this.getDate(dateString);
      this.currentViewState = ViewStateEnum.Hourly;
    } else {
      this.runAlert('Wystąpił błąd podczas pobierania danych godzinowych');
    }
  }

  getHourlyTempByDate(): Array<ForecastHour> {
    return this.hourlyData.data.filter(({ timestamp_local }) => this.selectedDay.getTime() === new Date(timestamp_local.slice(0, 10)).getTime());
  }

  getBarStyles(temp: number): { 'height': string, 'background-position': string } {
    temp = Math.trunc(temp);
    return {
      'height': temp + 50 + 'px',
      'background-position': temp + 25 + '%',
    };
  }

  setAlertTimer(): void {
    this.alertMessage$.pipe(debounceTime(4000)).subscribe((value) => {
      if (value !== '') {
        this.alertMessage$.next('');
      }
    });
  }

  runAlert(message: string): void {
    this.alertMessage$.next(message);
  }
}

enum ViewStateEnum {
  None,
  Daily,
  Hourly
}
