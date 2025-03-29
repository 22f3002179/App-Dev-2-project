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
            <div class="card-header">CustomerSignup</div>
            <div class="card-body">
              <form @submit.prevent="CustomerSignup">
                
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
      address: '',
      pin_code: '',
      errorMessage: null,
      successMessage: null
    };
  },
  methods: {
    async CustomerSignup() {
      this.errorMessage = null;
      this.successMessage = null;
      
      const payload = {
        full_name: this.full_name,
        email: this.email,
        password: this.password,
        address: this.address,
        pin_code: this.pin_code,
        role: 'customer'
      };
      
      try {
        // Sending POST request to the backend
        const response = await fetch("http://127.0.0.1:5000/api/CustomerSignup", {
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
          alert("Signup Successful");
          this.$router.push('/LoginPage');
        }
      } catch (error) {
        // Handle network errors or other issues
        this.errorMessage = "Unable to connect to server";
      }
    }
  }
};
</script>
