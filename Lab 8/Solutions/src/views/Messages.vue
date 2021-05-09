<template>
  <v-sheet>
    <div
        v-for="(message, index) in messages"
        :key="index"
        v-bind:class="message.sender === my_uuid ? 'text-right' : ''"
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
    messages: []
  }),
  computed: {
    my_uuid() {
      return localStorage.uuid
    }
  },
  methods: {
    send_message() {
      let new_message = {
        sender: localStorage.uuid,
        content: this.new_message_content
      }
      this.new_message_content = ''
      axios.post('http://localhost:5000/message/' + localStorage.uuid + '/' + this.$route.params.uuid, new_message).then(response => {
        console.log('message sent')
        this.get_messages()
      })
    },
    get_messages() {
      axios.get('http://localhost:5000/message/' + localStorage.uuid + '/' + this.$route.params.uuid).then(response => {
        this.messages = this.messages.concat(response.data)
      })
    }
  },
  created() {
    this.interval = setInterval(() => this.get_messages(), 1000);
  },
  watch: {
    $route() {
      this.new_message_content = ''
      this.messages = []
      this.get_messages()
    }
  }
}
</script>
