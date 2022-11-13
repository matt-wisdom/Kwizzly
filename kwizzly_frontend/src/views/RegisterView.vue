<template>
  <div class="center my-4 pt-10">
      <div class="bg-white bg-opacity-80 text-black px-4 md:px-1 rounded-md w-4/5 md:w-2/5 md:h-3/5 py-10 animate__animated animate__fadeIn">
      <h1 class="text-3xl bigdeal">Register</h1>
      <div class="md:px-16 mt-8" @keyup.enter="$refs['loginbtn'].click()">
          <div v-if="failed" class="px-6 py-1 border rounded-md border-red-600 bg-red-400">
            Registration Error: {{err_msg}}
          </div>
          <div>
              <label>
                Email:
                <input required v-model="email" type="email" class="outline-0 w-full border h-9">
              </label>
          </div>
          <div>
              <label>
                Username:
                <input required v-model="nickname" type="text" class="outline-0 w-full border h-9">
              </label>
          </div>
          <!-- <div class="mt-5 mb-1 container">
              <div class="grid grid-cols-2 text-xs">
                  <div class="col-span-1"> Password:</div>
                  <div class="col-span-1"> Confirm Password:</div>
              </div>
              <div class="grid grid-cols-2">
                <input required v-model="password1" type="password" class="col-span-1 outline-0 border h-9">
                <input required v-model="password2" type="password" class="col-span-1 outline-0  border h-9">
            </div> -->
          <div>
              <label>
                Password:
                <input required v-model="password1" type="password" class="outline-0 w-full border h-9">
              </label>
          </div>
          <div>
              <label>
                Current Password:
                <input required v-model="password2" type="password" class="outline-0 w-full  border h-9">
              </label>
          </div>
          <button @click="register" class="px-5 text-white text-lg py-2 bg-black hover:bg-gray-700 mt-1">Register</button>
      </div>
      </div>
  </div>
</template>

<script>
import get_api from '../service/api.js'
import base_url from '../service/base_url.js'
export default {
  name: 'RegisterView',
  created(){
      this.api = get_api(this.$router)
      if (localStorage.getItem('access_token')){
        this.$router.push("/")
      }
  },
  methods: {
    register() {
      let email_regexp = /^[^\s@]+@[^\s@]+\.[^\s@]+$/gi
      if (!this.email.match(email_regexp)){
        this.err_msg = "Email Invalid"
        this.failed = true
        return false
      }
      if (this.password1 != this.password2){
        this.err_msg = "Passwords dont match"
        this.failed = true
        return false
      }
      if (this.password1.length < 6) {
            this.err_msg = "Password too short"
            this.failed = true
            return false
      }
      if (this.nickname.length < 4) {
            this.err_msg = "username too short"
            this.failed = true
            return false
      }
      this.failed = false
      this.api.post(base_url.base_api_url+"/users/register", {
        "email": this.email,
        "nickname": this.nickname,
        "password1": this.password1,
        "password2": this.password2
      }).then((resp)=>{
        let data = resp.data
        console.log(data)
        localStorage.setItem("access_token", data["access_token"])
        window.location.reload()
      }).catch((err)=>{
        this.failed = true
        console.log(err)
        this.err_msg = err.response.data.message
        
      })
    }
  },
  data(){
      return {
          failed: false,
          err_msg: '',
          email: '',
          nickname: '',
          password1: '',
          password2: ''
      }
  }
}
</script>

<style scoped>
    label {
        @apply text-xs
    }
</style>