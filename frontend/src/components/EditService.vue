<template>
<div class="container-fluid">
      <nav class="navbar">
        <div class="navbar-links" style="padding: 10px; background-color: #f8f9fa;">
          <a href="/services" class="btn" style="color: #007bff; text-decoration: none;">Back to Services</a>
        </div>
      </nav>
    </div> 
    <div class="container">
    <h2>Edit Service</h2>
    <form @submit.prevent="updateService">
      <div class="mb-3">
        <label class="form-label">Service ID</label>
        <input type="text" v-model="serviceId" class="form-control" disabled />
      </div>

      <div class="mb-3">
        <label class="form-label">Description</label>
        <textarea v-model="description" class="form-control"></textarea>
      </div>

      <div class="mb-3">
        <label class="form-label">Price</label>
        <input type="number" v-model="price" class="form-control" />
      </div>

      <button type="submit" class="btn btn-primary">Update Service</button>
    </form>

    <p v-if="message" class="mt-3">{{ message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      serviceId: null,
      description: "",
      price: "",
      message: "",
    };
  },
  mounted() {
    this.fetchService();
  },
  methods: {
    async fetchService() {
      this.serviceId = this.$route.params.id;
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/adminservice/${this.serviceId}`);
        const data = await response.json();

        if (response.ok) {
          this.description = data.description || "";
          this.price = data.price || "";
        } else {
          this.message = data.message || "Failed to fetch service.";
        }
      } catch (error) {
        this.message = "";
      }
    },
    async updateService() {
      try {
        const token = localStorage.getItem("token");
        const payload = {};
    if (this.description.trim() !== "") {
      payload.description = this.description;
    }
    if (this.price !== null && this.price !== "") {
      payload.price = this.price;
    }

    if (Object.keys(payload).length === 0) {
      this.message = "No changes were made.";
      return;
        };

        const response = await fetch(`http://127.0.0.1:5000/api/adminservice/${this.serviceId}`, {
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
          this.$router.push("/services"); 
        }
      } catch (error) {
        this.message = "Error updating service.";
      }
    },
  },
};
</script>

