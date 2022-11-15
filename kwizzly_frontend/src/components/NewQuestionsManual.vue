<template>
    <div>
        <h4 class="text-lg mt-2 font-bold">New Question</h4>
        <div class="px-2">
            <form action="" method="post">
                <div class="px-4">
                    <label>
                    Question:<br>
                    <textarea v-model="question" required class="outline-0 border h-12 w-full px-4" cols="30" rows="14"></textarea>
                    </label>
                </div>
                <div class="mt-0">
                    <label>
                    Answer<br>
                    <input v-model="answer" type="text" class="outline-0 border h-7 ">
                    <button class="bg-gray-400 px-4 ml-2 py-1 rounded hover:bg-gray-300" @click.prevent="add_answer">
                        Add
                    </button>
                    </label>
                </div>
                <div>
                    <input type="checkbox" v-model="curr_is_correct" class="outline-0 border"> Mark as correct answer
                </div>
            </form>
            <div class="w-full bg-gray-50 px-2 mt-3 h-48 lg:h-24 mb-1 overflow-y-scroll custom-scrollbar">
                    <div v-for="answer, i in answers" v-bind:key="answer" :class="answer == correct?'bg-green-500':'bg-gray-500'" class="rounded-full inline-block w-50 px-2 text-white mt-2 mx-2 py-1 cursor-pointer">
                        <div class="grid grid-cols-12">
                            <div class="col-span-11 break-all  hover:text-gray-800" @dblclick="edit(i)">
                                {{answer}}
                            </div>
                            <div class="text-xs hover:text-red-600 cursor-pointer" @click="remove(i)">
                                X
                            </div>
                        </div>
                    </div>
            </div>
            <button @click="emit_data" class="bg-green-400 hover:bg-green-200 px-5 py-2 lg:-mt-7 -mt-5 rounded">
                Create
            </button>
        </div>
    </div>

</template>

<script>
export default {
    'name': 'NewQuestionsManual',
    props: ["data"],
    data(){
        return {
          answer: "",
          question: "",
          answers: [],
          correct: "",
          curr_is_correct: false
        }
    },
    methods: {
        remove(i){
            this.answers.splice(i, 1)
        },
        add_answer(){
            console.log(this.answer, this.answers)
            if (this.correct == "" && this.curr_is_correct === false){
                this.curr_is_correct = true
            }
            if (this.answer.length > 0) {
                if (this.answers.indexOf(this.answer) != -1){
                    return
                }
                this.answers.push(this.answer)
                if (this.curr_is_correct) {
                    this.correct = this.answer
                }
                this.answer = ""
                this.curr_is_correct = false
            }
        },
        emit_data(){
            this.$emit("data", 
                    {
                        question: this.question,
                        answers: this.answers,
                        correct: this.correct
                    })
        },
        edit(i){
            this.answer = this.answers[i]
            this.answers.splice(i, 1)
        }
    },
    created(){
        console.log(this.$props.data , "data")
        window.gg = this.$props.data
        if (this.$props.data.answers != undefined){
            this.question = this.$props.data.question
            this.answers  = this.$props.data.answers
            this.correct = this.$props.data.correct
        }
    }
}
</script>

<style scoped>
    input.h-9 {
        @apply rounded px-2 lg:w-2/5;
    }
    textarea {
        resize: none
    }

    form > div {
        @apply mt-4;
    }

    .questions {
        height: 43vh;
        max-height: 43vh;
        overflow-y: scroll;
        
    }
</style>