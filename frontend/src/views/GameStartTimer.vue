<script>
export default {
  data() {
    return {
      timeLeft: 60 * 2.5,
      intervalId: null
    };
  },
  computed: {
    formattedTime() {
      const minutes = Math.floor(this.timeLeft / 60);
      const seconds = this.timeLeft % 60;
      return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }
  },
  mounted() {
    this.startTimer();
  },
  beforeUnmount() {
    clearInterval(this.intervalId);
  },
  methods: {
    startTimer() {
      this.intervalId = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
        } else {
          clearInterval(this.intervalId);
        }
      }, 1000);
    }
  }
};
</script>

<template class="overflow-hidden timer">
  <div class="timer__container">
    <p class="timer__title">
      “ИНДУСТРИЯ 1.0”  - Золото современности
    </p>
    <div
      class="timer__color"
    >
      <div class="timer__clock">
        <p class="timer__start">
          Игра начнется через
        </p>
        <p class="timer__num">
          {{ formattedTime }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.timer {
  display: flex;
  align-items: center;
  justify-content: center;
}

.timer__container {
  font-family: Jura, Helvetica, Arial, sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;
  overflow-x: hidden;
}
.timer__color {
  position: relative;
  width: 411px;
  height: 311px;
  border-radius: 20px;
  background-image: linear-gradient(180deg, #5733FF 0%, #19C49B 29%, #E74C3C 58.5%, #BDE41E 100%);
}

.timer__title {
  margin-bottom: 30px;
  max-width: 460px;
  font-size: 28px;
  font-weight: 700;
  line-height: 33px;
  text-align: center;
}

.timer__clock {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 406px;
  height: 306px;
  top:2px;
  left: 3px;
  position: absolute;
  border-radius: 18px;
  overflow: hidden;
  background:#F5F5F5;
}

.timer__start {
  max-width: 300px;
  font-size: 36px;
  font-weight: 700;
  line-height: 43px;
  text-align: center;
}

.timer__num {
  font-size: 64px;
  font-weight: 700;
  line-height: 76px;
  letter-spacing: 0em;
  text-align: center;
}

</style>