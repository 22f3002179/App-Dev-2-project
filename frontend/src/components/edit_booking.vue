<template>
    <div class="container-fluid">
          <nav class="navbar">
            <div class="navbar-links" style="padding: 10px; background-color: #f8f9fa;">
              <a href="/MyBookings" class="btn" style="color: #007bff; text-decoration: none;">Back to My Bookings</a>
            </div>
          </nav>
        </div> 
        <div class="container">
        <h2>Edit Bookings </h2>
        <form @submit.prevent="updateService">
          <div class="mb-3">
            <label class="form-label">Booking_id</label>
            <input type="text" v-model="booking_id" class="form-control" disabled />
          </div>
    
          <div class="mb-3">
            <label class="form-label">Phone Number</label>
            <input type="tel" v-model="phone_number" class="form-control" />
          </div>

          <div class="mb-3">
            <label class="form-label">Location</label>
            <input type="text" v-model="location" class="form-control" />
          </div>

          <div class="mb-3">
            <label class="form-label">Pincode</label>
            <input type="text" v-model="pincode" class="form-control" />
          </div>
          
          <button type="submit" class="btn btn-primary">Update Bookings</button>
        </form>
    
        <p v-if="message" class="mt-3">{{ message }}</p>
      </div>
    </template>
    
    <script>
    export default {
      data() {
        return {
          booking_id: null,
          phone_number:"",
          location:"",
          pincode:"",
          message: "",
        };
      },
      mounted() {
        this.fetchService();
      },
      methods: {
        async fetchService() {
          this.booking_id = this.$route.params.booking_id;
          console.log("Booking ID set to:", this.booking_id);
          try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://127.0.0.1:5000/api/booking/${this.booking_id}`, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();
    
            if (response.ok) {
              this.phone_number = data.phone_number || "";
              this.location = data.location || "";
              this.pincode = data.pincode || "";
            } else {
              this.message = data.message || "Failed to fetch Bookings.";
            }
          } catch (error) {
            this.message = "";
          }
        },
        async updateService() {
          try {
            const token = localStorage.getItem("token");
            const payload = {};
        if (this.location.trim() !== "") {
          payload.location = this.location;
        }
        if (this.phone_number !== null && this.phone_number !== "") {
          payload.phone_number = this.phone_number;
        }
        if (this.pincode !== null && this.pincode !== "") {
          payload.pincode = this.pincode;
        }
    
        if (Object.keys(payload).length === 0) {
          this.message = "No changes were made.";
          return;
            };
    
            const response = await fetch(`http://127.0.0.1:5000/api/booking/${this.booking_id}`, {
              method: "PUT",
              headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify(payload),
            });
    
            const data = await response.json();
            this.message = data.message;
    
            if (response.ok) {
              this.$router.push("/MyBookings"); 
            }
          } catch (error) {
            this.message = "Error updating Bookings.";
          }
        },
      },
    };
    </script>
    
    