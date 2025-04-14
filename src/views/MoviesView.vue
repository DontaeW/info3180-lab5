<template>
    <div>
      <h1>Movie List</h1>
      <div v-for="movie in movies" :key="movie.id" class="movie-card">
        <img :src="movie.poster" :alt="movie.title" class="movie-poster">
        <h2>{{ movie.title }}</h2>
        <p>{{ movie.description }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  let movies = ref([]); // Create a reactive property to store the movies [cite: 88, 89]
  
  const fetchMovies = () => { // Function to fetch movies from the API [cite: 90, 91, 92]
    fetch('/api/v1/movies')
      .then(response => response.json())
      .then(data => {
        movies.value = data.movies;
      });
  };
  
  onMounted(() => {
    fetchMovies(); // Fetch movies when the component is mounted [cite: 91]
  });
  </script>
  
  <style scoped>
  .movie-card {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
  }
  .movie-poster {
    max-width: 200px;
    height: auto;
  }
  </style>