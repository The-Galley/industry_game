<script setup>
import GameModule from "@/components/GameModule.vue";
import {actions} from "@/store/modules/games";
import { useStore } from 'vuex';
const store = useStore();
const { stateUser } = store.getters;
console.log(stateUser);
import { useRouter } from 'vue-router';
import {onMounted, reactive} from "vue";
import Preloader from "@/components/PreloaderVue.vue";

const router = useRouter();
const Id = router.currentRoute.value.params.gameId;
const state = reactive({
  userCheckResult: '',
  loading: true
});

onMounted(async () => {
  try {
    actions.getUserCheck(Id).then((res) => {
      state.userCheckResult = res.data.status;
      state.loading = false;
      console.log(state.userCheckResult);
    });
  } catch (error) {
    console.error('Ошибка при получении данных:', error);
  }
});
const addUserToGame = async () => {
  try {
  await actions.addUsersLobby(Id)
      .then(() => {
       actions.getUserCheck(Id).then((res) => {
         state.userCheckResult = res.data.status;
         console.log(state.userCheckResult);
       });
      });
  }
  catch (error) {
    console.error('Ошибка при входе:', error);
  }
};
const deleteUserFromGame = async () => {
  try {
    await actions.deleteUserFromLobby(Id)
        .then(() => {
          state.userCheckResult = 'user deleted';
        });
  }
  catch (error) {
    console.error('Ошибка при выходе:', error);
  }
};

</script>

<template>
  <div
    v-if="!state.loading"
    class="w-100 d-flex flex-column align-items-center gamedesc"
  >
    <div class="w-100 d-flex flex-column align-items-center">
      <div class="w-100">
        <router-link
          class="nav-link gamedesc__link mt-4"
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
      <b-button
        v-if="state.userCheckResult !== 'CHECKED_IN'"
        class="gamedesc__button"
        @click="addUserToGame"
      >
        Присоединиться к игре
      </b-button>
      <div
        v-if="state.userCheckResult === 'CHECKED_IN'"
        class="d-flex flex-column mt-3"
      >
        <p class="gamedesc__wait">
          {{ stateUser.username }},  игра скоро начнется
        </p>
        <b-button
          class="gamedesc__button gamedesc__button_leave"
          @click="deleteUserFromGame"
        >
          Отказаться от участия
        </b-button>
      </div>
    </div>
  </div>
  <Preloader v-else />
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

.gamedesc__button {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  display: flex;
  align-items: center;
  justify-content: space-around;
  background-color: #00D5FB;
  outline: none;
  border: none;
  font-size: 18px;
  padding: 14px 21px;
  font-weight: 600;
  line-height: 28px;
  text-align: left;
}

.gamedesc__button_leave {
  background-color: #CCCDCF;
}

.gamedesc__wait {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  text-align: left;
  color: #00D5FB;
  font-size: 16px;
  font-weight: 400;
}

@media screen and (max-width: 650px) {
  .gamedesc {
    overflow-x: hidden;
  }
}

</style>