<template>
  <form action="" method="post">
    <div>
        <label>
        Title<br>
        <input required v-model="quiz_title_" type="text" class="outline-0 border h-9 ">
        </label>
    </div>
    <div>
        <label>
        Time per Question (seconds)<br>
        <input required v-model="time_pq" type="number" class="outline-0 border h-9 ">
        </label>
    </div>
    <div>
        <label>
        Question per Game<br>
        <input required v-model="qpg" type="number" class="outline-0 border h-9">
        </label>
    </div>
    <!-- <div>
        <label>
        <input v-model="quiz_public_" type="checkbox" class="outline-0 border"> 
        Public
        </label>
    </div> -->
    <button @click.prevent="change_pg" class="-ml-28 lg:-ml-56 mt-4 px-5 text-white text-lg py-2 bg-black hover:bg-gray-700">Next</button>
  </form>
</template>

<script>
export default {
    'name': 'CreateQuizIndex',
    props: [
        "quiz_title",
        "quiz_public",
        "time_per_question",
        "question_per_game",
        "max_contestant"
    ],
    data(){
        return {
            quiz_title_: this.quiz_title,
            quiz_public_: this.quiz_public,
            time_pq: this.time_per_question,
            qpg: this.question_per_game,
            max_contestant_: this.max_contestant
        }
    },
    methods: {
        change_pg() {
            this.$emit("finished-1", {
                "title": this.quiz_title_,
                "public": this.quiz_public_,
                "time_pq": this.time_pq,
                "qpg": this.qpg,
                "max_contestant": this.max_contestant_
            })
        }
    },
    created(){

    }
}
</script>

<style scoped>
    input.h-9 {
        @apply rounded px-2 lg:w-2/5;
    }

    form > div {
        @apply mt-4;
    }
</style>