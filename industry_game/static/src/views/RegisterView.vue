<template>
<section>
    <form
    lass="needs-validation"
      @submit.prevent="submit">

    <div class="mb-3">
        <label for="username" class="form-label">Username:</label>
        <input type="text" name="username" v-model="user.username" class="form-control" />
        <div
          class="invalid-feedback"
          :style="{ display: hasError}"
        >{{ form_error }}</div>
    </div>
    <div class="mb-3">
        <label for="password" class="form-label">Password:</label>
        <input type="password" name="password" v-model="user.password" class="form-control" />
        <div
          class="invalid-feedback"
          :style="{ display: hasError}"
        >{{ form_error }}</div>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</section>
</template>

<script>
import { defineComponent } from 'vue';
import { mapActions } from 'vuex';

export default defineComponent({
name: 'RegisterView',
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
    ...mapActions(['register']),
    async submit() {
    try {
        console.log(this.user)
        await this.register(this.user);
    } catch (error) {
        this.hasError = "block";
        this.form_error = error.response.statusText;
    }
    },
},
});
</script>
