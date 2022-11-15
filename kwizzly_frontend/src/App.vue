<template>
  <ModalComponent id="invite" @hidemodal="show_invite=false" class="absolute top-52" :data="data" :show="show_invite" :comp="invite"/>
  <NavBar/>
  <router-view/>
  <FooterComponent/>  
</template>

<script>
import base_url from './configs/base_url.js'
import NavBar from './components/NavBar.vue'
import FooterComponent from './components/Footer.vue'
import ModalComponent from "./components/ModalComponent.vue"
import InviteComponent from "./components/InviteComponent.vue"
export default {
  name: 'App',
  created(){
    this.start()
    setInterval(() => {
      let token = localStorage.getItem("access_token")
      if (token){
        if (this.socket.readyState === 3){
          this.start()
        }
      }
    }, 15000);
  },
  data() {
    return {
      timeout: 0,
      socket: null,
      invite: InviteComponent,
      show_invite: false,
      data: {}
    }
  },
  methods: {
    start(){
      let token = localStorage.getItem("access_token")
      this.socket = new WebSocket(`${base_url.base_ws_url}/game/notifications?token=${token}`)
      this.socket.addEventListener('open', ()=>{
        console.log("Connected")
      })
      this.socket.addEventListener("message", this.on_message)
    },
    on_message(event){
      let data = JSON.parse(event.data)
      let type = data["type"]
      switch (type) {
        case "invite_multiplayer":
          this.data = {message: data.msg, url: data.url}
          this.show_invite = true
          break;
      }
    }
  },
  components: {
    NavBar,
    FooterComponent,
    ModalComponent
  }
}
</script>

<style>
@font-face {
    font-family: bigdeal;
    src: url("@/assets/fonts/aBigDeal.ttf");
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
}
nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

#invite {
  z-index: 4444444;
}
</style>
