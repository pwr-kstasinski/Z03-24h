<template>
  <v-col
      cols="12"
      lg="8"
      class="mx-auto"
  >
    <h1
        class="text-h2 pa-12 text-center mt-12"
    >
      Login
    </h1>
    <v-sheet
        elevation="2"
        class="my-5 pa-5"
        rounded="lg"
    >
      <div>
        <v-text-field
            @keypress.enter="submit()"
            v-model="login"
            label="Login">
        </v-text-field>
        <v-text-field
            @keypress.enter="submit()"
            v-model="password"
            label="Password"
            type="password">
        </v-text-field>
        <div
            class="text-center"
        >
          <v-btn
              color="blue lighten-1"
              text
              depressed
              elevation="2"
              large
              @click="submit()"
          >Login
          </v-btn>
        </div>
      </div>
    </v-sheet>
  </v-col>
</template>

<script>
import router from "@/router";

export default {
  data: () => ({
    login: '',
    password: '',
    connection: null
  }),
  methods: {
    submit() {
      this.connection.send(JSON.stringify({
        "action": "try_login",
        "login": this.login,
        "password": this.password
      }))
    }
  },
  created() {
    console.log("Starting connection to WebSocket Server")
    this.connection = new WebSocket("ws://localhost:5000")

    this.connection.onmessage = function (event) {
      let obj = JSON.parse(event.data)
      if (obj.action === 'confirm_login') {
        localStorage.login = obj.login
        localStorage.id = obj.id
        router.push('/')
      }
      else if (obj.action === 'failed_login') {
        console.log('login failed')
      }
    }

    this.connection.onopen = function (event) {
      console.log(event)
      console.log("Successfully connected to the websocket server...")
    }
  },
  mounted() {
    if (localStorage.login) {
      router.push('/')
    }
  }
}
</script>
