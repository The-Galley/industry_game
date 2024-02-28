<template>
  <section>
    <form
      class="needs-validation"
      @submit.prevent="submit"
    >
      <div class="mb-3">
        <h3>Войти в личный кабинет</h3>
      </div>
      <div class="mb-3">
        <label
          for="username"
          class="form-label"
        >Логин:</label>
        <input
          v-model="user.username"
          type="text"
          name="username"
          class="form-control"
        >
        <div
          class="invalid-feedback"
          :style="{ display: hasError}"
        >
          {{ form_error }}
        </div>
      </div>
      <div class="mb-3">
        <label
          for="password"
          class="form-label"
        >Пароль:</label>
        <input
          v-model="user.password"
          type="password"
          name="password"
          class="form-control"
        >
        <div
          class="invalid-feedback"
          :style="{ display: hasError}"
        >
          {{ form_error }}
        </div>
      </div>
      <button
        type="submit"
        class="btn btn-primary"
      >
        Войти
      </button>
    </form>
  </section>
</template>

    <script>
    import { defineComponent } from 'vue';
    import { mapActions } from 'vuex';

    export default defineComponent({
    name: 'LoginView',
    data() {
        return {
        user: {
            username: '',
            password: '',
        },
        form_error: '',
        hasError: null,
        };
    },
    methods: {
        ...mapActions(['login']),
        async submit() {
        try {
            console.log(this.user);
            await this.login(this.user);
            this.$router.push('/');
        } catch (error) {
            this.hasError = "block";
            this.form_error = error?.response?.statusText;
        }
        },
    },
    });
    </script>
