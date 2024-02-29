<template>
  <div class="w-100 d-flex flex-column align-items-center game-selection">
    <HeaderGame />
    <p class="byte">
      {'Name'}, скорее присоединяйся к игре
    </p>
    <div v-if="userRole === 'ADMIN'">
      <button
        class="create-game"
        @click="goToCreateGamePage"
      >
        Создать игру
      </button>
    </div>
    <div :class="{'d-flex flex-wrap gap-4 justify-content-center': true, 'game-selection_admin': userRole === 'ADMIN', 'game-selection_user': userRole === 'PLAYER' }">
      <GameCard
        v-for="(game, index) in games"
        :key="index"
        :name="game.name"
        :description="game.description"
      />
    </div>
  </div>
</template>

<script setup>
import HeaderGame from "@/components/HeaderGame.vue";
import GameCard from "@/components/GameCard.vue";
import { actions } from "@/store/modules/games";
import { ref, onMounted } from 'vue';
import { useRouter } from "vue-router";
// let userRole = 'ADMIN';
const router = useRouter();

const goToCreateGamePage =() => {
  router.push('/creategame');
};
const games = ref([]);


onMounted(async () => {
  try {
    const response = await actions.getGameList(1);
    // games.value = response.data.items;
    console.log(response);
    games.value = [
      { name: 'Игра 1', description: 'Описание игры 1' },
      { name: 'Игра 2', description: 'Описание игры 2' },
      { name: 'Игра 3', description: 'Описание игры 3' },
      { name: 'Игра 4', description: 'Описание игры 4' },
      { name: 'Игра 5', description: 'Описание игры 5' }
    ];
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
    background: url("@/assets/MainBackground.svg") repeat left top;
    background-size: inherit;
    width: 100vw;
  }
}
</style>