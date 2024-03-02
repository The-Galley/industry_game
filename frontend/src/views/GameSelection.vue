<template>
  <div
    v-if="!state.loading"
    class="w-100 d-flex flex-column align-items-center game-selection"
  >
    <HeaderGame />
    <p
      v-if="isPlayer"
      class="byte mx-4"
    >
      {{ stateUser.username }}, скорее присоединяйся к игре
    </p>
    <div
      v-if="isAdmin"
      class="mb-5"
    >
      <button
        class="create-game"
        @click="goToCreateGamePage"
      >
        Создать игру
      </button>
    </div>
    <div
      :class="{'d-flex flex-wrap gap-4 justify-content-center game-selection_user': true}"
    >
      <GameCard
        v-for="(game, index) in games"
        :key="index"
        :name="game.name"
        :description="game.description"
        @click="goToGamePage(game.id)"
      />
    </div>
  </div>
  <Preloader v-else />
</template>

<script setup>
import { actions } from "@/store/modules/games";
import HeaderGame from "@/components/HeaderGame.vue";
import GameCard from "@/components/GameCard.vue";
import {ref, onMounted, reactive} from 'vue';
import { useRouter } from "vue-router";
import { useStore } from 'vuex';
import Preloader from "@/components/PreloaderVue.vue";

const state = reactive({
  loading: true
});
const store = useStore();
const { stateUser, isAdmin, isPlayer } = store.getters;
const router = useRouter();
const goToCreateGamePage =() => {
  router.push('/creategame');
};
const games = ref([]);

const goToGamePage = (gameId) => {
  router.push(`games/${gameId}`);
};


onMounted(async () => {
  try {
    await actions.getGameList(1).then((response) => {
      state.loading = false;
      games.value = response.data.items;
    });

  } catch (error) {
    console.error('Ошибка при получении списка игр:', error);
  }
});

</script>


<style scoped>
.game-selection_user {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  margin: 0 10px 25px 10px;
  justify-content: center;
}

.create-game  {
  display: flex;
  align-items: center;
  justify-content: space-around;
  background-color: #00D5FB;
  color: white;
  border-radius: 8px;
  outline: none;
  border: none;
  Width: 300px;
  Height: 56px;
  font-size: 24px;
  font-weight: 600;
  line-height: 28px;
  text-align: left;
  opacity: 1;
  transition: opacity 0.2s ease-in 0s;
}

.byte {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  text-align: left;
  color: #00D5FB;
  font-size: 20px;
  font-weight: 400;
  line-height: 23px;
}
@media screen and (max-width: 650px) {
  .game-selection {
    margin: 30px 0 30px;
    width: 100vw;
  }
}
</style>