<template>
  <div>
    <v-sheet
        class="mt-5 py-5"
        rounded="lg"
    >
      <v-autocomplete
          hide-details
          class="mx-5"
          :items="available_cities"
          item-text="city_name"
          item-value="city_id"
          label="City"
          outlined
          v-model="selected_city"
          @change="change_city()"
      ></v-autocomplete>
    </v-sheet>

    <v-row v-if="daily_forecast">
      <v-col v-for="i in [0, 1, 2]" :key="i" cols="12" md="4">
        <v-sheet
            class="mt-5 py-5 text-center"
            rounded="lg"
        >
          <h3>{{ daily_forecast[i]['valid_date'] }}</h3>
          <h1>{{ daily_forecast[i]['temp'] }} °C</h1>
          <img :src="'https://www.weatherbit.io/static/img/icons/' + daily_forecast[i]['weather']['icon'] + '.png'">
          <h3>{{ daily_forecast[i]['weather']['description'] }}</h3>
        </v-sheet>

        <v-btn
            color="white"
            class="d-block ma-auto mt-5"
            @click="show_hourly_forecast(daily_forecast[i]['valid_date'])"
        >
          Hourly forecast
        </v-btn>
      </v-col>

      <v-dialog
          v-model="dialog"
          max-width="500"
      >

        <v-card>
          <h1 class="text-center py-5">
            {{ selected_day }}
          </h1>
          <v-card-text>
            <v-sparkline
                :labels="hourly_forecast_labels"
                :value="hourly_forecast_values"
                color="blue lighten-1"
                line-width="2"
                padding="16"
            ></v-sparkline>

            <v-simple-table>
              <thead>
              <tr>
                <th>
                  Time
                </th>
                <th>
                  Temperature
                </th>
              </tr>
              </thead>
              <tbody>
              <tr
                  v-for="hour in hourly_forecast"
                  :key="hour['timestamp_utc']"
              >
                <td>{{ hour['timestamp_utc'].substr(11, 8) }}</td>
                <td>{{ hour['temp'] }} °C</td>
              </tr>
              </tbody>
            </v-simple-table>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>

<script>
import cities_list from '@/assets/cities.json'
import axios from 'axios'

export default {
  data() {
    return {
      available_cities: cities_list,
      selected_city: '',
      daily_forecast: '',
      dialog: false,
      selected_day: '',
      hourly_forecast: '',
    }
  },
  computed: {
    hourly_forecast_labels() {
      let hours = []
      for (let key in this.hourly_forecast) {
        hours.push(this.hourly_forecast[key]['timestamp_utc'].substr(11, 2))
      }
      return hours
    },
    hourly_forecast_values() {
      let values = []
      for (let key in this.hourly_forecast)
        values.push(this.hourly_forecast[key]['temp'])
      return values
    }
  },
  methods: {
    change_city() {
      axios
          .get('https://api.weatherbit.io/v2.0/forecast/daily?key=b222196110454d3eafe661c36e73f212&city_id=' + this.selected_city)
          .then(response => (this.daily_forecast = response['data']['data']))
    },
    show_hourly_forecast(day) {
      axios
          .get('https://api.weatherbit.io/v2.0/forecast/hourly?&key=b222196110454d3eafe661c36e73f212&city_id=' + this.selected_city)
          .then(response => (this.hourly_forecast = response['data']['data'].filter(entry => entry['timestamp_utc'].substr(0, 10) === day)))
      this.dialog = true
      this.selected_day = day
    }
  },
}
</script>
