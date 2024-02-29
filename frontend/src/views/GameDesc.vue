<script setup>

import GameModule from "@/components/GameModule.vue";
import HeaderGame from "@/components/HeaderGame.vue";
</script>

<template>
  <div class="gamedesc__header">
    <HeaderGame />
  </div>
  <div class="w-100 d-flex flex-column align-items-center gamedesc">
    <div class="w-100 d-flex flex-column align-items-center">
      <GameModule />
      <b-button class="gamedesc__button mt-5">
        Присоединиться к игре
      </b-button>
      <div class="d-flex flex-column">
        <p class="gamedesc__wait">
          gigachad99,  игра скоро начнется
        </p>
        <b-button class="gamedesc__button gamedesc__button_leave">
          Отказаться от участия
        </b-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gamedesc__header {
  margin: 30px 0;
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
  margin-top: 150px;
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
    background: url("@/assets/MainBackground.svg") no-repeat left top;
    width: 100vw;
    height: 100vh;
    overflow-y: hidden;
  }
}

</style>