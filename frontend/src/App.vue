<template>
  <div id="app">
    <!--    <NavBar />-->
    <div class="main container">
      <router-view />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import NavBar from '@/components/NavBar.vue';
// export default {
//   components: {
//     NavBar
//   }
// };
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.main {
  //padding-top: 5em;
  padding: 0;
  margin: 0;
}
</style>