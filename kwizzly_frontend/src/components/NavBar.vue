<template>
  <div class="cursor-pointer  w-screen top-0 grid  grid-rows-1 md:grid-cols-6 md:h-16 py-2 z-50 mb-14">
    <div class="row-span-1 md:pt-2  lg:col-span-2">
        <div class="md:float-left">
        </div>
    </div>
    
    <div class="md:col-span-2 grid md:grid-cols-4 animate__animated animate__fadeIn">
      <router-link to="/" class="md:mt-0 md:pt-2 mt-1 hover:bg-gray-700">Home</router-link>
      <router-link class="md:mt-0 md:pt-2 mt-1 md:ml-3 hover:bg-gray-700" to="/create-quiz"> Create Quiz </router-link>
      <router-link class="md:mt-0 md:pt-2 mt-1 md:ml-3 hover:bg-gray-700" to="/quizes"> Quizes </router-link>
      <router-link class="md:mt-0 md:pt-2 mt-1 md:ml-5 hover:bg-gray-700" to="/about"> About </router-link>
    </div>
    <div class="md:col-span"></div>
    <div class="md:col-span-1 grid  grid-cols-2 text-sm auth animate__animated animate__fadeIn" v-if="no_auth">
            <router-link to="/login" class="md:mt-0 md:pt-2  md:px-0.5 hover:text-gray-700"> Login </router-link>
            <router-link class="md:mt-0 -ml-16 md:pt-2 md:px-0.5 md:ml-3 lg:-ml-16 hover:text-gray-700" to="/register"> Register </router-link>
    </div>
    <div class="md:col-span-1 grid  grid-cols-2 text-sm auth animate__animated animate__fadeIn" v-else>
            <router-link to="/my-profile" class="md:mt-0 md:pt-2  md:px-0.5 hover:text-gray-700"> My Profile </router-link>
            <div @click="logout" class="md:mt-0 md:pt-2  md:px-0.5 hover:text-gray-700"> Log out </div>
    </div>
  </div>
</template>

<script>
import get_api from "../service/api.js"
export default {
  name: "NavBar",
  created() {
      this.api = get_api(this.$router)
      this.new_ = this.api.get("https://164.92.212.186:5000/videos/*?playlists_only=true")
      .then(resp=>{
        var data = resp.data
        this.plist_ = data["playlists"]
        console.log("dddd")
        console.log(this.plist_)
      })
  },
  data(){
    return {
      plist_: []
    }
  },
  methods: {
    logout(){
      localStorage.removeItem("access_token")
      this.$router.push("/")
      window.location.reload()
    }
  },
  computed: {
    no_auth() {
      return localStorage.getItem('access_token')?false:true
    }
  }
};
</script>

<style scoped>
  * {
    font-family: bigdeal;
  }

  .auth > * {
    font-family: Arial, Helvetica, sans-serif;
    font-weight: bolder;
  }
 .navbar-icon > i  {
   font-size: 4em;
 }

 .animate__animated.animate__fadeIn {
    --animate-duration: 2s;
  }

  .animate__animated.animate__fadeIn.auth {
    --animate-duration: 4s;
  }
</style>
