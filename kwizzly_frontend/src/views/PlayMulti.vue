<template>
    <div class="center mb-2 -mt-4">
      <div class="bg-white animate__animated animate__fadeIn bg-opacity-80 text-black lg:px-8 w-5/6 lg:w-3/5 md:h-4/5 py-2">
        <h1 class="font-bold mt-2">Launch Multiplayer Game</h1>
        <span class="text-blue-300">{{msg}}</span>
        <div class="text-lg py-10">
            <div v-if="join_url">
                Game Created. Send this url to friends <br>
                <a :href="join_url" class="mt-5 text-xs text-blue-500 underline block">
                  {{join_url}}
                </a><br>
                <div>
                  <span class="text-sm text-blue-400 block">or input the users id here and invite</span>
                  <input @keypress.enter="invite" type="text" class="outline-0 border h-9 px-3" v-model="invite_uid">
                  <button @click="invite" class="px-2 py-1 hover:bg-gray-600 bg-black text-white">Invite</button>
                </div>
                <br>
                <a :href="join_url" class="bg-green-600 text-2xl mt-5 text-white px-5 hover:bg-green-300 py-2">
                  Start Game
                </a>
            </div>
            <div v-else>
                Starting game
            </div>
            
        </div>
      </div>
    </div>
</template>

<script>
import get_api from "../service/api.js";
import base_url from '../configs/base_url.js';
export default {
  name: "PlayMulti",
  created() {
    let quiz_id = this.$route.params["quiz_id"]
    this.api = get_api(this.$router)

    this.api
        .get(base_url.base_api_url + `/quiz/${quiz_id}/launch-multiplayer`)
        .then((resp) => {
            let data = resp.data
            this.game_id = data.game_id
            this.join_url = `${window.location.origin}/join-multi/${data.game_id}?quiz_id=${data.quiz_id}`
            let again = this.$route.query["again"]
            if (again){
              this.api
                  .get(base_url.base_api_url + `/quiz/invite-again/${again}?game_url=${escape(this.join_url)}`).
                  then(()=>{
                    this.msg = "Users invited"
                  }).catch(() => {this.msg = "Could not invite users"})

            }
        })
        .catch((err) => {
            this.msg = "could not get game url: " + err
        });
  },
  methods: {
    invite(){
      let gurl = base_url.base_api_url + `/quiz/invite/${this.invite_uid}/${this.game_id}?game_url=${escape(this.join_url)}`
      this.api
        .get(gurl)
        .then((resp) => {
            let data = resp.data
            console.log(data)
            this.msg = "Invite sent"
            this.invite_uid = ""
        })
        .catch((err) => {
            this.msg = "Could not invite: " + err
        });
    }
  },
  data() {
    return {
        join_url: null,
        invite_uid: "",
        game_id: null
    }
  },
}
</script>

<style>
    
</style>
