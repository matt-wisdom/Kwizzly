<template>
    <div class=" ml-1 w-full bg-black md:col-span-1 mt-2 mr-3 md:mr-0 md:mt-0 text-white pt-4">
      <div>
        <b class="text-xl underline text-blue-900">New Videos</b>
        <div class="" style="min-height: 10em">
          <ul class="cursor-pointer mt-3 list-disc">
            <li @click="$router.push('/view/'+item.id)" class="hover:text-blue-900"  :key="item.id" v-for='item in new_'><a><b>{{item.audio_name}}</b></a></li>
          </ul>
        </div>

      </div>
      <div>
        <b class="text-xl underline text-blue-900">Popular Videos</b>
        <div class="" style="min-height: 10em">
          <ul class="cursor-pointer mt-3 list-disc">
            <li @click="$router.push('/view/'+item.id)" class="hover:text-blue-900"  :key="item.id" v-for='item in pop_'><a><b>{{item.audio_name}}</b></a></li>
          </ul>
        </div>
      </div>
    </div>
</template>
  
<script>
  import get_api from "../service/api.js"
  export default {
    name: "SideBar",
    created() {
      this.api = get_api(this.$router)
      this.new_ = this.api.get("https://164.92.212.186:5000/videos/*?new=true&per_page=5")
      .then(resp=>{
        var data = resp.data
        this.new_ = data.results
      })
      this.new_ = this.api.get("https://164.92.212.186:5000/videos/*?popular=true&per_page=5")
      .then(resp=>{
        var data = resp.data
        this.pop_ = data.results
        if (!this.pop_){
          console.log("No pop")
        }
      })
    },
    data() {
      return {
        new_: [],
        pop_: []
      }
    }
  }
</script>

  <style>
  </style>
  