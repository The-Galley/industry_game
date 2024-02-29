<script setup>

import GameModule from "@/components/GameModule.vue";
import HeaderGame from "@/components/HeaderGame.vue";
</script>

<template>
  <div class="gamedesc">
    <div class="gamedesc__header">
      <HeaderGame />
    </div>
    <div class="w-100 d-flex align-items-center gamedesc__container">
      <div class="d-flex flex-column align-items-start">
        <GameModule />
        <div class="d-flex mt-4">
          <b-button class="gamedesc__button">
            Начать игру
          </b-button>
          <b-button class="gamedesc__button gamedesc__button_leave">
            Отменить игру
          </b-button>
        </div>
      </div>
      <div class="gamedesc__column-right">
        <p class="gamedesc__num">
          Участники <span class="gamedesc__span">{26}</span>
        </p>
        <div class="d-flex flex-column">
          <p class="gamedesc__nick">
            Участник 1
          </p>
          <p class="gamedesc__name">
            Имя участника
          </p>
        </div>
        <div class="d-flex flex-column">
          <p class="gamedesc__nick">
            Участник 1
          </p>
          <p class="gamedesc__name">
            Имя участника
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gamedesc {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  display: flex;
  flex-direction: column;
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
}
</style>