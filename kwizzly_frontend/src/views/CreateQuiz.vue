<template>
  <div class="center mb-1 -mt-4 pt-10">
      <div class="bg-white animate__animated animate__fadeIn bg-opacity-80 text-black lg:px-8 rounded-md w-5/6 lg:w-3/5 md:h-5/6 py-5">
      <h2 class="text-2xl bigdeal">Create A Quiz</h2>
        <component 
        v-if="!finished"
        :quiz_title="quiz_title"
        :quiz_public="quiz_public" 
        :time_per_question="time_per_question" 
        :question_per_game="question_per_game" 
        :max_contestant="max_contestant"
        @finished-1="finished_1" 
        @finished-2="finished_2"
        :is="currentComp"
        @back="currentComp=comps['0']"
        ></component>
      </div>
  </div>
</template>

<script>
import get_api from '../service/api.js'
import base_url from '../configs/base_url.js'
import CreateQuizIndex from '../components/CreateQuizIndex.vue'
import CreateQuizQuestions from "../components/CreateQuizQuestions.vue"
export default {
  name: 'LoginView',
  created(){
      this.api = get_api(this.$router)
  },
  components: {
      CreateQuizIndex,
      CreateQuizQuestions
  }
  ,
  methods: {
      finished_1(data){
          this.quiz_title = data.title
          this.quiz_public = data.public
          this.time_per_question = data.time_pq
          this.question_per_game = data.qpg
          this.max_contestant = data.max_contestant
          this.currentComp = this.comps["1"]
      },
      finished_2(data){
          this.questions = data
          this.finished = true
          console.log(this.questions)
          data = {
                    creator_id: "",
                    public: this.quiz_public,
                    title: this.quiz_title,
                    timed_per_question: this.timed_per_question,
                    max_contestant: this.max_contestant,
                    question_per_session: this.question_per_game,
                    questions: this.questions
                }
          this.api.post(base_url.base_api_url+"/quiz/create", data
            ).then((resp)=>{
                let data = resp.data
                this.$router.push('/view-quiz/' + data.id)

            }).catch((err)=>{
                this.failed = true
                console.log(err)
                this.err_msg = err.response.data.message
                
            })
      }
  },
  data(){
      return {
          finished: false,
          currentComp: CreateQuizIndex,
          comps:{
              "0": CreateQuizIndex,
              "1": CreateQuizQuestions
          },
          quiz_title: "",
          quiz_public: true,
          time_per_question: 10,
          question_per_game: 10,
          max_contestant: 4,
          questions: []
      }
  }
}
</script>

<style>
</style>