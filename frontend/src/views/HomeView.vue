<template>
  <section>
    <h1>Мета-игра "Индустрия 1.0"</h1>

    <p v-if="!isLoggedIn">
      <span><a href="/register">Регистрация</a></span>
      <span> или </span>
      <span><a href="/login">Войти</a></span>
    </p>
    <div v-else>
      <GameListTable />
    </div>
  </section>
</template>
<script>

import { defineComponent } from 'vue';
import GameListTable from '../components/GameListTable.vue';

export default defineComponent({
  name: 'HomeView',
  components: {
    GameListTable,
  },
  computed : {
    isLoggedIn: function() {
      return this.$store.getters.isAuthenticated;
    },
  },

});
</script>
