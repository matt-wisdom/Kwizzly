<template>
    <ModalComponent @hidemodal="show_delete=false" class="absolute top-52" :data="{'id': quiz_data.id, 'title': quiz_data.title}"  :comp="delete_comp" :show="show_delete"/>
    <div class="center mb-4 -mt-4 pt-10">
        <div class="bg-white animate__animated animate__fadeIn bg-opacity-80 text-black lg:px-8 rounded-md w-5/6 lg:w-4/5 md:h-4/5 lg:h-3/5 py-5">
            <h2 class="text-3xl font-bold bigdeal">{{quiz_data.title}}</h2>
            <div id="data" class="grid grid-cols-2 font-bold px-4">
                <div class="">
                    {{quiz_data.public?'Public':'Private'}}
                </div>
                <div class="">
                    Maximum Participant: {{quiz_data.max_contestant}}
                </div>
                <div class="">
                    Seconds per Question: {{quiz_data.timed_per_question}} secs
                </div>
                <div class="">
                    Questions per Game: {{quiz_data.question_per_session}} 
                </div>
                <div class="">
                    Created: {{quiz_data.created}}
                </div>
            </div>
            <div class="mt-5">
                <button @click="$router.push(`/play-single/${quiz_data.id}`)" class="px-5 text-white text-lg py-2 bg-gray-900 hover:bg-black">Play</button>
                <button @click="$router.push(`/play-multi/${quiz_data.id}`)" class="ml-3 px-5 text-white text-lg py-2 bg-black hover:bg-gray-700">Play Multiplayer</button>
                <button @click="$router.push(`/leaderboard/${quiz_data.id}`)" class="ml-3 px-5 text-white text-lg py-2 bg-gray-700 hover:bg-gray-900">Leaderboard</button>
                <!-- <button v-if="is_creator" class="ml-3 px-5 text-white text-lg py-2 bg-green-700 hover:bg-green-900">Edit</button> -->
                <button @click="show_delete=true" v-if="is_creator" class="ml-3 px-5 text-white text-lg py-2 bg-red-700 hover:bg-red-900">Delete</button>
            </div>
        </div>
    </div>
</template>

<script>
import get_api from '../service/api.js'
import base_url from '../service/base_url.js'
import ModalComponent from "../components/ModalComponent.vue"
import DeleteQuiz from '../components/DeleteQuiz.vue'
export default {
  name: 'ViewQuiz',
  components: {
      ModalComponent,
  },
  created(){
      this.api = get_api(this.$router)
      let id = this.$route.params["id"]
      this.api.get(base_url.base_api_url+`/quiz/quiz/${id}`).then((resp)=>{
            let data = resp.data
            console.log(resp.data)
            let created = new Date(data.timestamp*1000).toLocaleString()
            this.is_creator = data.is_creator
            this.quiz_data = {
                id: data.id,
                timed_per_question: data.timed_per_question,
                title: data.title,
                question_per_session: data.question_per_session,
                created: created,
                public: data.public,
                max_contestant: data.max_contestant,
                creator_id: data.creator_id
            }
          }).catch((err)=>{
            this.failed = true
            console.log(err)
            this.err_msg = err.response.data.message
          })
  },
  methods: {
  },
  data(){
      return {
          delete_comp: DeleteQuiz,
          show_delete: false,
          is_creator: false,
          quiz_data: {}
      }
  }
}
</script>

<style scoped>
    #data > div {
        border: 1px solid black;
        padding: 10px;
    }
</style>
