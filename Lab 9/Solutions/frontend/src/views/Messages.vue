<template>
  <v-sheet>
    <div
        v-for="message in messages"
        :key="message.id"
        v-bind:class="message.sender_id == my_id ? 'text-right' : ''"
        class="my-8 mx-4"
    >
      <v-card
          elevation="2"
          class="pa-3 d-inline"
          style="z-index: 10"
      >
        {{ message.content }}
      </v-card>
    </div>

    <v-text-field
        @click:append="send_message()"
        @keyup.enter="send_message()"
        v-model="new_message_content"
        style="position: absolute; bottom: 0; width: 100%; z-index: 11; background: #fff"
        outlined
        label="Send a message"
        append-icon="mdi-send"
        class="pa-3"
        hide-details
        clearable
    ></v-text-field>
  </v-sheet>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
    new_message_content: '',
    messages: [],
    last_message_id: 0
  }),
  computed: {
    my_id() {
      return localStorage.id
    }
  },
  methods: {
    send_message() {
      let new_message = {
        sender: localStorage.id,
        content: this.new_message_content
      }
      this.new_message_content = ''
      axios.post('http://localhost:5000/message/' + this.my_id + '/' + this.$route.params.id, new_message).then(response => {
        this.get_new_messages()
      })
    },
    get_new_messages() {
      axios.get('http://localhost:5000/message/' + this.my_id + '/' + this.$route.params.id).then(response => {
        let last_id = 0
        for (let index in this.messages) {
          if (last_id < this.messages[index].id) {
            last_id = this.messages[index].id
          }
        }
        console.log(last_id)

        this.messages = this.messages.concat(response.data.filter(message => message.id > last_id))
      })
    },
    send_heartbeat() {
      axios.post('http://localhost:5000/online', {'user_id': this.my_id})
    }
  },
  created() {
    setInterval(() => this.get_new_messages(), 1000);
    setInterval(() => this.send_heartbeat(), 1000);
  },
  watch: {
    $route() {
      this.new_message_content = ''
      this.messages = []
      this.get_new_messages()
    }
  }
}
</script>
