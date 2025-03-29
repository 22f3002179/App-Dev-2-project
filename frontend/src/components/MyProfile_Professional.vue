<template>
  <div class="container d-flex justify-content-center align-items-start vh-100">
    <div class="card shadow-lg p-4 w-100" style="max-width: 600px; border-radius: 15px;">
      <div class="card-header text-center bg-primary text-white" style="border-radius: 10px 10px 0 0;">
        <h4>Professional Profile</h4>
      </div>
      <div class="card-body" style="max-height: 70vh; overflow-y: auto;">
        <div v-if="professionalData" class="d-flex flex-column gap-4">

          <!-- Email ID (Non-editable) -->
          <div class="mb-3">
            <label for="email_id" class="form-label">Email ID</label>
            <input 
              type="email" 
              id="email_id" 
              v-model="professionalData.professional.email_id" 
              class="form-control" 
              readonly 
            />
          </div>

          <!-- MainServices ID (Non-editable) -->
          <div class="mb-3">
            <label for="MainServices_id" class="form-label">Main Services ID</label>
            <input 
              type="number" 
              id="MainServices_id" 
              v-model="professionalData.professional.MainServices_id" 
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
                v-model="professionalData.professional.full_name" 
                class="form-control"
                placeholder="Enter your full name"
              />
            </div>
            <div v-else>
              <p>{{ professionalData.professional.full_name || 'Not available' }}</p>
            </div>
          </div>

          <!-- Experience -->
          <div class="mb-3">
            <label for="experience" class="form-label">Experience</label>
            <div v-if="isEditing">
              <input 
                type="number" 
                id="experience" 
                v-model="professionalData.professional.experience" 
                class="form-control"
                placeholder="Enter your years of experience"
              />
            </div>
            <div v-else>
              <p>{{ professionalData.professional.experience || 'Not available' }}</p>
            </div>
          </div>

          <!-- Address -->
          <div class="mb-3">
            <label for="address" class="form-label">Address</label>
            <div v-if="isEditing">
              <input 
                type="text" 
                id="address" 
                v-model="professionalData.professional.address" 
                class="form-control"
                placeholder="Enter your address"
              />
            </div>
            <div v-else>
              <p>{{ professionalData.professional.address || 'Not available' }}</p>
            </div>
          </div>

          <!-- Pin Code -->
          <div class="mb-3">
            <label for="pin_code" class="form-label">Pin Code</label>
            <div v-if="isEditing">
              <input 
                type="text" 
                id="pin_code" 
                v-model="professionalData.professional.pin_code" 
                class="form-control"
                placeholder="Enter your pin code"
              />
            </div>
            <div v-else>
              <p>{{ professionalData.professional.pin_code || 'Not available' }}</p>
            </div>
          </div>

          <!-- Supporting Documents -->
          <div class="mb-3">
            <label for="supporting_documents" class="form-label">Supporting Documents</label>
            <div v-if="isEditing">
              <input 
                type="text" 
                id="supporting_documents" 
                v-model="professionalData.professional.supporting_documents" 
                class="form-control"
                placeholder="Enter supporting documents"
              />
            </div>
            <div v-else>
              <p>{{ professionalData.professional.supporting_documents || 'Not available' }}</p>
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
          <p>Loading professional details...</p>
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
      professionalData: null,
      token: localStorage.getItem('token'),
      isEditing: false, // To toggle between edit and view mode
    };
  },
  async created() {
    await this.fetchProfessionalDetails();
  },
  methods: {
    async fetchProfessionalDetails() {
      const email_id = localStorage.getItem('email_id');
      console.log("Fetching professional details for email:", email_id);

      if (!email_id || !this.token) {
        console.error("Missing email or token, unable to fetch details.");
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/Professional?email_id=${email_id}`, {
          headers: { 'Authorization': `Bearer ${this.token}` },
        });

        if (!response.ok) throw new Error('Failed to fetch professional details');

        const data = await response.json();
        console.log('Professional data fetched:', data);

        this.professionalData = data;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    toggleEdit() {
      if (this.isEditing) {
        this.saveChanges(); // Save the changes if currently editing
      } else {
        this.isEditing = true; // Switch to edit mode
      }
    },
    cancelEdit() {
      this.isEditing = false;
      this.fetchProfessionalDetails(); // Reset the data to the original state
    },
    async saveChanges() {
      const email_id = localStorage.getItem('email_id');
      const professionalId = this.professionalData.professional.Professional_id;
      if (!this.token) {
        console.error("Missing token");
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/Professional/${professionalId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`,
          },
          body: JSON.stringify({
            full_name: this.professionalData.professional.full_name,
            experience: this.professionalData.professional.experience,
            address: this.professionalData.professional.address,
            pin_code: this.professionalData.professional.pin_code,
            supporting_documents: this.professionalData.professional.supporting_documents,
          }),
        });

        if (!response.ok) throw new Error('Failed to save professional details');

        const updatedData = await response.json();
        console.log('Updated data:', updatedData);

        alert('Profile updated successfully');
        this.isEditing = false; // Turn off editing after successful update
        this.professionalData = updatedData; // Update the local data with the updated info
      } catch (error) {
        console.error('Error updating data:', error);
      }
    },
    goBack() {
      // Navigate back to the previous page
      this.$router.go(-1);
    }
  },
};
</script>

<style scoped>
/* Custom styling */
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
