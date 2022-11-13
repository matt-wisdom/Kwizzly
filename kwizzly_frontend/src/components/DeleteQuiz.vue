<template>
    <div class="text-black pt-8">
        <h1 class="font-black mb-12">Delete quiz: {{data.title}}</h1>
        <p class="text-lg mt-12 mb-7">
            Are you sure you want to delete this quiz?
        </p>
        <button @click="delete_quiz" class="py-3 px-4 bg-red-600 rounded hover:bg-red-300">
            Delete
        </button>
        <button @click="$emit('hidemodal')" class="py-3 px-4 bg-gray-600 ml-2 rounded hover:bg-gray-300">
            Cancel
        </button>
    </div>
</template>
<script>
import get_api from '../service/api.js'
import base_url from '../service/base_url.js'
export default {
    name: 'DeleteQuiz',
    props: ["data"],
    methods: {
        delete_quiz(){
            this.api.delete(
                base_url.base_api_url+`/quiz/${this.data.id}/delete`,
            ).then((resp)=>{
            let data = resp.data
            console.log(data)
            this.$router.push("/")
          }).catch((err)=>{
            this.failed = true
            console.log(err)
            this.err_msg = err.response.data.message
          })
        }
    },
    created(){
      this.api = get_api(this.$router)
    }
}
</script>
<style scoped>
    
</style>