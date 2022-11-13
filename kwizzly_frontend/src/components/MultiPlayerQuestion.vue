<template>
    <div class="w-full">
        <!-- <span>{{curr_timeleft}}</span> -->
        <i class="fa fa-clock-o" aria-hidden="true"></i>
        <div class="py-4 bg-black my-3 mx-10 text-white">
            {{question}}
        </div>
        <div class="answers text-2xl mt-8">
            <div @click="selected=i" :class="selected===i?'bg-green-600':'bg-white'" class="hover:scale-110 shadow py-1 mb-3 mx-12 cursor-pointer" v-for="answer, i in answers" v-bind:key="answer">
                {{answer}}
            </div>
        </div>
        <button @click="answer" class="bg-black mt-8 hover:bg-gray-700 text-white px-6 py-2">Next</button>
    </div>
</template>
<script>
export default {
    name: "MultiPlayerQuestion",
    props: [
        "question",
        "answers",
        "time",
        "state",
        "can_answer"
    ],
    created(){
        this.timeout = setInterval(()=>{
            this.curr_timeleft -= 1
            if (this.curr_timeleft < 1){
                this.$emit('timeout')
                this.answer()
            }
            if (!this.timeout_set){
                this.timeout_set = true
                this.$watch('question', 
                    (old, new_value) => {
                        this.curr_timeleft = this.time
                        console.log("new   q", old, new_value)
                        this.timeout = setInterval(()=>{
                        this.curr_timeleft -= 1
                        if (this.curr_timeleft < 1){
                            this.$emit('timeout')
                            this.answer()
                            this.curr_timeleft = this.time
                        }
                    }, 1200)
                })
            }
        }, 1200)
    },
    data() {
        return {
            selected: -1,
            timeout: -1,
            curr_timeleft: this.time,
            timeout_set: false,
        }
    },
    methods: {
        answer(){
            if (!this.can_answer){
                return
            }
            let answer = ""

            if (this.selected !== -1){
                answer = this.answers[this.selected]
                this.$emit('answer', answer)
            }
            console.log("TImeout", this.timeout)
            this.selected = -1
            clearInterval(this.timeout)
            this.curr_timeleft = this.time
        }
    },
}
</script>
<style scoped>
    
</style>