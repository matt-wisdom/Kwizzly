<template>
    <div class="py-4 md:relative bottom-0 w-full animate__animated animate__fadeIn">
        <div class="text-center pt-5 text-sm">
            &copy; Kwizzly 2022
            <div class="space-x-2 cursor-pointer">
                <i class="fab fa-facebook"></i>
                <i class="fab fa-twitter"></i>
                <i class="fab fa-github"></i>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'FooterComponent'
}
</script>

<style scoped>
    .animate__animated.animate__fadeIn {
        --animate-duration: 15s;
    }
</style>
