<template>
    <div class="container mt-14 md:mt-24 mr-0 lg:mb-16" style="min-height: 50vh">
      <div class="lg:float-right lg:mr-16 animate__animated animate__fadeIn">
        <div class="row mb-10">
          <h1 class="text font-black text-5xl md:pl-20 animate__animated animate__fadeIn">
            Welcome to Kwizzly
          </h1>
        </div>
        <div class="row">
          <p>
            Create and play various types of quizes today.<br>
            You can play quizes alone or against friends.
          </p>
        </div>
        <div class="row ml-10 md:ml-24 mt-5 md:mt-12 flex flex-wrap flex-row">
          <router-link to="create-quiz" class="bg-yellow-500 py-4 my-3 px-3 text-xl  hover:bg-yellow-800">
            Create a quiz
          </router-link>
          <router-link to="quizes" class="ml-2 md:ml-8 hover:bg-red-300  my-3  bg-red-800 text-xl py-4 px-5 animate-pulse">
            Play Now!
          </router-link>
        </div>
      </div>
      </div>
</template>

<script>
  import get_api from "../service/api.js"
  export default {
    components: {
    },
    created() {
      this.api = get_api(this.$router)
    },
    data() {
      return {
      }
    }
  }
</script>

<style scoped>

.shadow-yellow {
  box-shadow: 2px 2px 3px #ffff003e;
}

.shadow-red {
  box-shadow: 3px 3px 4px #ff00003e;
}

</style>
