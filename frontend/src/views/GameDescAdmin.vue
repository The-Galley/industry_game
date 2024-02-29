<script setup>

import GameModule from "@/components/GameModule.vue";
</script>

<template>
  <div class="w-100 d-flex align-items-center gamedesc">
    <div class="d-flex flex-column align-items-center ms-2">
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
    <div>
      <p>Участники {26}</p>
      <div>
        <p>Участник 1</p>
        <p>Имя участника</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gamedesc {

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
</style>