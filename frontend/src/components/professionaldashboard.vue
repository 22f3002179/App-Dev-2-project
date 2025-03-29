<template>
  <nav class="navbar">
    <a href="#" class="navbar-brand">Professional Dashboard</a>
    <div class="navbar-links">
      <a href="/professionaldashboard" class="btn">Home</a>
      <a href="/MyProfile_Professional" class="btn">My Profile</a>
    </div>
    <div class="navbar-actions">
      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>
  </nav>

  <div class="container mt-4">
    <div v-if="filteredBookings.length">
      <h4 class="text-center">All Service Booking Requests:</h4>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Booking ID</th>
            <th>Date of Request</th>
            <th>Date of Completion</th>
            <th>Phone Number</th>
            <th>Status</th>
            <th>Location</th>
            <th>Pincode</th>
            <th>Rating</th>
            <th>Customer ID</th>
            <th>Service ID</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in filteredBookings" :key="booking.booking_id">
            <td>{{ booking.booking_id }}</td>
            <td>{{ booking.date_of_request }}</td>
            <td>{{ booking.date_of_completion || 'N/A' }}</td>
            <td>{{ booking.phone_number }}</td>
            <td>{{ booking.status }}</td>
            <td>{{ booking.location }}</td>
            <td>{{ booking.pincode }}</td>
            <td>{{ booking.rating || 'No rating' }}</td>
            <td>{{ booking.customer_id }}</td>
            <td>{{ booking.service_id }}</td>
            <td v-if="booking.status === 'requested'">
              <button class="btn btn-success" @click="acceptBooking(booking.booking_id)">Accept</button>
            </td>
            <td v-else>-</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else>
      <p class="text-center">No booking requests available.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfessionalDashboard',
  data() {
    return {
      allBookings: [],
      filteredBookings: [],
      professionalDetails: {},
      serviceIds: []
    };
  },
  created() {
    this.fetchProfessionalDetails();
  },
  methods: {
    async fetchProfessionalDetails() {
      const email_id = localStorage.getItem('email_id');
      const token = localStorage.getItem('token');

      if (!email_id || !token) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/Professional?email_id=${email_id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch professional details');
        const data = await response.json();
        if (data.professional) {
          this.professionalDetails = {
            Professional_id: data.professional.Professional_id,
            MainServices_id: data.professional.MainServices_id
          };
          this.fetchServicesByMainServiceId();
        }
      } catch (error) {
        console.error(error);
      }
    },
    async fetchServicesByMainServiceId() {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch('http://127.0.0.1:5000/api/adminservice', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch services');
        const data = await response.json();
        this.serviceIds = data.services.filter(service => 
          service.MainServices_id == this.professionalDetails.MainServices_id
        ).map(service => service.service_id);
        this.fetchAllBookings();
      } catch (error) {
        console.error(error);
      }
    },
    async fetchAllBookings() {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/booking');
    const data = await response.json();
    this.allBookings = data;

    this.filteredBookings = data.filter(booking => 
      this.serviceIds.includes(booking.service_id) &&
      (booking.status === 'requested' || 
        booking.professional_id === this.professionalDetails.Professional_id)
    );
  } catch (error) {
    console.error(error);
  }
}
,
    async acceptBooking(bookingId) {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/booking/${bookingId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            status: 'assigned',
            professional_id: this.professionalDetails.Professional_id
          })
        });
        if (!response.ok) throw new Error('Failed to accept booking');
        this.fetchAllBookings();
      } catch (error) {
        console.error(error);
      }
    },
    logout() {
      localStorage.clear();
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.navbar {
  background-color: #343a40;
  padding: 10px;
}

.navbar-brand {
  color: #fff;
  font-size: 1.5em;
}

.navbar-links {
  float: right;
}

.navbar-actions {
  float: right;
  margin-left: 10px;
}

.navbar-links a,
.navbar-actions button {
  margin-left: 10px;
}

.btn {
  background-color: #007bff;
  color: #fff;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  margin-bottom: 5px;
}

.btn-danger {
  background-color: #dc3545;
}

.table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 12px;
  text-align: center;
  border: 1px solid #ddd;
}

.table-striped tr:nth-child(even) {
  background-color: #f9f9f9;
}

.text-center {
  text-align: center;
}

.mt-3 {
  margin-top: 20px;
}

.mt-4 {
  margin-top: 30px;
}
</style>

