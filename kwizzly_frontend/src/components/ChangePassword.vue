<template>
    <div class="text-black py-4">
        <h1>Change password</h1>
        <form action="" method="post">
            <div v-if="failed" class=" mx-3 px-6 py-1 border rounded-md border-red-600 bg-red-400">
                Change Password Error: {{err_msg}}
            </div>
            <div>
                <label>
                Email<br>
                <input required v-model="email" type="text" class="outline-0 border h-9 ">
                </label>
            </div>
            <div>
                <label>
                Current Password<br>
                <input required v-model="old_password" type="password" class="outline-0 border h-9 ">
                </label>
            </div>
            <div>
                <label>
                New Password<br>
                <input required v-model="new_password" type="password" class="outline-0 border h-9">
                </label>
            </div>
            <div>
                <label>
                Confirm New Password<br>
                <input required v-model="new_password2" type="password" class="outline-0 border h-9">
                </label>
            </div>
            <button @click.prevent="change_pword" class="mt-4 px-5 text-white text-lg py-2 bg-black hover:bg-gray-700">Change</button>
        </form>
    </div>
</template>
<script>
import get_api from '../service/api.js'
import base_url from '../service/base_url.js'
export default {
    name: 'ChangePassword',
    data() {
        return {
            email: "",
            old_password: "",
            new_password: "",
            new_password2: "",
            err_msg: "",
            failed: false
        }
    },
    methods: {
        change_pword(){
            this.api.post(
            base_url.base_api_url+"/users/change-password",
            {
                email: this.email,
                old_password: this.old_password,
                new_password: this.new_password,
                new_password2: this.new_password2
            }
            ).then((resp)=>{
                let data = resp.data
                this.profile_data = data
                this.$emit('hidemodal')
            }).catch((err)=>{
                this.failed = true
                console.log(err)
                this.err_msg = err.response.data.message
                this.err_msg = this.err_msg?this.err_msg:err.data
            })
        }
    },
    created() {
      this.api = get_api(this.$router)
      
    }
}
</script>
<style scoped>
    
</style>