<template>
  <div>
    <h1
        class="text-h2 pa-12 text-center mt-12"
    >
      Users online
    </h1>

    <v-simple-table>
      <thead>
        <tr>
          <th class="text-left">
            User
          </th>
          <th class="text-left">
            Last seen
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="user in online_users"
          :key="user.id"
        >
          <td>{{ user.login }}</td>
          <td>{{ user.last_seen }}</td>
        </tr>
      </tbody>
  </v-simple-table>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
    online_users: [],
  }),
  methods: {
    get_online_users() {
      axios.get('http://localhost:5000/online').then(response => {
        this.online_users = response.data
      })
    }
  },
  created() {
    setInterval(() => this.get_online_users(), 1000);
  }
}
</script>
