<script setup>

</script>

<template>
  <button
    class="card"
    @click="console.log(1)"
  >
    <img
      src="@/assets/CardImage.png"
      alt="Card"
      class="card__image"
    >
    <div class="p-2 w-100 d-flex flex-column align-items-start">
      <p class="card__description">
        Всемирный фестиваль молодежи 2024
      </p>
      <div class="d-flex justify-content-between w-100">
        <p class="card__name">
          “ИНДУСТРИЯ 1.0”  - Золото современности
        </p>
        <img
          src="@/assets/blackArrow.svg"
          alt="Arrow"
        >
      </div>
    </div>
  </button>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 400px;
  background-color: #F2F2F2;
  border: none;
  border-radius: 8px;
  scale: 1;
  transition: scale 0.5s ease 0s;
}
.card:hover {
  scale: 1.05;
}
.card__image {
  width: 400px;
  display: flex;
  object-fit: cover;
  object-position: center;
  border-radius: 8px;
}

.card__name {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  max-width: 330px;
  font-size: 20px;
  font-weight: 400;
  text-align: left;
  margin: 0;
  color: #454862;
}

.card__description {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  color: #8A8A8A;
  font-size: 14px;
  font-weight: 400;
  line-height: 16px;
  text-align: left;
}

@media screen and (max-width: 450px) {
  .card {
    max-width: 350px;
  }

  .card__image {
    width: 350px;
  }
}
</style>