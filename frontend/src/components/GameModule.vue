<script setup>
 let userRole = 'ADMIN';
</script>

<template>
  <div :class="{'game-module': true, 'game-module_admin': userRole === 'ADMIN'}">
    <div :class="{'image_container': true, 'image_container_admin': userRole === 'ADMIN'}">
      <img
        src="@/assets/CardImage.png"
        alt="Game avatar"
        :class="{'gamedesc__image': true, 'gamedesc__image_admin': userRole === 'ADMIN'}"
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
  max-width: 650px;
}

.game-module_admin {
  align-items: flex-start;
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
  max-width: 640px;
}

.gamedesc__title {
  font-family: Jura,sans-serif;
  font-size: calc(1.3rem + 0.4vw);
  font-weight: 700;
  line-height: 33px;
  text-align: left;
  margin: 25px 0 25px 10px;

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
@media screen and (max-width: 800px) {
  .gamedesc__image {
    width: 460px;
  }

  .image_container_admin {
    height: 0;
  }

  .gamedesc__image_admin {
    max-width: 0px;
    height: 0;
  }
}
@media screen and (max-width: 650px) {
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