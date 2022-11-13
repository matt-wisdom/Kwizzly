<template>
    <div class="center mb-4 -mt-4 pt-10">
      <div class="bg-white animate__animated animate__fadeIn bg-opacity-80 text-black lg:px-8 rounded-md w-5/6 lg:w-4/5 md:h-4/5 lg:h-3/5 py-5">
      <h2 class="text-2xl bigdeal mb-4">Private Quizes</h2>
      <ListQuizes :quizes="quizes" />
      <div class="text-white mt-5">
          <button class="disableable bg-gray-400 px-5 py-2 rounded-sm" :disabled="page==1">Prev</button>
          <button class="disableable ml-2 bg-gray-500 px-5 py-2 rounded-sm" :disabled="!has_next">Next</button>
      </div>
      </div>
  </div>
</template>

<script>
import get_api from '../service/api.js'
import ListQuizes from '../components/ListQuizes.vue'
export default {
  name: 'PrivateQuizes',
  created(){
      this.api = get_api(this.$router)
  },
  components: {
      ListQuizes
  },
  methods: {
  },
  data(){
      return {
          page: 1,
          has_next: true,
          quizes: [
              {id: "12333333", timed_per_question: 10, title: "Hello", question_per_session: 10, created: "21 April 2021", public: false, max_contestant: 4},
              {id: "123333", timed_per_question: 10, title: "Hello", question_per_session: 10, created: "21 April 2021", public: false, max_contestant: 4},
              {id: "3333", timed_per_question: 10, title: "Hello", question_per_session: 10, created: "21 April 2021", public: false, max_contestant: 4},
              {id: "1233", timed_per_question: 10, title: "Hello", question_per_session: 10, created: "21 April 2021", public: false, max_contestant: 4},
              {id: "23", timed_per_question: 10, title: "Hello", question_per_session: 10, created: "21 April 2021", public: false, max_contestant: 4},
              {id: "23333", timed_per_question: 10, title: "Hello", question_per_session: 10, created: "21 April 2021", public: false, max_contestant: 4},
              {id: "33", timed_per_question: 10, title: "Hello", question_per_session: 10, created: "21 April 2021", public: false, max_contestant: 4},
              {id: "3gg", timed_per_question: 10, title: "Hello", question_per_session: 10, created: "21 April 2021", public: false, max_contestant: 4},
              {id: "2433", timed_per_question: 10, title: "Hello", question_per_session: 10, created: "21 April 2021", public: false, max_contestant: 4},
              {id: "23e35r33", timed_per_question: 10, title: "Hello", question_per_session: 10, created: "21 April 2021", public: false, max_contestant: 4},
              {id: "3e3", timed_per_question: 10, title: "Hello", question_per_session: 10, created: "21 April 2021", public: false, max_contestant: 4},
              {id: "3re", timed_per_question: 10, title: "Hello", question_per_session: 10, created: "21 April 2021", public: false, max_contestant: 4}
          ]
      }
  }
}
</script>

<style scoped>
    button.disableable:disabled {
        @apply bg-gray-200
    }
</style>