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

export default {
  data: () => ({
    drawer: true,
    links: []
  }),
  mounted() {
    if (localStorage.login) {
      axios.get('http://localhost:5000/users').then(response => {
        let links = []
        for (let i in response.data) {
          if (response.data[i].uuid !== localStorage.uuid) {
            links.push({title: response.data[i].login, icon:'mdi-message', to: '/messages/' + response.data[i].uuid})
          }
        }
        this.links = links
      })
    } else {
      this.links = [{title: 'Login', icon: 'mdi-login-variant', to: '/login'}]
    }
  },
}
</script>
