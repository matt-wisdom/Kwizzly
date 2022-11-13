<template>
  <!-- <h4 class="text-lg">Add Questions</h4> -->
  <ModalComponent @edit_data="edited_data" @data="new_question" @hidemodal="show_new_question=false" class="absolute top-52" :show="show_new_question" :data=edit_data :custom_event="'edit_data'" :comp="new_q"/>
  <form action="" method="post" class="animate__animated animate__fadeIn">
      <button @click.prevent="show_new_question=true" class="px-5 text-white py-2 text-sm bg-gray-900 hover:bg-gray-700">New Question</button>
      <button @click.prevent="change_pg" class="ml-2 mt-1 md:mt-0 px-5 text-sm text-white py-2 bg-gray-700 hover:bg-gray-300">Generate Questions from text</button>
      <div class="questions px-3 custom-scrollbar">
          <div v-for="question, i in questions" v-bind:key="question" class="cursor-pointer">
              <div class="dropdown">
                <div :id="i" class="px-4 py-3 rounded bg-green-100 mt-2 grid grid-cols-12">
                    <p class="col-span-10">{{question["question"]}}</p>
                    <p @click="edit(i)" class="text-xs float-right hover:text-red-700">edit</p>
                    <p @click="remove(i)" class="text-xs float-right hover:text-red-700">X</p>
                </div>
                <ul class="w-screen md:w-auto dropdown-inline-menu hidden pt-1 z-50">
                    <li :class="answer == question['correct']?'bg-green-500':'bg-red-500'" class="grid border-b border-gray-200 grid-cols-12 hover:bg-gray-300" v-bind:key="answer" v-for="answer, j in question['answers']">
                        <a href="#" class="text-sm col-span-10  py-2 px-4 block whitespace-no-wrap">{{answer}}</a>
                        <span @click="remove_answer(i, j)" class="text-xs hover:text-red-700 ml-2">X</span>
                    </li>
                </ul>
              </div>
            </div>
        </div>

      <button @click.prevent="$emit('back')" class="mt-4 px-5 text-white text-lg py-2 bg-black hover:bg-gray-700">Back</button>
    <button @click.prevent="finished" class="ml-2 mt-4 px-5 text-white text-lg py-2 bg-green-700 hover:bg-gray-700">Create Quiz</button>
  </form>
</template>

<script>
import NewQuestionsManual from "../components/NewQuestionsManual.vue"
import ModalComponent from "../components/ModalComponent.vue"
export default {
    'name': 'CreateQuizQuestions',
    components: {
        ModalComponent
    },
    data(){
        return {
          edit_data: {},
          new_q: NewQuestionsManual,
          show_new_question: false,
          questions: [
          ]
        }
    },
    methods: {
        remove(i){
            this.questions.splice(i, 1)
        },
        edited_data(data){
            this.questions.splice(data.index, 1)
            delete data.index
            this.questions.push(data)
            this.edit_data = {}

        },
        edit(i){
            this.edit_data = this.questions[i]
            this.edit_data.index = i
            this.show_new_question = true
        },
        new_question(data){
            this.questions.push(data)
        },
        finished(){
            this.$emit('finished-2', this.questions)
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

    .questions {
        height: 37vh;
        max-height: 37vh;
        overflow-y: scroll;
        
    }
</style>