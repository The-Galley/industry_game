<template>
  <div class="w-100 d-flex flex-column align-items-center game-selection">
    <HeaderGame />
    <p class="byte">
      {'Name'}, скорее присоединяйся к игре
    </p>
    <div :class="{'': true, 'game-selection_admin': userRole === 'ADMIN', 'game-selection_user': userRole === 'PLAYER' }">
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

let userRole = 'PLAYER';
</script>

<style scoped>
.game-selection_user {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: center;
}

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