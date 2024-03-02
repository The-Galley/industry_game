<template>
  <div class="overflow-hidden d-flex justify-content-center">
    <div class="reg">
      <HeaderGame />
      <b-form
        class="w-100 d-flex flex-column gap-3 align-items-center"
        style="max-width: 420px"
        @submit.prevent="submit"
      >
        <p class="form__title">
          Привет, рады снова видеть!
        </p>
        <div class="w-100">
          <label
            for="username"
            class="form__label"
          >Никнейм</label>
          <b-form-input
            id="username"
            v-model="form.username"
            class="form__input"
            :state="usernameValidation"
            placeholder="Введите свое имя"
          />
          <b-form-invalid-feedback
            :state="usernameValidation"
          >
            Это поле не должно быть пустым.
          </b-form-invalid-feedback>
        </div>
        <div class="w-100">
          <label
            for="password"
            class="form__label"
          >Пароль</label>
          <b-form-input
            id="password"
            v-model="form.password"
            type="password"
            class="form__input"
            :state="passwordValidation"
            placeholder="Придумайте пароль"
          />
          <b-form-invalid-feedback :state="passwordValidation">
            Пароль должен содержать не менее 8 символов.
          </b-form-invalid-feedback>
        </div>
        <div class="d-flex flex-column align-items-center justify-content-center w-100">
          <div
            v-if="hasError"
            class="error-message"
          >
            {{ form_error }}
          </div>
          <b-button
            class="reg__button"
            type="submit"
            :disabled="!isFormValid"
          >
            Войти
          </b-button>
          <router-link
            class="nav-link mt-2 text-decoration-underline"
            to="/register"
          >
            Зарегистрироваться
          </router-link>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
import HeaderGame from "@/components/HeaderGame.vue";
import {mapActions} from "vuex";

export default {
  components: {HeaderGame},
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      hasError: false,
      form_error: ''
    };
  },
  computed: {
    usernameValidation() {
      return this.form.username.length > 1;
    },
    passwordValidation() {
      return this.form.password?.length > 7;
    },
    isFormValid() {
      return (
          this.usernameValidation &&
          this.passwordValidation
      );
    },
  },
  methods: {
    ...mapActions(['login']),
    async submit() {
      try {
        console.log(this.form);
        await this.login(this.form);
        this.$router.push('/selectgame');

      } catch (error) {
        if (error.response.status === 404) {
          this.hasError = "block";
          this.form_error = "Пользователь с таким именем пользователя и паролем не найден";
        } else if (error.response.status === 409) {
          this.hasError = "block";
          this.form_error = "Вы уже вошли в систему";
        } else {
          console.error("Произошла ошибка:", error.response);
          this.hasError = "block";
          this.form_error = "Произошла ошибка. Пожалуйста, попробуйте еще раз.";
        }
      }
    },
  },
};
</script>


<style scoped>
.error-message {
  color: red;
  margin: 0 0 10px;
  text-align: center;
}
.reg {
  color: #454862;
  font-family: Roboto, Helvetica, Arial, sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;
  overflow-x: hidden;
}

.form__input{
  background-color: #F2F2F2;
  padding: 18px 15px 18px 15px;
  border: none;
  font-size: calc(0.7rem + 0.45vw);
}

.form__label {
  border: none;
  font-size: calc(0.7rem + 0.45vw);
  font-weight: 400;
}

.form__title {
  font-weight: 400;
  color: #00D5FB;
  font-size: calc(0.925rem + 0.3vw);
}

.reg__button {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  display: flex;
  align-items: center;
  justify-content: space-around;
  background-color: #00D5FB;
  outline: none;
  width: 170px;
  border: none;
  font-size: 18px;
  font-weight: 600;
  padding: 12px 21px 12px 21px;
}
</style>