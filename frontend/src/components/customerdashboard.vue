<template>
    <div class="container-fluid">
      <!-- Navbar -->
      <nav class="navbar">
        <a href="#" class="navbar-brand">Customer Dashboard</a>
        <div class="navbar-links">
          <a href="/customerdashboard" class="btn">Home</a>
          <a href="/MyBookings" class="btn">My Bookings</a>
          <a href="/MyProfile_Customer" class="btn">My Profile</a>
        </div>
        <div class="navbar-actions">
          <button class="btn btn-danger" @click="logout">Logout</button>
        </div>
      </nav>
    </div>
    <div class="container">

    
<!-- Display Available Services with Search Functionality -->
<div v-if="services.length > 0">
  <h4>Select a Service</h4>
  
  <!-- Search Input -->
  <input type="text" v-model="searchQuery" placeholder="Search by name, price, or description" class="form-control mb-3" />

  <table class="table table-bordered">
    <thead>
      <tr>
        <th>Service Name</th>
        <th>Price</th>
        <th>Description</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="service in filteredServices" :key="service.service_id">
        <td>{{ service.service_name }}</td>
        <td>{{ service.price }}</td>
        <td>{{ service.description }}</td>
        <td>
          <button @click="selectService(service)" class="btn btn-primary btn-sm">Book</button>
        </td>
      </tr>
    </tbody>
  </table>
</div>
    
    <!-- Booking Form -->
    <div v-if="selectedService">
      <h3>Booking Details</h3>
      <form @submit.prevent="bookService">
        <div class="form-group">
          <label>Service:</label>
          <input type="text" v-model="selectedService.service_name" class="form-control" disabled>
        </div>
        <div class="form-group">
          <label>Phone Number:</label>
          <input type="text" v-model="phone_number" class="form-control" required>
        </div>
        <div class="form-group">
          <label>Location:</label>
          <input type="text" v-model="location" class="form-control" required>
        </div>
        <div class="form-group">
          <label>Pincode:</label>
          <input type="text" v-model="pincode" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-success">Confirm Booking</button>
      </form>
      <p v-if="message" class="mt-3">{{ message }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      services: [],  
      selectedService: null,  
      date_of_request: "",
      phone_number: "",
      location: "",
      pincode: "",
      message: "",
      searchQuery: "",
    };
  },computed: {
    filteredServices() {
      return this.services.filter(service => {
        const query = this.searchQuery.toLowerCase();
        return (
          service.service_name.toLowerCase().includes(query) ||
          service.price.toString().includes(query) ||
          service.description.toLowerCase().includes(query)
        );
      });
    }
  },
  methods: {
    async logout() {
        localStorage.removeItem('Token');
        this.$router.push('/');
      },
    async fetchServices() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/adminservice");
        const data = await response.json();
        this.services = data.services || [];
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    selectService(service) {
      this.selectedService = service;
    },
    async bookService() {
      try {
        const token = localStorage.getItem("token");
        const payload = {
          phone_number: this.phone_number,
          location: this.location,
          pincode: this.pincode,
          service_id: this.selectedService.service_id,
        };

        const response = await fetch("http://127.0.0.1:5000/api/booking", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const data = await response.json();
        this.message = data.message || "Booking successful!";

        if (response.ok) {
          this.selectedService = null;
          this.date_of_request = "";
          this.phone_number = "";
          this.location = "";
          this.pincode = "";
        }
      } catch (error) {
        console.error("Booking error:", error);
        this.message = "Failed to book service.";
      }
    }
  },
  mounted() {
    this.fetchServices();
  }
};
</script>

<style scoped>
.container-fluid {
  background: #f8f9fa;
  padding: 10px;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #007bff;
  padding: 10px 20px;
  border-radius: 5px;
}

.navbar-brand {
  font-size: 1.5rem;
  color: #fff;
  font-weight: bold;
}

.navbar-links a,
.navbar-actions button {
  margin-left: 10px;
  color: white;
}

.container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.subtitle {
  margin-bottom: 10px;
  color: #555;
}

.table {
  width: 100%;
  margin-top: 10px;
}

.btn {
  padding: 5px 10px;
  font-size: 14px;
}

.booking-form {
  margin-top: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.message {
  color: green;
  font-weight: bold;
  text-align: center;
  margin-top: 10px;
}
</style>
