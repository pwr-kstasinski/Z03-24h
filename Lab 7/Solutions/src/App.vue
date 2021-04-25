<template>
  <v-app id="inspire">
    <v-app-bar
        app
        color="white"
        prominent
        shrink-on-scroll
    >
      <v-container class="py-0 fill-height">
        <v-icon
            color="blue lighten-1"
            size="32"
        >
          mdi-weather-partly-cloudy
        </v-icon>

          <v-btn
              text
              disabled
          >
            Weatherify
        </v-btn>

        <v-spacer></v-spacer>

      </v-container>
    </v-app-bar>

    <v-main class="grey lighten-3">
      <v-container>
        <v-row>
          <v-col>
            <router-view></router-view>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    links: [
      {title: 'Weatherify', to: '/'},
      {title: 'About', to: '/about'},
    ],
  }),
}
</script>

<style lang="sass">
h1, h2, h3
  font-family: "Roboto", sans-serif
  font-weight: 300
</style>