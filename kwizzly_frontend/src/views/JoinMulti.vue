<template>
    <ModalComponent @hidemodal="show_new_question=false" class="absolute top-52" :data="{session_data: session_data, quiz_id: game_data.id}" :show="show_result" :comp="show_result_comp"/>
    <div class="center mb-4 -mt-4 pt-10 px-1">
        <div class="bg-gray-200 text-black text-sm h-2/5 md:h-1/5 py-1 w-full md:w-4/5 center mb-2 overflow-y-scroll custom-scrollbar ">
            <h4 class="font-black">Scores</h4>
            <div v-for="item in Object.keys(scores).sort((a, b)=>{scores[b].score-scores[a].score})" :key="item" class="grid grid-cols-2">
                <div>
                    {{scores[item]["name"]}}
                </div>
                <div>
                    {{scores[item]["score"]}}
                </div>
            </div>
        </div>
        <div class="bg-gray-100 mx-1 w-full px-3 md:w-4/5 font-black text-black py-5 h-full">
            <div class="text-sm text-green-600 w-full h-10">
                <small class="">{{msg}}</small>
            </div>
            <div>
                <div class="center mb-2 -mt-4">
                    <MultiPlayerQuestion :can_answer="can_answer" :time="10" :question="current_question" :answers="current_answers" @answer="answer" v-if="started&&current_question"/> 
                </div>
            </div>
        </div>
    </div>
</template>
<script>  
import MultiPlayerQuestion from '../components/MultiPlayerQuestion.vue'
import get_api from "../service/api.js";
import base_url from '../configs/base_url.js';
import ModalComponent from "../components/ModalComponent.vue"
import MultiPlayerQuizResult from '../components/MultiPlayerQuizResult.vue'
export default {
    name: "JoinMulti",
    components: {
        MultiPlayerQuestion,
        ModalComponent
    },
    data() {
        return {
            game_id: this.$route.params["gameid"],
            socket: null,
            msg: "Starting",
            show_result: false,
            show_result_comp: MultiPlayerQuizResult,
            started: false,
            state: "onbegin",
            waiting_result: false,
            game_data: {},
            last_answer_correct: false,
            last_answer_why: "",
            answered: 0,
            current_question: "",
            current_answers: [],
            error: false,
            err_msg: "",
            session_data: {},
            countdown: 5,
            countdown_timer: null,
            can_answer: true,
            scores: {}
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
            this.can_answer = false
            this.waiting_result = true
            this.socket.send(
                JSON.stringify(
                    {
                        "type": "my_answer",
                        "answer": answer
                    }
                )
            )
        },
        new_participant(user){
            this.msg = `New participant: ${user.nickname}`
        },
        on_message(event){
            let data = JSON.parse(event.data)
            console.log(data)
            let type = data["type"]
            switch (type) {
                case "timeout":
                    break
                case "metadata":
                    this.game_data = data.data
                    break;
                case "register":
                    this.new_participant(data.user)
                    this.api
                        .get(base_url.base_api_url + `/quiz/game/${this.game_id}/`)
                        .then((resp) => {
                            let data = resp.data
                            console.log(resp)
                            this.game_data.game = data
                        })
                        .catch((err) => {
                            console.log(err)
                        })
                    break;
                case "ended":
                    this.msg = "Can't join. Game already played"
                    this.socket.close()
                    break
                case "no_participant":
                    this.msg = "No participants"
                    this.socket.close()
                    break
                case "already_started":
                    this.msg = "Can't join. Game already started"
                    this.socket.close()
                    break
                case "started":
                    this.state = "started"
                    this.msg = "Game started"
                    break;
                case "start":
                    this.state = "start"
                    break;
                case "game-data":
                    this.game_data.game = data
                    break;
                case "score":
                    this.scores = data.score
                    break;
                case "question":
                    console.log("question set")
                    this.can_answer = true
                    this.msg = "Game started"
                    this.current_question = data.question
                    this.current_answers = data.answers
                    break;
                case "answer-status":
                    this.can_answer = false
                    // this.wrong_answer()
                    // this.waiting_result = false
                    // this.last_answer_correct = data["status"]
                    // if (!this.last_answer_correct){
                    //     this.last_answer_why = data["why"]
                    //     // alert(data["why"])
                    // }
                    // this.corrects = data["corrects"]
                    break;
                case "other-answer-status":
                    // this.other_answer(data.by)
                    break;
                // case "answer-status":
                //     this.waiting_result = false
                //     this.last_answer_correct = data["status"]
                //     if (!this.last_answer_correct){
                //         this.last_answer_why = data["why"]
                //         // alert(data["why"])
                //     }
                //     this.corrects = data["corrects"]
                //     break;
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
        this.api = get_api(this.$router)
        let quiz_id = this.$route.query["quiz_id"]
        this.socket = new WebSocket(`${base_url.base_ws_url}/game/multiplayer?token=${token}&quiz_id=${quiz_id}&game_id=${this.game_id}`)
        
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
