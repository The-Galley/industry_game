<script setup>
import GameModule from "@/components/GameModule.vue";
import { actions } from "@/store/modules/games";
import {ref, onMounted, reactive} from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const Id = router.currentRoute.value.params.gameId;

const gameName = ref('');
const gameDescription = ref('');

onMounted(async () => {
  try {
    const response = await actions.getGameById(Id);
    gameName.value = response.data.name;
    gameDescription.value = response.data.description;
  } catch (error) {
    console.error('Ошибка при получении списка игр:', error);
  }
});
const users = ref({meta: '', items: ''});
onMounted( () => {
  try {
    actions.getUsersLobby(Id).then((response)=> {
      users.value.meta = response.data.meta;
      users.value.items = response.data.items;
      state.loading = false;
    });
  } catch (error) {
    console.error('Ошибка при получении списка игр:', error);
  }
});


const state = reactive({
  loading: true
});

</script>

<template>
  <div class="w-100 d-flex gamedesc__container">
    <div class="d-flex flex-column align-items-start">
      <div class="w-100">
        <router-link
          class="nav-link gamedesc__link"
          to="/games"
        >
          <img
            src="@/assets/blackArrow.svg"
            alt="arrow-back"
            style="transform: rotate(180deg); width: 14px"
          >
          Назад к выбору игры
        </router-link>
      </div>
      <GameModule :Id="Id" />
      <div class="d-flex mt-4">
        <router-link
          class="nav-link gamedesc__button"
          to="/timer"
        >
          Начать игру
        </router-link>
        <b-button class="gamedesc__button gamedesc__button_leave">
          Отменить игру
        </b-button>
      </div>
    </div>
    <div
      class="gamedesc__column-right"
    >
      <p
        class="gamedesc__num"
      >
        Участники <span
          class="gamedesc__span"
        >{{ users.meta ? users.meta.total : '' }}</span>
      </p>
      <div
        v-for="(user, index) in users.items"
        :key="index"
      >
        <div class="d-flex flex-column">
          <p class="gamedesc__nick">
            {{ user.username }}
          </p>
          <p class="gamedesc__name">
            {{ user.name }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gamedesc__link {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  font-size: 18px;
  width: 220px;
  padding: 5px;
  margin-bottom: 15px;
  text-align: left;
}
.gamedesc__container {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  display: flex;
  align-items: start;
  justify-content: space-between;
  color: #454862;
  margin: 0 15px;
}

.gamedesc__column-right {
  width: 100%;
  margin-left: calc(1rem + 3.5vw);
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-start;
}
.gamedesc__button {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  display: flex;
  align-items: center;
  justify-content: space-around;
  background-color: #00D5FB;
  color: white;
  border-radius: 8px;
  outline: none;
  border: none;
  font-size: 18px;
  padding: 12px 21px;
  font-weight: 600;
  line-height: 28px;
  text-align: left;
}

.gamedesc__button_leave {
  background-color: #CCCDCF;
  margin-left: 30px;
}

.gamedesc__num {
  font-size: 18px;
  font-weight: 600;
  line-height: 21px;
  text-align: left;
  width: 200px;
}

.gamedesc__span {
  font-size: 18px;
  font-weight: 600;
  line-height: 21px;
  letter-spacing: 0em;
  text-align: left;
  margin-left: 10px;
 color:#00D5FB;
}

.gamedesc__nick {
  font-size: 14px;
  font-weight: 500;
  line-height: 25px;
  margin: 0 0 5px;
 }

.gamedesc__name {
  font-family: Roboto;
  font-size: 14px;
  font-weight: 400;
  color: #8A8A8A;
  margin: 0;
}

@media screen and (max-width: 900px) {
  .gamedesc__container {
    flex-direction: column;
    align-items: flex-start;
    gap: 4rem;
  }

  .gamedesc__column-right {
    margin: 0;
  }

  .gamedesc__header {
    display: none;
  }
  .gamedesc__link {
    font-family: Roboto, Helvetica, Arial, sans-serif;
    font-size: 18px;
    width: 220px;
    padding: 5px;
    margin-bottom: 15px;
    text-align: left;
  }
  .gamedesc__link {
     margin-top: 30px;
   }
}
</style>