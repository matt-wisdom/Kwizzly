<template>
    <div class="md:5/6 lg:h-4/6 flex flex-row flex-shrink-0 flex-wrap md:pl-4 pb-5">
        <router-link :to="'/view-quiz/' + quiz.id" v-for="quiz in quizes" v-bind:key="quiz.id" class="w-4/5 md:w-2/5 lg:w-1/5 shadow rounded-md mx-auto md:mx-2 mt-8 pb-5 hover:scale-110 cursor-pointer bg-gray-200 bg-opacity-100">
            <img src="@/assets/images/i.jpg" alt="">
            <h3 class="my-3 font-black text-lg">{{quiz.title}}</h3> 
            <div class="grid grid-cols-4 text-xs hover:text-gray-400 text-gray-700">
                <div class="col-span-2 border-r border-black">
                    {{quiz.question_per_session}} questions
                </div>
                <div class="col-span-2">
                {{quiz.public?'Public':'Private'}}
                </div>
            </div>               
            <div class="text-xs text-gray-700 mt-2">
                    {{quiz.timed_per_question}}secs/question
                </div>
        </router-link >
    </div>
      
</template>
<script>
export default {
    name: 'ListQuizes',
    props: ['quizes'],
}
</script>
<style scoped>
    
</style>