<template>
      <div class="container-fluid">
      <!-- Navbar -->
      <nav class="navbar">
        <a href="#" class="navbar-brand">Admin Dashboard</a>
        <div class="navbar-links">
          <a href="/admindashboard" class="btn">Home</a>
          <a href="/mainservices" class="btn">Main Services</a>
          <a href="/services" class="btn">Services</a>
          <a href="/Professionals_Customers" class="btn">Professionals/Customers</a>
        </div>
      </nav>
    </div>
  <div class="container">
    <h2 class="text-center">Main Services</h2>
              <form @submit.prevent="Mainservice">
              <div class="form-group">
                <label for="name" class="form-label">Service Name</label>
                <input type="text" class="form-control" id="name" v-model="name" required />
              </div>
              <button type="submit" class="btn btn-success mt-3">Create Service</button>
              <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
            </form>
              <div class="card shadow-lg">
      <div class="card-header bg-primary text-white">
        <h3 class="mb-0">All Main Services</h3>
      </div>
      <div class="card-body">
        <table class="table table-striped table-hover">
          <thead class="thead-dark">
            <tr>
              <th>ID</th>
              <th>Main Service</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in mainServices" :key="service.MainServices_id">
              <td>{{ service.MainServices_id }}</td>
              <td>{{ service.name }}</td>
              <td>
                <button @click="deleteService(service.MainServices_id)" class="btn btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>  
  </div>  
</template>

<script>
export default {
data() {
  return {
    name: '',
    mainServices: [],
    errorMessage: null,
    isAdmin: false,
  };
},
methods: {
  async fetchMainServices() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/MainService");
        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();
        this.mainServices = data.services || data; 
        this.errorMessage = null; 
      } catch (error) {
        console.error("Fetch error:", error);
        this.errorMessage = "Failed to fetch services";
      }
    },
    async deleteService(serviceId) {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5000/api/MainService/${serviceId}`, {
          method: "DELETE",
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });

        const data = await response.json();
        if (response.status === 200) {
          this.fetchMainServices();
          this.errorMessage = null; 
        } else {
          this.errorMessage = data.message || "Failed to delete service.";
        }
      } catch (error) {
        console.error("Delete service error:", error);
        this.errorMessage = "Failed to delete service.";
      }
    },
  async Mainservice() {
    const payload = {
      name: this.name,
    };

    try {
      const token = localStorage.getItem("token");
      if (!token) {
      this.errorMessage = "No token found. Please log in again.";
      console.error("Authorization Error: Token is missing.");
      return;
    }

    console.log("token Retrieved:", token);
      const response = await fetch("http://127.0.0.1:5000/api/MainService", {
        method: "POST",
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload)
      });

      const result = await response.json();
      console.log("Server Response:", result);
      if (!response.ok) {
        this.errorMessage = result.message || "Something went wrong";
      } else {
        alert("Main Service Created Successfully");
        this.fetchMainServices();
      }
    } catch (error) {
      this.errorMessage = "Unable to connect to server";
    }
  }
},mounted() {
  this.fetchMainServices();
}
};
</script>

<style scoped>
 
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  color: white;
}

.navbar-brand {
  font-size: 24px;
}

.navbar-actions {
  display: flex;
  gap: 10px;
}

.navbar-links {
  display: flex;
  gap: 15px;
}

.navbar-actions .btn, .navbar-links .btn {
  background-color: #5c6bc0;
  color: white;
  border: none;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  border-radius: 5px;
}

.navbar-actions .btn:hover, .navbar-links .btn:hover {
  background-color: #3f4f98;
}

.navbar-actions .btn.btn-danger {
  background-color: #e53935;
}

.navbar-actions .btn.btn-danger:hover {
  background-color: #c62828;
}


.navbar-actions .btn.btn-export {
  background-color: #4caf50;
}

.navbar-actions .btn.btn-export:hover {
  background-color: #45a049;
}


.small-table {
  width: 60%;
  margin: 0 auto;
  font-size: 14px;
}

.small-table th, .small-table td {
  text-align: center;
  padding: 8px 12px;
}

.small-table th {
  background-color: #333;
  color: white;
}

.small-table td {
  background-color: #f4f4f4;
}
</style>