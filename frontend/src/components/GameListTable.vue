<template>
  <h6>Goto first button number</h6>
  <BPagination
    v-model="metaPagination.page"
    :total-rows="metaPagination.total"
    :per-page="metaPagination.per_page"
    @page-click="getGameList"
  />
</template>

<script>
import { defineComponent } from 'vue';
import { mapActions } from 'vuex';

export default defineComponent({
  name: 'GameListTable',
  data() {
    return {
      metaPagination: {
        page: null,
        pages: null,
        per_page: null,
        total: null,
      },
    };
  },
  async mounted(){
    await this.loadGameList();
  },
  ...mapActions(['getGameList']),
  methods:{
    async loadGameList(event, page){
      var data = await this.getGameList(page);
      console.log(data);
      console.log('page:', page);
      this.metaPagination.page = 1;
      this.metaPagination.pages = 10;
      this.metaPagination.per_page = 20;
      this.metaPagination.total = 100;
    }
  },
});
</script>