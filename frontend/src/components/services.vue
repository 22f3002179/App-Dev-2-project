<template>
  <div class="container-fluid">
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
    <h2 class="text-center">Services</h2>
              <form @submit.prevent="createService">
                <div class="form-group mt-3">
                  <label for="id" class="form-label">Select Service</label>
                  <select class="form-control" id="id" v-model="id" required>
                    <option value="" disabled>Select a service</option>
                    <option v-for="service in mainservices" :key="service.MainServices_id" :value="service.MainServices_id">
                      {{ service.name }}
                    </option>
                  </select>
                </div>
                <div class="form-group">
                <label for="description" class="form-label">Description</label>
                <input type="text" class="form-control" id="description" v-model="description" required />
                </div>
                <div class="form-group">
                <label for="price" class="form-label">Price</label>
                <input type="number" class="form-control" id="price" v-model="price" required />
              </div>
              <button type="submit" class="btn btn-success mt-3">Create Service</button>
              <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
            </form>
              <div class="card shadow-lg">
      <div class="card-header bg-primary text-white">
        <h3 class="mb-0">All Services</h3>
      </div>
      <div class="card-body">
        <table class="table table-striped table-hover">
          <thead class="thead-dark">
            <tr>
              <th>ID</th>
              <th>Service</th>
              <th>Description</th>
              <th>Price</th>
              <th>Edit</th>
              <th>Delete</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in allservices" :key="service.service_id">
              <td>{{ service.service_id }}</td>
              <td>{{ service.service_name }}</td>
              <td>{{ service.description }}</td>
              <td>{{ service.price}}</td>
              <td>
                <router-link :to="{ name: 'EditService', params: { id: service.service_id } }" class="btn btn-primary btn-sm">
                  Edit
                </router-link>
              </td>
  
              <td>
                <button @click="deleteService(service.service_id)" class="btn btn-danger btn-sm">Delete</button>
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
    allservices: [],
    mainservices: [],
    id: '',
    description: '',
    price: '',
    errorMessage: null,
    isAdmin: false,
    showModal: false,
    selectedServiceId: null,
    newDescription: '',
    newPrice: '',
  };
}, created() {
      this.fetchmainServices();
      this.fetchServices();
    },
methods: {
  async fetchmainServices() {
        try {
          const response = await fetch("http://127.0.0.1:5000/api/MainService");
          const result = await response.json();
  
          if (response.ok) {
            this.mainservices = result.services;
          } else {
            this.errorMessage = result.message || "Failed to fetch main services";
          }
        } catch (error) {
          this.errorMessage = "Unable to connect to the server to fetch services.";
        }
      },
      async fetchServices() {
        console.log("Fetching services...");
        try {
          const response = await fetch("http://127.0.0.1:5000/api/adminservice"); 
          console.log("Response status:", response.status);
          const result = await response.json();
          console.log("Response JSON:", result);
  
          if (response.ok) {
            this.allservices = result.services;
            console.log("Services updated in Vue:", this.allservices);
          } else {
            this.errorMessage = result.message || "Failed to fetch all services";
            console.error("Error message:", this.errorMessage);
          }
        } catch (error) {
          this.errorMessage = "Unable to connect to the server to fetch services.";
        }
      },  
  async createService() {
      const payload = {
        id: this.id,
        description: this.description,
        price: this.price,
      };
    try {
      const token = localStorage.getItem("token");
      if (!token) {
      this.errorMessage = "No token found. Please log in again.";
      console.error("Authorization Error: Token is missing.");
      return;
    }
    console.log("token Retrieved:", token);
      const response = await fetch("http://127.0.0.1:5000/api/adminservice", {
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
        alert("Service Created Successfully");
        this.fetchServices();
      }
    } catch (error) {
      this.errorMessage = "Unable to connect to server";
    }
  },
  async deleteService(serviceId) {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5000/api/adminservice/${serviceId}`, {
          method: "DELETE",
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });

        const data = await response.json();
        if (response.status === 200) {
          this.fetchServices();
          this.errorMessage = null; 
        } else {
          this.errorMessage = data.message || "Failed to delete service.";
        }
      } catch (error) {
        console.error("Delete service error:", error);
        this.errorMessage = "Failed to delete service.";
      }
    },
},mounted() {
    this.fetchServices();
    this.fetchmainServices();
  },
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