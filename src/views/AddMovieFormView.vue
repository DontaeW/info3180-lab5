<script setup>
import { ref } from "vue";
import MovieForm from "@/components/MovieForm.vue";

</script>

<template>
    <div class="container">
        <h1>Movie Form</h1>
        <MovieForm/>
    </div>
</template>

<style>
.container{
    display: flex;
    flex-direction: column;
    align-items: center;
}
.container{
    width:80vw;
    height: 80vh;
}
</style>