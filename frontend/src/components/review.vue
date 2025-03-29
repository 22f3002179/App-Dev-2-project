<template>
  <div class="container">
    <h2>Rate the Service</h2>
    <form @submit.prevent="updateService">
      <div class="mb-3">
        <label class="form-label">Booking ID</label>
        <input type="text" v-model="booking_id" class="form-control" disabled />
      </div>

      <div class="mb-3">
        <label class="form-label">Rating</label>
        <div class="rating-buttons">
          <button v-for="n in 5" :key="n"
                  :class="{'btn': true, 'btn-outline-primary': rating !== n, 'btn-primary': rating === n}"
                  @click="setRating(n)">
            {{ n }}
          </button>
        </div>
        <p>Selected Rating: {{ rating }}</p>
      </div>
    </form>

    <p v-if="message" class="mt-3">{{ message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      booking_id: null,
      rating: 0, // Default rating
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
          this.rating = data.rating || 0; 
        } else {
          this.message = data.message || "Failed to fetch rating.";
        }
      } catch (error) {
        this.message = "Error fetching booking details.";
      }
    },
    setRating(n) {
      this.rating = n; 
    },
    async updateService() {
      try {
        const token = localStorage.getItem("token");
        const payload = { rating: this.rating };

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
        this.message = "Error updating rating.";
      }
    },
  },
};
</script>

<style scoped>
.rating-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.rating-buttons button {
  padding: 10px 20px;
  font-size: 18px;
  border: 1px solid #ccc;
  background-color: white;
  cursor: pointer;
}

.rating-buttons button:hover {
  background-color: #f0f0f0;
}

.rating-buttons button.btn-primary {
  background-color: #007bff;
  color: white;
}

.rating-buttons button.btn-outline-primary {
  background-color: white;
  color: #007bff;
}
</style>
