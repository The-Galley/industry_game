<template>
  <div class="overflow-hidden d-flex mx-3">
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
      <b-button class="starpage__button mt-4">
        Войти в игру
        <img
          src="@/assets/Arrow.svg"
          alt="arrow"
        >
      </b-button>
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
  background: url("@/assets/MainBackground.svg") no-repeat center;
  width: 100vw;
  height: 100vh;
  overflow-x: hidden;
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
  outline: none;
  border: none;
  Width: 215px;
  Height: 56px;
  font-size: 24px;
  font-weight: 600;
  line-height: 28px;
  text-align: left;
}

</style>