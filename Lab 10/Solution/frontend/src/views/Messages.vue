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
          v-bind:style="message.sender_id == my_id ? 'background: #007bff; color: #fff' : ''"
          style="z-index: 10"
      >
       {{ message.content }}
      </v-card>
      <div
          style="font-size: 0.8em; color: #ccc; margin-top: 10px;"
      >
        {{ message.read ? 'read, ' : ''}} {{ message.sent }}</div>
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
import router from "@/router";

export default {
  data: () => ({
    new_message_content: '',
    messages: [],
    connection: null
  }),
  computed: {
    my_id() {
      return localStorage.id
    }
  },
  created() {
    console.log("Starting connection to WebSocket Server")
    this.connection = new WebSocket("ws://localhost:5000")
    let ap = this

    this.connection.onmessage = function (event) {
      console.log('message received myid:'+localStorage.id+' recid:'+localStorage.recipient_id)
      let obj = JSON.parse(event.data)
      console.log(obj)

      if (obj.action == 'list_messages' && ((obj.sender == localStorage.id && obj.recipient == localStorage.recipient_id) || (obj.recipient == localStorage.id && obj.sender == localStorage.recipient_id) )) {
        ap.messages = ap.messages.concat(obj['messages'])
      }
    }

    this.connection.onopen = function (event) {
      console.log(event)
      console.log("Successfully connected to the websocket server...")
      this.connection.send(JSON.stringify({"action": "get_users"}))
    }
  },
  mounted() {
    // this.messages = localStorage.messages
    // localStorage.messages = []
  },
  methods: {
    send_message() {
      this.connection.send(JSON.stringify({"action": "send_message", "sender": this.my_id, "recipient": this.$route.params.id, content: this.new_message_content}))
      this.new_message_content = ''
    }
  },
  watch: {
    $route() {
      this.messages = []
      this.new_message_content = ''
      this.connection.send(JSON.stringify({"action": "get_messages", "sender": this.my_id, "recipient": this.$route.params.id}))
      localStorage.recipient_id = this.$route.params.id
    }
  }
}
</script>
