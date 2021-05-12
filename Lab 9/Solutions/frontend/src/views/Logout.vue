<template>
  <h1
  class="text-h2 pa-12 text-center mt-12"
  >
    Logged out
  </h1>
</template>

<script>

export default {
  beforeMount() {
    localStorage.removeItem('login')
    localStorage.removeItem('id')
  }
}
</script>
