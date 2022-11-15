<template>
    <ModalComponent @data="new_question" @hidemodal="show_chg_pwd=false" class="absolute top-52" :show="show_chg_pwd" :comp="chg_comp"/>
    <div class="center mb-4 -mt-4 pt-10 px-1">
        <div class="bg-gray-100 mx-1 w-full md:w-4/5 lg:w-3/5 font-black text-black py-1">
            <div class="text-xl text-red-600" v-if="failed">
                Could not get user data: {{err_msg}}
            </div>
            <div class="grid grid-cols-4 pt-5 pb-2 ">
                <div class="col-span-1">Nickname</div>
                <div class="col-span-3 font-normal">{{profile_data.nickname}}</div>
                <div class="col-span-1">Email</div>
                <div class="col-span-3 font-normal">{{profile_data.email}}</div>
                <div class="col-span-1">ID</div>
                <div class="col-span-3 font-normal">{{profile_data.id}}</div>
                <div class="col-span-1">Telegram Token</div>
                <div class="col-span-3 font-normal break-all">{{tg_token}}</div>
            </div>
            <div class="text-blue-500 text-sm  mt-5">
                <button @click="show_chg_pwd=true" class="disableable  px-5 py-2 underline hover:text-blue-300 rounded-sm" >Change password</button>
                <!-- <button class="disableable ml-2 px-5 py-2 underline hover:text-blue-300 rounded-sm">Invites</button> -->
            </div>
        </div>
    </div>
</template>
<script>
import get_api from '../service/api.js'
import base_url from '../configs/base_url.js'
import ChangePassword from '../components/ChangePassword.vue'
import ModalComponent from '../components/ModalComponent.vue'
export default {
    name: 'MyProfile',
    components: {
        ModalComponent
    },
    data() {
        return {
            show_chg_pwd: false,
            chg_comp: ChangePassword,
            profile_data: {},
            failed: false,
            err_msg: "",
            tg_token: ""
        }
    },
    created() {
      this.api = get_api(this.$router)
      this.api.get(
          base_url.base_api_url+"/users/myprofile"
        ).then((resp)=>{
            let data = resp.data
            this.profile_data = data
          }).catch((err)=>{
            this.failed = true
            console.log(err)
            this.err_msg = err.response.data.message
            this.err_msg = this.err_msg?this.err_msg:err.data
          })
        
        this.api.get(
          base_url.base_api_url+"/users/get_telegram_token"
        ).then((resp)=>{
            let data = resp.data
            this.tg_token = data.token
          }).catch((err)=>{
            this.failed = true
            console.log(err)
            this.err_msg = err.response.data.message
            this.err_msg = this.err_msg?this.err_msg:err.data
          })
    }
}
</script>
<style scoped>
    .grid > div {
        @apply mt-5;
    }
</style>
