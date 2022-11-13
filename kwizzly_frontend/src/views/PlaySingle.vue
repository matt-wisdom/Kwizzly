<template>
    <ModalComponent @hidemodal="show_new_question=false" class="absolute top-52" :data="{session_data: session_data, quiz_id: game_data.id}" :show="show_result" :comp="show_result_comp"/>
    <div class="center mb-2 -mt-4">
      <div class="bg-white animate__animated animate__fadeIn bg-opacity-80 text-black lg:px-8 w-5/6 lg:w-3/5 md:h-4/5 py-2">
        <h1 class="font-bold">{{game_data.title}}</h1>
        <div class="grid grid-rows-2">
            <div>{{game_data.questions}} Questions</div>
            <div>Correct: {{corrects}} out of {{answered}}</div>
        </div>
        <div>

        </div>
      </div>
    </div>
    <div class="center mb-4 -mt-4 pt-7">
        
      <div class="bg-white animate__animated animate__fadeIn bg-opacity-80 text-black lg:px-8 rounded-md w-5/6 lg:w-3/5 md:h-4/5 py-5">
          <SinglePlayerQuestion :time="10" :question="current_question" :answers="current_answers" @answer="answer" v-if="started"/> 
          <div v-else class="text-xl center">
              Game begins in:
              <div class="rounded-full w-28 h-28 bg-black text-white text-3xl center mt-7">
                {{countdown}}
              </div>
          </div>
      </div>
    </div>
</template>
<script>
import base_url from '../service/base_url.js'
import SinglePlayerQuestion from '../components/SinglePlayerQuestion.vue'
import ModalComponent from "../components/ModalComponent.vue"
import SinglePlayerQuizResult from '../components/SinglePlayerQuizResult.vue'
export default {
    name: "PlaySingle",
    components: {
        SinglePlayerQuestion,
        ModalComponent
    },
    data() {
        return {
            socket: null,
            show_result: false,
            show_result_comp: SinglePlayerQuizResult,
            started: false,
            state: "onbegin",
            waiting_result: false,
            game_data: {},
            score: 0,
            corrects: 0,
            last_answer_correct: false,
            last_answer_why: "",
            answered: 0,
            current_question: "",
            current_answers: [],
            error: false,
            err_msg: "",
            session_data: {},
            countdown: 5,
            countdown_timer: null
        }  
    },
    methods: {
        finished(data){
            console.log(data)
            this.session_data = data
            this.show_result = true
        },
        answer(answer){
            console.log(answer)
            this.answered += 1
            this.waiting_result = true
            this.socket.send(
                JSON.stringify(
                    {
                        "type": "answer",
                        "answer": answer
                    }
                )
            )
        },
        on_message(event){
            let data = JSON.parse(event.data)
            console.log(data)
            let type = data["type"]
            switch (type) {
                case "metadata":
                    if (this.state != "started_sent"){
                        this.socket.close()
                        this.error = true
                        this.err_msg = "Game not started"
                    }
                    this.game_data = data.data
                    this.state = "started"
                    break;
                case "question":
                    console.log("NEW QQQQQQQ")
                    this.current_question = data.question
                    this.current_answers = data.answers
                    break;
                case "answer-status":
                    this.waiting_result = false
                    this.last_answer_correct = data["status"]
                    if (!this.last_answer_correct){
                        this.last_answer_why = data["why"]
                        // alert(data["why"])
                    }
                    this.corrects = data["corrects"]
                    break;
                case "finished":
                    this.finished(data.data)
                    this.state = "finished"
                    break;
                default:
                    break;
            }
        }
    },
    created() {
        let token = localStorage.getItem("access_token")
        let quiz_id = this.$route.params["quiz_id"]
        this.socket = new WebSocket(`${base_url.base_ws_url}/game/singleplayer?token=${token}&quiz_id=${quiz_id}`)
        
        this.socket.addEventListener('open', (event)=>{
            console.log(event)
            this.countdown_timer = setInterval(() => {
                if (this.countdown < 1){
                    clearInterval(this.countdown_timer)
                    return
                }
                this.countdown -= 1
            }, 1000);
            setTimeout(() => {
                this.started = true
                this.socket.send(
                JSON.stringify(
                    {
                        "type": "start"
                    }
                    )
                )
                this.state = "started_sent"
            }, 5000)
        })

        this.socket.addEventListener("message", this.on_message)
    },
}
</script>
<style>
    
</style>
