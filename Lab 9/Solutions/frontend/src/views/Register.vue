<template>
  <v-col
      cols="12"
      lg="8"
      class="mx-auto"
  >
    <h1
        class="text-h2 pa-12 text-center mt-12"
    >
      Register
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
          >Register
          </v-btn>
        </div>
      </div>
    </v-sheet>
  </v-col>
</template>

<script>
import router from "@/router";
import axios from 'axios';

export default {
  data: () => ({
    login: '',
    password: '',
  }),
  methods: {
    submit() {
      axios.post('http://localhost:5000/users', {
        "login": this.login,
        "password": this.password
      }).then(response => {
        localStorage.login = response.data.login
        localStorage.id = response.data.id
        router.push('/')
      })
    }
  },
  mounted() {
    if (localStorage.login) {
      router.push('/')
    }
  }
}
</script>
