<script setup>
import { useStore } from 'vuex';
const store = useStore();
const { isAdmin, isPlayer } = store.getters;
</script>

<script>
import {actions} from "@/store/modules/games";

export default {
  props: {
    Id: String
  },

    data() {
      return {
        form: {
          name: '',
          description: '',
        },
        editing: false
      };
    },
  mounted() {
    try {
      actions.getGameById(this.Id)
          .then(response => {
            this.form.name = response.data.name;
            this.form.description = response.data.description;
          });
    } catch (error) {
      console.error('Ошибка при получении списка игр:', error);
    }},
    methods: {
      toggleEdit() {
        this.editing = !this.editing;
      },
      async submit() {
        console.log(this.form);
        this.toggleEdit();
        try {
          console.log(this.form,);
          const response = await actions.updateGameById(this.form, Number(this.Id));
          console.log(response);
        } catch (error) {
          console.error("Произошла ошибка:", error.response);
          this.hasError = "block";
          this.form_error = "Произошла ошибка. Пожалуйста, попробуйте еще раз.";
        }
      },
    }
  };
</script>



<template>
  <div :class="{'game-module': true, 'game-module_admin': isAdmin}">
    <div :class="{'image_container': true, 'image_container_admin': isAdmin}">
      <img
        src="@/assets/CardImage.png"
        alt="Game avatar"
        :class="{'gamedesc__image': true, 'gamedesc__image_admin': isAdmin}"
      >
    </div>
    <b-form
      :class="{'w-100 d-flex flex-column gap-3 mt-4': true, 'align-items-start': isAdmin, 'align-items-center': isPlayer}"
      @submit.prevent="submit"
    >
      <div
        v-if="isAdmin"
        class="w-100 d-flex align-items-end"
      >
        <button
          v-if="!editing"
          class="game-module__submit"
          @click="toggleEdit"
        >
          Редактировать
        </button>
        <button
          v-if="editing"
          type="submit"
          class="game-module__submit"
        >
          Сохранить
        </button>
      </div>
      <!--      :model-value="gameName.name"-->
      <div class="w-100">
        <b-form-textarea
          id="name"
          v-model="form.name"
          class="game-module__input"
          placeholder="Введите название игры"
          :plaintext="!editing"
          no-resize
        />
      </div>
      <!--      :model-value="gameName.description"-->
      <div
        class="w-100 "
        fluid
      >
        <b-form-textarea
          id="description"
          v-model="form.description"
          class="game-module__text-input gamedesc__event"
          placeholder="Описание игры"
          rows="3"
          max-rows="8"
          wrap="soft"
          no-resize
          :plaintext="!editing"
        />
      </div>
    </b-form>
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

.game-module__submit {
  border: none;
  background: transparent;
  color: #454862;
  padding: 0;
  margin: 20px 0 0 auto;
  cursor: pointer;
  opacity: 1;
  transition: opacity 0.3s ease-in-out 0.1s ;
}

.game-module__submit:hover {
 opacity: 0.5;
}

.game-module__input {
  border: none;
  padding-left: 0;
  font-family: Jura, sans-serif;
  font-size: calc(1.3rem + 0.4vw);
  font-weight: 700;
  line-height: 33px;
  text-align: left;
  margin: 0 0 0 10px;
}

.gamedesc__event {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  font-size: 18px;
  font-weight: 400;
  line-height: 19px;
  text-align: center;
  color: #8A8A8A;
  margin: 0 10px 20px;
}

.game-module__text-input {
  min-height: 130px;
  width: 100%;
  border: none;
  font-family: Roboto, Helvetica, Arial, sans-serif;
  font-size: 18px;
  font-weight: 400;
  max-width: 620px;
  line-height: 25px;
  text-align: left;
  margin: 0 10px;
  padding: 10px 10px 10px 0;
}

@media screen and (max-width: 990px) {
  .gamedesc__image {
    width: 660px;
  }
}
@media screen and (max-width: 900px) {
  .game-module__submit {
    margin: 0 0 0 10px;
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
    border-radius: 8px;
  }
}
</style>