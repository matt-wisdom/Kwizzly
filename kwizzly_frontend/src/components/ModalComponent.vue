<template>
    <div v-if="show" class="modal-container animate__animated animate__fadeIn " @click.stop="$emit('hidemodal')" style="background-color: #aaaaaaaf">
        <div @click.stop="al" class="modal rounded" style="background-color: #ffffff">
            <component :data="data" class="" :is="comp" @data="emit_data" @hidemodal="$emit('hidemodal')" />
        </div>
    </div>
</template>

<script>
export default {
    'name': 'ModalComponent',
    props: [
        "comp",
        "show",
        "data",
        "custom_event"
    ],
    data(){
        return {
        }
    },
    methods: {
        emit_data(data){
            if (Object.keys(this.data).length){
                this.$emit('hidemodal')
                this.$emit(this.custom_event, data)
            }
            else{
                this.$emit('hidemodal')
                this.$emit('data', data)
            }
        }
    },
}
</script>

<style scoped>
    .animate__animated.animate__fadeIn {
        --animate-duration: 1s;
    }
</style>