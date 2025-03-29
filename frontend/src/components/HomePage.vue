<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card text-center p-4">
      <div class="card-header">
        Welcome to Household Service App
      </div>
      <div class="card-body">
        <blockquote class="blockquote mb-0">
          <div class="d-flex flex-column gap-3">
            <router-link to="/LoginPage" class="btn btn-primary">Login</router-link>
            <router-link to="/ProfessionalSignup" class="btn btn-secondary">Register as a Professional</router-link>
            <router-link to="/CustomerSignup" class="btn btn-danger">Register as a Customer</router-link>
          </div>
        </blockquote>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
};
</script>
