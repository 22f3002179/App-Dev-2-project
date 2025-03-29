<template>
  <div class="container d-flex justify-content-center align-items-start vh-100">
    <div class="card shadow-lg p-4 w-100" style="max-width: 600px; border-radius: 15px;">
      <div class="card-header text-center bg-primary text-white" style="border-radius: 10px 10px 0 0;">
        <h4>Customer Profile</h4>
      </div>
      <div class="card-body" style="max-height: 70vh; overflow-y: auto;">
        <div v-if="CustomerData" class="d-flex flex-column gap-4">

          <!-- Email ID (Non-editable) -->
          <div class="mb-3">
            <label for="email_id" class="form-label">Email ID</label>
            <input 
              type="email" 
              id="email_id" 
              v-model="CustomerData.email_id" 
              class="form-control" 
              readonly 
            />
          </div>

          <!-- Customer ID (Non-editable) -->
          <div class="mb-3">
            <label for="Customer_id" class="form-label">Customer ID</label>
            <input 
              type="number" 
              id="Customer_id" 
              v-model="CustomerData.Customer_id" 
              class="form-control" 
              readonly 
            />
          </div>

          <!-- Full Name -->
          <div class="mb-3">
            <label for="full_name" class="form-label">Full Name</label>
            <div v-if="isEditing">
              <input 
                type="text" 
                id="full_name" 
                v-model="CustomerData.full_name" 
                class="form-control"
                placeholder="Enter your full name"
              />
            </div>
            <div v-else>
              <p>{{ CustomerData.full_name || 'Not available' }}</p>
            </div>
          </div>

          <!-- Address -->
          <div class="mb-3">
            <label for="address" class="form-label">Address</label>
            <div v-if="isEditing">
              <input 
                type="text" 
                id="address" 
                v-model="CustomerData.address" 
                class="form-control"
                placeholder="Enter your address"
              />
            </div>
            <div v-else>
              <p>{{ CustomerData.address || 'Not available' }}</p>
            </div>
          </div>

          <!-- Pin Code -->
          <div class="mb-3">
            <label for="pin_code" class="form-label">Pin Code</label>
            <div v-if="isEditing">
              <input 
                type="text" 
                id="pin_code" 
                v-model="CustomerData.pin_code" 
                class="form-control"
                placeholder="Enter your pin code"
              />
            </div>
            <div v-else>
              <p>{{ CustomerData.pin_code || 'Not available' }}</p>
            </div>
          </div>

          <!-- Edit/Save Button -->
          <div class="mt-4 d-flex justify-content-between">
            <button @click="toggleEdit" class="btn btn-primary px-4 py-2">
              {{ isEditing ? 'Save Changes' : 'Edit Profile' }}
            </button>
            <button v-if="isEditing" @click="cancelEdit" class="btn btn-secondary px-4 py-2">Cancel Edit</button>
          </div>

        </div>

        <!-- Loading state -->
        <div v-else class="text-center">
          <p>Loading customer details...</p>
        </div>

        <!-- Back Button -->
        <div class="mt-4">
          <button @click="goBack" class="btn btn-outline-secondary w-100">
            <i class="bi bi-arrow-left-circle"></i> Back
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      CustomerData: null,
      token: localStorage.getItem('token'),
      email_id: localStorage.getItem('email_id'),
      isEditing: false, 
    };
  },
  async created() {
    await this.fetchCustomerDetails();
  },
  methods: {
    async fetchCustomerDetails() {
  console.log("Fetching customer details for email:", this.email_id);

  if (!this.email_id || !this.token) {
    console.error("Missing email or token, unable to fetch details.");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:5000/api/Customer`, {
      headers: { 'Authorization': `Bearer ${this.token}` },
    });

    if (!response.ok) throw new Error('Failed to fetch customer details');

    const data = await response.json();
    console.log('Raw API response:', data); // Debugging step

    // Access the correct array inside the object
    if (data.customers && Array.isArray(data.customers)) {
      const customer = data.customers.find(cust => cust.email_id === this.email_id);

      if (customer) {
        this.CustomerData = customer;
      } else {
        console.warn("No matching customer found for email:", this.email_id);
        this.CustomerData = null;
      }
    } else {
      console.error("Expected an array but received:", typeof data.customers, data);
      this.CustomerData = null;
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
},
    toggleEdit() {
      if (this.isEditing) {
        this.saveChanges();
      } else {
        this.isEditing = true;
      }
    },
    cancelEdit() {
      this.isEditing = false;
      this.fetchCustomerDetails();
    },
    async saveChanges() {
      if (!this.token || !this.CustomerData) {
        console.error("Missing token or customer data");
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/Customer/${this.CustomerData.Customer_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`,
          },
          body: JSON.stringify({
            full_name: this.CustomerData.full_name,
            pin_code: this.CustomerData.pin_code,
            address: this.CustomerData.address,
          }),
        });

        if (!response.ok) throw new Error('Failed to save customer details');

        alert('Profile updated successfully');
        this.isEditing = false;
        this.fetchCustomerDetails();
      } catch (error) {
        console.error('Error updating data:', error);
      }
    },
    goBack() {
      this.$router.go(-1);
    }
  },
};
</script>

  <style scoped>

  .card {
    background-color: #f8f9fa;
  }
  
  .card-header {
    background-color: #007bff;
    color: white;
  }
  
  .card-body {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
  }
  
  .form-control {
    border-radius: 5px;
    font-size: 14px;
  }
  
  button {
    font-size: 14px;
    border-radius: 5px;
    padding: 8px 16px;
  }
  
  button:hover {
    opacity: 0.9;
  }
  
  .mt-4 {
    margin-top: 20px;
  }
  
  .d-flex {
    display: flex;
  }
  
  .text-center {
    text-align: center;
  }
  
  .text-muted {
    color: #6c757d;
  }
  
  .w-100 {
    width: 100%;
  }
  
  .card-body {
    overflow-y: auto;
  }
  
  .card {
    max-height: 85vh;
    overflow-y: auto;
  }
  </style>