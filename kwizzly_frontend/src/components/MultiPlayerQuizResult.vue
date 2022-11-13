<template>
    <div class="center text-black py-8 px-12 mt-6">
        <!-- <div class="rounded-full w-28 h-28 bg-black text-white text-3xl center mt-7"> -->
        <!-- </div> -->
        <h1 class="text-xl font-black">Final Scores</h1>
        <div class="">
            <div v-for="item in Object.keys(this.data.session_data['score']).sort((a, b)=>{this.data.session_data['score'][b].score-this.data.session_data['score'][a].score})" :key="item" class="grid grid-cols-2">
                <div>
                    {{data.session_data['score'][item]["name"]}}
                </div>
                <div>
                    {{data.session_data['score'][item]["score"]}}
                </div>
            </div>
        </div>
        <div class=" space-2 text-white mt-8">
            <div @click="$router.push(`/play-multi/${$route.query['quiz_id']}?again=${$route.params['gameid']}`)" class="px-5 py-3 bg-black inline-block">
                Play Again
            </div>
            <router-link  to="/" class="px-5 ml-2 py-3 bg-gray-900 inline-block mt-3 md:mt-0">
                Home
            </router-link>
        </div>
    </div>
</template>
<script>
export default {
    name: 'MultiPlayerQuizResult',
    props: ["data"],
}
</script>
<style scoped>
    
</style>