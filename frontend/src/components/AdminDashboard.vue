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
      <div class="navbar-actions">
        <button class="btn btn-export" @click="exportCSV">Export CSV</button>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </div>
    </nav>
  </div>

  <!-- Search Input -->
  <div class="container-fluid mt-3">
    <input
      type="text"
      v-model="searchQuery"
      class="form-control"
      placeholder="Search bookings by Phone Number, Status, location, or pincode"
    />
  </div>

  <!-- All Bookings Table -->
  <div class="card shadow-lg mt-3">
    <div class="card-header bg-primary text-white">
      <h3 class="mb-0">All Bookings</h3>
    </div>
    <div class="card-body">
      <table class="table table-striped table-hover small-table">
        <thead class="thead-dark">
          <tr>
            <th>Booking ID</th>
            <th>Date of Request</th>
            <th>Date of Completion</th>
            <th>Phone Number</th>
            <th>Status</th>
            <th>Location</th>
            <th>Pincode</th>
            <th>Rating</th>
            <th>Professional ID</th>
            <th>Customer ID</th>
            <th>Service ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in filteredBookings" :key="service.booking_id">
            <td>{{ service.booking_id }}</td>
            <td>{{ service.date_of_request }}</td>
            <td>{{ service.date_of_completion }}</td>
            <td>{{ service.phone_number }}</td>
            <td>{{ service.status }}</td>
            <td>{{ service.location }}</td>
            <td>{{ service.pincode }}</td>
            <td>{{ service.rating }}</td>
            <td>{{ service.professional_id }}</td>
            <td>{{ service.customer_id }}</td>
            <td>{{ service.service_id }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      bookings: [],
      searchQuery: "",
      errorMessage: null
    };
  },
  computed: {
    // filter bookings based on search query
    filteredBookings() {
      if (!this.searchQuery) {
        return this.bookings;
      }
      const query = this.searchQuery.toLowerCase();
      return this.bookings.filter(service => {
        return Object.values(service).some(value =>
          String(value).toLowerCase().includes(query)
        );
      });
    }
  },
  methods: {
    async fetchMainServices() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/booking");
        const data = await response.json();
        this.bookings = data;
      } catch (error) {
        this.errorMessage = "Failed to fetch services";
      }
    },async exportCSV() {
  try {
    this.$router.push('/admindashboard');
    const token = localStorage.getItem("token");
    const response = await fetch('http://127.0.0.1:5000/api/exportData', {
      method: 'GET',
      headers: {
       "Authorization": `Bearer ${token}`,
      },
    });

    if (response.ok) {
      const result= await response.json();
      alert(result.message);
    } else {
      alert("Error exporting data");
    }
  } catch (error) {
    alert("Error exporting data");
    console.error(error);
  }
},
    async logout() {
      localStorage.removeItem('Token');
      this.$router.push('/');
    }
  },
  mounted() {
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
  width: 80%;
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

.form-control {
  width: 50%;
  margin: 0 auto;
  font-size: 14px;
}
</style>
