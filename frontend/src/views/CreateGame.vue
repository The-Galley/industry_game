<template>
  <div class="overflow-hidden d-flex justify-content-center">
    <div class="reg">
      <HeaderGame />
      <b-form
        class="w-100 d-flex flex-column gap-3 align-items-center"
        style="max-width: 420px"
        @submit.prevent="submit"
      >
        <div class="w-100">
          <label
            for="name"
            class="form__label"
          >Название игры</label>
          <b-form-input
            id="name"
            v-model="form.name"
            class="form__input"
            :state="nameValidation || !formSubmitted ? null : false"
            placeholder="Введите название игры"
          />
          <b-form-invalid-feedback
            :state="nameValidation || !formSubmitted ? null : false"
          >
            Это поле не должно быть пустым.
          </b-form-invalid-feedback>
        </div>
        <div class="w-100">
          <label
            for="description"
            class="form__label"
          >Описание игры</label>
          <b-form-input
            id="description"
            v-model="form.description"
            class="form__input"
            :state="descriptionValidation || !formSubmitted ? null : false"
            placeholder="Придумайте описание игры"
          />
          <b-form-invalid-feedback :state="descriptionValidation || !formSubmitted ? null : false">
            Это поле не должно быть пустым.
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
          >
            Создать игру
          </b-button>
        </div>
      </b-form>
    </div>
  </div>
</template>

<script>
import HeaderGame from "@/components/HeaderGame.vue";
import {actions} from "@/store/modules/games";

export default {
  components: {HeaderGame},
  data() {
    return {
      form: {
        name: '',
        description: '',
      },
      hasError: false,
      form_error: '',
      formSubmitted: false
    };
  },
  computed: {
    nameValidation() {
      return this.form.name.length > 1;
    },
    descriptionValidation() {
      return this.form.description?.length > 1;
    },
    isFormValid() {
      return (
          this.nameValidation &&
          this.descriptionValidation
      );
    },
  },
  methods: {
    async submit() {
      try {
        if (!this.isFormValid) {
          return;
        }
        console.log(this.form);
        const response = await actions.createGame(this.form);
        this.$router.push(`/games/${response.data.id}`);

      } catch (error) {
        console.error("Произошла ошибка:", error.response);
        this.hasError = "block";
        this.form_error = "Произошла ошибка. Пожалуйста, попробуйте еще раз.";
      } finally {
        this.formSubmitted = true;
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

.form__input {
  font-family: Roboto, Helvetica, Arial, sans-serif;
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
  margin-top: 15px;
}
</style>