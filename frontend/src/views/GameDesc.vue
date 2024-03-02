<script setup>
import HeaderGame from "@/components/HeaderGame.vue";
import GameDescPlayer from "@/components/GameDescPlayer.vue";
import GameDescAdmin from "@/components/GameDescAdmin.vue";
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';


const store = useStore();
const { isAdmin, isPlayer } = store.getters;
const router = useRouter();
const gameId = router.currentRoute.value.params.gameId;
</script>

<template>
  <div class="d-flex flex-column">
    <div class="gamedesc__header">
      <HeaderGame />
    </div>
    <GameDescPlayer
      v-if="isPlayer"
      :gameid="gameId"
    />
    <GameDescAdmin
      v-if="isAdmin"
      :gameid="gameId"
    />
  </div>
</template>

<style scoped>
.gamedesc__header {
  margin: 30px 0;
}
@media screen and (max-width: 900px) {
  .gamedesc__header {
    display: none;
  }
}
</style>