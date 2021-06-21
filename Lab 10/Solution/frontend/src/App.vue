<template>
  <v-app>

    <v-navigation-drawer
        v-model="drawer"
        app
    >
      <v-sheet
          color="grey lighten-4"
          class="pa-4"
      >
        <div
            class="text-center"
        >
          <v-icon
              color="blue lighten-1"
              size="64"
          >mdi-forum
          </v-icon>
        </div>

        <div
            class="text-center"
        >
          Messengerify
        </div>
      </v-sheet>

      <v-divider></v-divider>

      <v-list>
        <v-list-item
            v-for="link in links"
            :key="link.title"
            :to="link.to"
            link
        >
          <v-list-item-icon>
            <v-icon>{{ link.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ link.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";
import router from "@/router";

export default {
  data: () => ({
    drawer: true,
    links: [],
    connection: null
  }),
  methods: {
    update_navbar(users=[]) {
      if (localStorage.login) {
        let links = []
          if (localStorage.id) {
            for (let i in users) {
              if (users[i].id != localStorage.id) {
                links.push({
                  title: users[i].login,
                  icon: users[i].active ? 'mdi-wifi' : 'mdi-wifi-off',
                  to: '/messages/' + users[i].id
                })
              }
            }
            links.push({title: 'Logout', icon: 'mdi-power', to: '/logout'})
          }
          this.links = links
      } else {
        this.links = [
          {title: 'Login', icon: 'mdi-login-variant', to: '/login'},
          {title: 'Register', icon: 'mdi-account-plus', to: '/register'},
        ]
      }
    }
  },
  created() {
    console.log("Starting connection to WebSocket Server")
    this.connection = new WebSocket("ws://localhost:5000")
    let ap = this

    this.connection.onmessage = function (event) {
      let obj = JSON.parse(event.data)
      if (obj.action === 'list_users') {
        ap.update_navbar(obj.users)
      }
      else if (obj.action === 'check_active') {
        this.connection.send(JSON.stringify({"action": "set_active", "user_id": localStorage.id}))
      }
    }

    this.connection.onopen = function (event) {
      console.log(event)
      console.log("Successfully connected to the websocket server...")
      this.connection.send(JSON.stringify({"action": "get_users"}))
    }
  },
  watch: {
    $route() {
      this.connection.send(JSON.stringify({"action": "get_users"}))
    }
  }
}
</script>
