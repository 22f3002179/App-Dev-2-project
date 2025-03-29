
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
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Login</div>
          <div class="card-body">
            <form @submit.prevent="Login">

              
              <!-- Email Input -->
              <div class="form-group">
                <label for="email_id" class="form-label">Email</label>
                <input type="email" class="form-control" id="email_id" v-model="email_id" required />
              </div>

              <!-- Password Input -->
              <div class="form-group mt-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required />
                <small id="passwordHelp" class="form-text text-muted">
                </small>
              </div>

              <!-- Role Selection -->
              <div class="form-group mt-3">
                <label for="role" class="form-label">Select Your Role</label>
                <select id="role" class="form-control" v-model="role" required>
                  <option value="">-- Select Role --</option>
                  <option value="admin">admin</option>
                  <option value="professional">professional</option>
                  <option value="customer">customer</option>
                </select>
              </div>

              <!-- Error Message -->
              <div v-if="errorMessage" class="text-danger mt-2">
                {{ errorMessage }}
              </div>

              <!-- Submit Button -->
              <button type="submit" class="btn btn-primary mt-3">Login</button>

            </form>
          </div>
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
      email_id: '',
      password: '',
      role: '',
      errorMessage: null
    };
  },
  methods: {
    async Login() {
      this.errorMessage = null;

      const payload = {
        email_id: this.email_id,
        password: this.password,
        role: this.role
      };
      console.log("Sending payload:", payload);

      try {
        // Sending POST request to the backend
        const response = await fetch("http://127.0.0.1:5000/api/Login", {
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
          alert("Login Successful");
          console.log("token Received:", result.token);
          if (result.token) {
           localStorage.setItem("token", result.token);
           localStorage.setItem("email_id", result.email_id);
           localStorage.setItem("role", result.role); 
           console.log("token stored successfully!");
          } else {
             console.error("No token received from server");
          }

          if (result.role === 'customer') {
            this.$router.push('/customerdashboard');
          } else if (result.role === 'admin') {
            this.$router.push('/admindashboard');
          } else if (result.role === 'professional') {
            this.$router.push('/professionaldashboard'); 
          } else {
            this.errorMessage = "Unknown role"; 
          }
        }
      } catch (error) {
        console.error("Login Error:", error);
        this.errorMessage = "Unable to connect to server";
      }
    }
  }
};
</script>