<template>
  <div class="w-100 d-flex flex-column align-items-center game-selection">
    <HeaderGame />
    <p class="byte">
      {'Name'}, скорее присоединяйся к игре
    </p>
    <div class="d-flex  flex-wrap gap-3 justify-content-center">
      <GameCard />
      <GameCard />
      <GameCard />
      <GameCard />
      <GameCard />
      <GameCard />
    </div>
  </div>
</template>

<script setup>
import HeaderGame from "@/components/HeaderGame.vue";
import GameCard from "@/components/GameCard.vue";
</script>

<style scoped>
 .byte {
   font-family: Roboto, Helvetica, Arial, sans-serif;
   text-align: left;
   color: #00D5FB;
   font-size: 20px;
   font-weight: 400;
   line-height: 23px;
 }
 @media screen and (max-width: 650px) {
   .game-selection {
     margin: 30px 0 30px;
     background: url("@/assets/MainBackground.svg") repeat left top;
     background-size: inherit;
     width: 100vw;
   }
 }
</style>