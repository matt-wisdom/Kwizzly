<template>
    <div class="w-full text-black">
        <h1 class="font-black text-lg">Invitation</h1>
        <div class=" mt-16">
            <span class="">{{data.message}}</span>
            <a class="block py-2 my-9 px-3 bg-green-600 hover:bg-green-300 mx-8 md:mx-24" :href="data.url">Click to accept</a>
        </div>
    </div>
</template>
<script>
export default {
    name: "InviteComponent",
    props: [
        "data",
    ],
    created(){
    },
    data() {
        return {
        }
    },
    methods: {
    },
}
</script>
<style scoped>
    
</style>