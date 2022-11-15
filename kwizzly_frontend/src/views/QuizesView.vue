<template>
  <div class="center mb-4 -mt-4 pt-10">
    <div
      class="
        bg-white
        animate__animated animate__fadeIn
        bg-opacity-80
        text-black
        lg:px-8
        rounded-md
        w-5/6
        lg:w-4/5
        md:h-4/5
        lg:h-3/5
        py-5
      "
    >
      <h2 class="text-2xl bigdeal mb-4">Quizes</h2>
      <div v-if="failed" class="mx-3 px-6 py-1 rounded-md text-red-400">
        Error Loading Data
      </div>
      <ListQuizes :quizes="quizes" />
      <div class="text-white mt-5">
        <button
          @click="go('prev')"
          class="disableable bg-gray-400 px-5 py-2 rounded-sm"
          :disabled="page == 1"
        >
          Prev
        </button>
        <button
          @click="go('next')"
          class="disableable ml-2 bg-gray-500 px-5 py-2 rounded-sm"
          :disabled="!has_next"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import get_api from "../service/api.js";
import base_url from '../configs/base_url.js';
import ListQuizes from "../components/ListQuizes.vue";
export default {
  name: "QuizesView",
  created() {
    this.api = get_api(this.$router);
    this.go("");
  },
  components: {
    ListQuizes,
  },
  methods: {
    go(where) {
      switch (where) {
        case "next":
          this.page += 1;
          break;
        case "prev":
          this.page -= 1;
          break;
      }
      this.api
        .get(base_url.base_api_url + "/quiz/quizes?page=" + this.page)
        .then((resp) => {
          this.quizes = []
          let data = resp.data
          this.has_next = data.has_next;
          for (let quiz of data.data) {
            this.quizes.push({
              id: quiz.id,
              timed_per_question: quiz.timed_per_question,
              title: quiz.title,
              question_per_session: quiz.question_per_session,
              created: quiz.timestamp,
              public: quiz.public,
              max_contestant: quiz.max_contestant,
            });
          }
        })
        .catch((err) => {
          this.failed = true;
          console.log(err);
          this.err_msg = err.response.data.message;
          // this.err_msg = this.err_msg?this.err_msg:err.data
        });
    },
  },
  data() {
    return {
      err_msg: "",
      failed: false,
      page: 1,
      has_next: true,
      quizes: [
      ],
    };
  },
};
</script>

<style scoped>
button.disableable:disabled {
  @apply bg-gray-200;
}
</style>