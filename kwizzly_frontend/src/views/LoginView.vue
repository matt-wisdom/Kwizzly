<template>
  <div class="center my-4 pt-10">
      <div class="bg-white bg-opacity-90 text-black px-4 md:px-1 rounded-md w-4/5 md:w-2/5 md:h-3/5 py-10 animate__animated animate__fadeIn">
      <h1 class="text-3xl bigdeal">Login</h1>
      <div class="md:px-16 mt-8" @keyup.enter="$refs['loginbtn'].click()">
          <div v-if="failed" class="px-6 py-1 border rounded-md border-red-600 bg-red-400">
            Login Error: {{err_msg}}
          </div>
          <div>
              <label>
                Email:
                <input v-model="user" required type="email" class="outline-0 w-full border h-9">
              </label>
          </div>
          <div class="mt-5 mb-1">
              <label>
                  Password:
                <input v-model="password" required type="password" class="outline-0 w-full border h-9">
              </label>
          </div>
          <div class="mb-3"><input type="checkbox" class="outline-0 border h-3 inline-block"> <span class="text-xs">Remember me</span> </div>
          <div class="text-xs mb-1">Don't have an account? <router-link class="underline text-blue-700" to="/register">Register now</router-link></div>
          <button ref="loginbtn" @click="login" class="px-5 text-white text-lg py-2 bg-black hover:bg-gray-700">Login</button>
      </div>
      </div>
  </div>
</template>

<script>
import get_api from '../service/api.js'
import base_url from '../service/base_url.js'
export default {
  name: 'LoginView',
  created(){
      this.api = get_api(this.$router)
  },
  methods: {
      login(){
          this.failed = false;
          this.api.post(base_url.base_api_url+"/users/login", {
            "email": this.user,
            "password": this.password,
          }).then((resp)=>{
            let data = resp.data
            // console.log(data)
            localStorage.setItem("access_token", data["access_token"])
            
            console.log(this.$route.query)
            if (this.$route.query["next"]) {
              this.$router.push(this.$route.query["next"])
            } else {
              this.$router.push("/")
            }
          }).catch((err)=>{
            this.failed = true
            console.log(err)
            this.err_msg = err.response.data.message
          })
      }
  },
  data(){
      return {
          user: '',
          password: '',
          failed: false,
          err_msg: ''
      }
  }
}
</script>

<style>

</style>