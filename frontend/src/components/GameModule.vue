<script setup>
 let userRole = 'Admin';
import HeaderGame from "@/components/HeaderGame.vue";
</script>

<template>
  <div class="gamedesc__header">
    <HeaderGame />
  </div>
  <div :class="{'game-module': true, 'game-module_admin': userRole === 'Admin'}">
    <div class="image_container">
      <img
        src="@/assets/CardImage.png"
        alt="Game avatar"
        :class="{'gamedesc__image': true, 'gamedesc__image_admin': userRole === 'Admin'}"
      >
    </div>
    <h2 class="gamedesc__title">
      “ИНДУСТРИЯ 1.0”  - Золото современности
    </h2>
    <p class="gamedesc__event">
      Всемирный фестиваль молодежи 2024
    </p>
    <p class="gamedesc__description">
      Описание игры Описание игры Описание игры Описание игры Описание игры Описание игры
      Описание игры Описание игры Описание игры Описание игры Описание игры Описание игры
      Описание игры Описание игры Описание игры Описание игры Описание игры Описание игры
    </p>
  </div>
</template>

<style scoped>
.game-module {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.game-module_admin {
  align-items: flex-start;
}

.gamedesc__header {
  margin: 30px 0;
}

.image_container {
  max-width: 864px;
  height: 180px;
}
.gamedesc__image {
  width: 860px;
  height: 100%;
  object-fit: cover;
  object-position: center;
  border-radius: 8px;
}

.gamedesc__image_admin {
  width: 640px;
}

.gamedesc__title {
  font-family: Jura,sans-serif;
  font-size: calc(1.4rem + 0.6vw);
  font-weight: 700;
  line-height: 33px;
  text-align: center;
  margin: 25px 10px;

}

.gamedesc__event {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 19px;
  text-align: center;
  color: #8A8A8A;
  margin: 0 10px 20px;
}

.gamedesc__description {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  font-size: 14px;
  font-weight: 400;
  max-width: 620px;
  line-height: 25px;
  margin: 0 10px;
}
@media screen and (max-width: 990px) {
  .gamedesc__image {
    width: 660px;
  }
}
@media screen and (max-width: 768px) {
  .gamedesc__image {
    width: 460px;
  }
}
@media screen and (max-width: 650px) {
  .gamedesc {
    background: url("@/assets/MainBackground.svg") no-repeat left top;
    width: 100vw;
    height: 100vh;
    overflow-y: hidden;
  }

  .gamedesc__header {
    display: none;
  }

  .image_container {
    width: 100%;
  }

  .gamedesc__image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    border-radius: 0 0 8px 8px;
  }
}
</style>