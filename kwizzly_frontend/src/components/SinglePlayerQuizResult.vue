<template>
    <div class="center text-black py-8 px-12 mt-6">
        You answered {{data.session_data["correct"]}} questions
        correctly which gives you a score of:
        <div class="rounded-full w-28 h-28 bg-black text-white text-3xl center mt-7">
            {{data.session_data["score"]}}%
        </div>
        <div class=" space-2 text-white mt-8">
            <div @click="$router.go()" class="px-5 py-3 bg-black inline-block">
                Play Again
            </div>
            <router-link :to="`/leaderboard/${data.quiz_id}`" class="px-5 py-3 bg-gray-900 mt-3 md:mt-0 inline-block">
                View Leaderboard
            </router-link>>
            <router-link  to="/" class="px-5 py-3 bg-gray-900 inline-block mt-3 md:mt-0">
                Home
            </router-link>
        </div>
    </div>
</template>
<script>
export default {
    name: 'SinglePlayerQuizResult',
    props: ["data",]
}
</script>
<style scoped>
    
</style>