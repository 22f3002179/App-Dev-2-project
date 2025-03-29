<template>
    <div>
      <nav class="navbar">
        <a href="#" class="navbar-brand">Customer Dashboard</a>
        <div class="navbar-links">
          <router-link to="/customerdashboard" class="btn">Home</router-link>
        </div>
      </nav>
      
      <div class="container mt-4">
        <h2>Your Bookings</h2>
        <table class="table table-bordered">
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
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in bookings" :key="booking.booking_id">
              <td>{{ booking.booking_id }}</td>
              <td>{{ booking.date_of_request }}</td>
              <td>{{ booking.date_of_completion ? booking.date_of_completion : 'Pending' }}</td>
              <td>{{ booking.phone_number }}</td>
              <td>{{ booking.status }}</td>
              <td>{{ booking.location }}</td>
              <td>{{ booking.pincode }}</td>
              <td>{{ booking.rating ? booking.rating : 'Not Rated' }}</td>
              <td>
                <router-link v-if="booking.status === 'requested'" :to="`/edit_booking/${booking.booking_id}`" class="btn btn-warning">Edit</router-link>
                <button v-if="['requested', 'assigned'].includes(booking.status)" @click="deleteBooking(booking.booking_id)" class="btn btn-danger">Delete</button>
                <button v-if="booking.status === 'assigned'" @click="completeBooking(booking.booking_id)" class="btn btn-success">Complete</button>
                <router-link v-if="booking.status === 'completed'" :to="`/review/${booking.booking_id}`" class="btn btn-secondary">Review</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CustomerBookings',
    data() {
      return {
        bookings: []
      };
    },
    methods: {
      async fetchBookings() {
        try {
          const token = localStorage.getItem("token"); 
          const email = localStorage.getItem("email_id"); 
          if (!email) {
            console.error("User email not found.");
            return;
          }

          const customerResponse = await fetch(`http://127.0.0.1:5000/api/Customer?email_id=${email}`, {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          });

          if (!customerResponse.ok) {
            throw new Error(`Failed to fetch customer data. Status: ${customerResponse.status}`);
          }

          const customerData = await customerResponse.json();
          console.log("Customer Data:", customerData);

          // Access the customers array within the response object
          const customers = customerData.customers;

          // Check if the customers array is present
          if (Array.isArray(customers)) {
            const customer = customers.find(c => c.email_id === email);
            if (!customer) {
              console.error("Customer ID not found for this email.");
              return;
            }

            const customerId = customer.Customer_id;
            console.log("Customer ID:", customerId);

            // Fetch bookings
            const bookingsResponse = await fetch(`http://127.0.0.1:5000/api/booking?customer_id=${customerId}`, {
              method: "GET",
              headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
              },
            });

            if (!bookingsResponse.ok) {
              throw new Error(`Failed to fetch bookings. Status: ${bookingsResponse.status}`);
            }

            const bookingsData = await bookingsResponse.json();
            console.log("Bookings Data:", bookingsData);

            // Ensure bookingsData is an array
            this.bookings = Array.isArray(bookingsData) ? bookingsData : [];
          } else {
            console.error("Expected 'customers' to be an array, but received:", customerData);
          }

        } catch (error) {
          console.error("Error fetching bookings:", error);
        }
      },

      async deleteBooking(booking_id) {
        if (confirm('Are you sure you want to delete this booking?')) {
          try {
            const token = localStorage.getItem("token");
            const response = await fetch(`http://127.0.0.1:5000/api/booking/${booking_id}`, {
              method: 'DELETE',
              headers: { Authorization: `Bearer ${token}` },
            });

            const result = await response.json(); 
            console.log("API Response:", result); 

            if (response.ok) {
              console.log("Deleting from UI:", booking_id);
              this.bookings = this.bookings.filter(b => b.booking_id !== booking_id);
            } else {
              alert(`Failed to delete booking: ${result.message}`);
            }
          } catch (error) {
            console.error("Error deleting booking:", error);
            alert("Error deleting booking. Check console for details.");
          }
        }
      },

      async completeBooking(booking_id) {
        try {
          const token = localStorage.getItem("token");
          const response = await fetch(`http://127.0.0.1:5000/api/booking/${booking_id}`, {
            method: 'PUT', 
            headers: { 
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              status: "completed",
              date_of_completion: new Date().toISOString().split('T')[0]
            })
          });

          const result = await response.json();
          console.log("API Response:", result);

          if (response.ok) {
            alert("Booking marked as completed!");
            this.fetchBookings(); 
          } else {
            alert(`Failed to complete booking: ${result.message}`);
          }
        } catch (error) {
          console.error("Error completing booking:", error);
          alert("Error completing booking. Check console for details.");
        }
      }
    },
    mounted() {
      this.fetchBookings();
    }
  };
</script>


  