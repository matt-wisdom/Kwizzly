<template>
  <div class="center">
    <div class="bg-white text-black w-screen md:w-4/5 overflow-x-scroll custom-scrollbar">
      <table class="w-full">
        <thead class="font-black text-2xl">
          <tr class="border-b border-gray-300">
            <td class="py-4">Position</td>
            <td class="py-4">User</td>
            <td>Score</td>
            <td>Date</td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="score, i in scores" v-bind:key="score" class="border-b border-gray-300">
            <td class="py-5">{{i}}</td>
            <td class="py-5">{{score.score.taker_name || score.score.taker_id}}</td>
            <td>{{score.score.score}}%</td>
            <td>{{new Date(score.score.timestamp*1000).toLocaleString()}}</td>
          </tr>
          <div v-if="scores.length < 1" >
            No one has played this game yet. <br>
            <button class="px-6 py-4 rounded bg-gray-700 hover:bg-gray-400 my-5">
              Click to play.
            </button>
          </div>
        </tbody>
      </table>
      <button v-if="has_next"
          @click="go()"
          class="disableable my-4 ml-2 bg-gray-500 px-5 py-2 rounded-sm"
    >Load more</button>
    </div>
  </div>
</template>
<script>
import get_api from '../service/api.js'
import base_url from '../configs/base_url.js';
export default {
  name: "LeaderBoard",
  created() {
    this.api = get_api(this.$router);
    this.go();
  },
  data() {
    return {
      page: 0,
      scores: [],
      has_next: true,
    };
  },
  methods: {
    go() {
      this.page += 1;
      this.api
        .get(base_url.base_api_url + `/quiz/${this.$route.params['quiz_id']}/leaderboard?page=${this.page}` )
        .then((resp) => {
          let data = resp.data;
          console.log(data)
          this.has_next = data.has_next;
          for (let score of data.data) {
            this.scores.push({
              score,
            });
          }
        })
        .catch((err) => {
          alert(err)
          this.failed = true
          console.log(err)
          this.err_msg = err.response.data.message
        });
    },
  },
};
</script>
<style scoped>
</style>