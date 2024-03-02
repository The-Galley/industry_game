<template>
  <div class="overflow-hidden d-flex">
    <div class="StartPage">
      <p class="metagame">
        мета игра
      </p>
      <p class="title">
        Индустрия
      </p>
      <p class="description mt-4">
        приведи свой дистрикт к победе
      </p>
      <router-link
        class="nav-link starpage__button mt-4"
        to="/login"
      >
        Войти
      </router-link>
      <router-link
        class="nav-link starpage__button mt-4"
        to="/register"
      >
        Зарегистрироваться
      </router-link>
    </div>
  </div>
</template>

<script setup>

</script>

<style scoped>
.StartPage {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;
}
.metagame {
  font-size: calc(1.025rem + 1.5vw);
  font-weight: 400;
  line-height: 1.2;
}
.title {
  font-family: Jura, Helvetica, Arial, sans-serif;
  font-size: calc(2.125rem + 5.5vw);
  font-weight: 700;
  line-height: 1.2;
}
.description {
  font-size: calc(0.8rem + 0.8vw);
  font-weight: 400;
  line-height: 1.2;
}
.starpage__button {
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

.starpage__button:hover {
  opacity: 0.5;
}

</style>