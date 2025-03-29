<template>
    <div class="card-body">
        <blockquote class="blockquote mb-0">
          <div class="d-flex flex-column gap-3">
            <router-link to="/" class="btn btn-primary">Home Page</router-link>
          </div>
        </blockquote>
      </div>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">ProfessionalSignup</div>
            <div class="card-body">
              <form @submit.prevent="ProfessionalSignup">
                
                <!-- Full Name Input -->
                <div class="form-group">
                  <label for="full_name" class="form-label">Full Name</label>
                  <input type="text" class="form-control" id="full_name" v-model="full_name" required />
                </div>
                
                <!-- Email Input -->
                <div class="form-group mt-3">
                  <label for="email" class="form-label">Email</label>
                  <input type="email" class="form-control" id="email" v-model="email" required />
                </div>
                
                <!-- Password Input -->
                <div class="form-group mt-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" class="form-control" id="password" v-model="password" required />
                  <small class="form-text text-muted">We'll never share your password with anyone else.</small>
                </div>
                
                <!-- Experience Input -->
                <div class="form-group mt-3">
                  <label for="experience" class="form-label">Experience</label>
                  <input type="text" class="form-control" id="experience" v-model="experience" required />
                </div>
                
                <!-- Address Input -->
                <div class="form-group mt-3">
                  <label for="address" class="form-label">Address</label>
                  <input type="text" class="form-control" id="address" v-model="address" required />
                </div>
                
                <!-- Pin Code Input -->
                <div class="form-group mt-3">
                  <label for="pin_code" class="form-label">Pin Code</label>
                  <input type="text" class="form-control" id="pin_code" v-model="pin_code" required />
                </div>
                
                <!-- Service ID Input -->
                <div class="form-group mt-3">
                  <label for="service_id" class="form-label">Select Service</label>
                  <select class="form-control" id="service_id" v-model="service_id" required>
                    <option value="" disabled>Select a service</option>
                    <option v-for="service in services" :key="service.MainServices_id" :value="service.MainServices_id">
                      {{ service.name }}
                    </option>
                  </select>
                </div>
                
                <!-- Supporting Documents Input -->
                <div class="form-group mt-3">
                  <label for="supporting_documents" class="form-label">Supporting Documents</label>
                  <input type="text" class="form-control" id="supporting_documents" v-model="supporting_documents" required />
                </div>
                
                <!-- Error Message -->
                <div v-if="errorMessage" class="text-danger mt-2">
                  {{ errorMessage }}
                </div>
                <div v-if="successMessage" class="text-success mt-2">
                  {{ successMessage }}
                </div>
                
                <!-- Submit Button -->
                <button type="submit" class="btn btn-success mt-3">Sign Up</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        full_name: '',
        email: '',
        password: '',
        experience: '',
        address: '',
        pin_code: '',
        services: [],
        service_id: '',
        supporting_documents: '',
        errorMessage: null,
        successMessage: null
      };
    }, 
    created() {
      this.fetchServices();
    },
    methods: {
      async ProfessionalSignup() {
        this.errorMessage = null;
        this.successMessage = null;
  
        const payload = {
          full_name: this.full_name,
          email: this.email,
          password: this.password,
          experience: this.experience,
          address: this.address,
          pin_code: this.pin_code,
          service_id: this.service_id,
          supporting_documents: this.supporting_documents,
          role: "professional"
        };
  
        try {
          const response = await fetch("http://127.0.0.1:5000/api/professionalSignup", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
          });
  
          const result = await response.json();
  
          if (!response.ok) {
            this.errorMessage = result.message || "Something went wrong";
          } else {
            alert(result.message);
            this.$router.push('/LoginPage');
          }
        } catch (error) {
          this.errorMessage = "Unable to connect to server";
        }
      },
  
      async fetchServices() {
        try {
          const response = await fetch("http://127.0.0.1:5000/api/MainService");
          const result = await response.json();
  
          if (response.ok) {
            this.services = result.services;
          } else {
            this.errorMessage = result.message || "Failed to fetch services";
          }
        } catch (error) {
          this.errorMessage = "Unable to connect to the server to fetch services.";
        }
      },
    },
  };
  </script>
  
