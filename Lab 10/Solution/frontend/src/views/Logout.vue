<template>
  <h1
  class="text-h2 pa-12 text-center mt-12"
  >
    Logged out
  </h1>
</template>

<script>

export default {
  created() {
    console.log("Starting connection to WebSocket Server")
    this.connection = new WebSocket("ws://localhost:5000")

    let user_id = localStorage.id
    localStorage.removeItem('login')
    localStorage.removeItem('id')

    setTimeout(function(){ this.connection.send(JSON.stringify({"action": "logout", "user_id": user_id})) }, 3000);
  }
}
</script>
