<template>
    <div class="container py-5">
      <div class="card shadow-lg p-4">
        <h2 class="mb-4 text-center">🎬 Add a New Movie</h2>
  
        <form id="movieForm" @submit.prevent="saveMovie">
          <div class="mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input
              type="text"
              name="title"
              class="form-control"
              v-model="title"
            />
          </div>
  
          <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea
              name="description"
              class="form-control"
              rows="3"
              v-model="description"
            ></textarea>
          </div>
  
          <div class="mb-3">
            <label for="poster" class="form-label">Poster</label>
            <input type="file" class="form-control" @change="handleFileUpload" />
          </div>
  
          <button type="submit" class="btn btn-primary w-100">Submit</button>
        </form>
  
        <!-- Success or Fail message -->
        <div v-if="response" class="mt-4">
          <div v-if="response.message" class="alert alert-success">
            {{ response.message }}
          </div>
          <div v-if="response.errors" class="alert alert-danger">
            <ul class="mb-0">
              <li v-for="(error, index) in response.errors" :key="index">
                {{ error }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  
  const title = ref("");
  const description = ref("");
  const poster = ref(null);
  const csrf_token = ref("");
  const response = ref(null);
  
  function handleFileUpload(e) {
    poster.value = e.target.files[0];
  }
  
  function getCsrfToken() {
    fetch("/api/v1/csrf-token")
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
      });
  }
  
  function saveMovie() {
    let form = document.getElementById("movieForm");
    let formData = new FormData(form);
    formData.append("title", title.value);
    formData.append("description", description.value);
    formData.append("poster", poster.value);
  
    fetch("/api/v1/movies", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": csrf_token.value,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        response.value = data;
        console.log(data);
        if (data.message) {
          //  Reset fields if submission was successful
          title.value = "";
          description.value = "";
          poster.value = null;
  
          // Clear file input
          form.reset();
        }
      })
      .catch((err) => {
        console.error(err);
      });
  }
  
  onMounted(() => {
    getCsrfToken();
  });
  </script>