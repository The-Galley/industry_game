<template>
  <div class="overflow-hidden d-flex justify-content-center">
    <div class="reg">
      <HeaderGame />
      <b-form
        class="w-100 d-flex flex-column gap-3 align-items-center"
        style="max-width: 420px"
        @submit.stop.prevent
      >
        <p class="form__title">
          Привет, давай знакомиться!
        </p>
        <div class="w-100">
          <label
            for="userName"
            class="form__label"
          >ФИО</label>
          <b-form-input
            id="userName"
            v-model="form.userName"
            class="form__input"
            :state="userNameValidation"
            placeholder="Введите свое имя"
          />
          <b-form-invalid-feedback
            :state="userNameValidation"
          >
            Это поле не должно быть пустым.
          </b-form-invalid-feedback>
        </div>
        <div class="w-100">
          <label
            for="userTelegramm"
            class="form__label"
          >Телеграмм</label>
          <b-form-input
            id="userTelegramm"
            v-model="form.userTelegramm"
            class="form__input"
            :state="userTelegrammValidation"
            placeholder="Введите свой ник в телеграмме"
          />
          <b-form-invalid-feedback :state="userTelegrammValidation">
            Ник в Телеграмме должен содержать от 5 символов.
          </b-form-invalid-feedback>
        </div>
        <div class="w-100">
          <label
            for="userNickname"
            class="form__label"
          >Имя в игре</label>
          <b-form-input
            id="userNickname"
            v-model="form.userNickname"
            class="form__input"
            :state="userNicknameValidation"
            placeholder="Придумайте имя, которое будет видно в игре"
          />
          <b-form-invalid-feedback :state="userNicknameValidation">
            Имя в игре должно содержать от 5 символов.
          </b-form-invalid-feedback>
        </div>
        <div class="w-100">
          <label
            for="userPassword"
            class="form__label"
          >Пароль</label>
          <b-form-input
            id="userPassword"
            v-model="form.userPassword"
            class="form__input"
            :state="userPasswordValidation"
            placeholder="Придумайте пароль"
          />
          <b-form-invalid-feedback :state="userPasswordValidation">
            Пароль должен содержать не менее 8 символов.
          </b-form-invalid-feedback>
        </div>
        <div class="d-flex justify-content-end mt-2 w-100">
          <b-button
            class="reg__button"
            type="submit"
            :disabled="!isFormValid"
            @click="handleSubmit"
          >
            Готово
          </b-button>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
import HeaderGame from "@/components/HeaderGame.vue";

export default {
  components: {HeaderGame},
  data() {
    return {
      form: {
        userName: '',
        userTelegramm: '',
        userNickname: '',
        userPassword: '',
      },
    };
  },
  computed: {
    userNameValidation() {
      return this.form.userName.length > 1;
    },
    userTelegrammValidation() {
      return this.form.userTelegramm?.length > 5;
    },
    userNicknameValidation() {
      return this.form.userNickname?.length > 5;
    },
    userPasswordValidation() {
      return this.form.userPassword?.length > 8;
    },
    isFormValid() {
      // Check if all fields are valid
      return (
          this.userNameValidation &&
          this.userTelegrammValidation &&
          this.userNicknameValidation &&
          this.userPasswordValidation
      );
    },
  },
  methods: {
    handleSubmit() {
      console.log(
         this.form
      );
      // Add logic to handle form submission
      // Reset form fields if needed
      this.form.userTelegramm = '';
      this.form.userName = '';
      this.form.userNickname = '';
      this.form.userPassword = '';
    },
  },
};
</script>


<style scoped>
.reg {
  color: #454862;
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
   border: none;
   font-size: 18px;
   font-weight: 600;
   padding: 12px 21px 12px 21px;
 }
</style>