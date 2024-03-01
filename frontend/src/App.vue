<template id="app">
  <div class="main">
    <router-view />
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
@font-face {
  font-family: "Jura";
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url("@/fonts/Jura-Bold.woff2") format("woff2"),
  url("@/fonts/Jura-Bold.woff") format("woff");
}

@font-face {
  font-family: "Roboto";
  font-style: normal;
  font-weight: 300;
  font-display: swap;
  src: url("@/fonts/Roboto-Light.woff") format("woff"),
  url("@/fonts/Roboto-Light.woff2") format("woff2");
}

@font-face {
  font-family: "Roboto";
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url("@/fonts/Roboto-Regular.woff") format("woff"),
  url("@/fonts/Roboto-Regular.woff2") format("woff2");
}


#app {
  background: url("@/assets/MainBackground.svg") no-repeat center;
  background-size: cover;
  width: 100vw;
  height: 100vh;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #454862;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.main {
  max-width: 1500px;
  //padding-top: 5em;
  padding: 0;
  margin: 0;
}
</style>