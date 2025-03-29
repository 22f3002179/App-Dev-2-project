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
    </nav>
  </div>
  
  <div class="container">
    <h2 class="text-center">Professionals</h2>
    <input type="text" v-model="searchProfessional" placeholder="Search by name " class="search-box" />
    <table class="styled-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Full Name</th>
          <th>Email</th>
          <th>Experience</th>
          <th>Address</th>
          <th>Pincode</th>
          <th>Supporting Documents</th>
          <th>MainServices ID</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="professional in filteredProfessionals" :key="professional.Professional_id">
          <td>{{ professional.Professional_id }}</td>
          <td>{{ professional.full_name }}</td>
          <td>{{ professional.email_id }}</td>
          <td>{{ professional.experience }}</td>
          <td>{{ professional.address }}</td>
          <td>{{ professional.pin_code }}</td>
          <td>{{ professional.supporting_documents }}</td>
          <td>{{ professional.MainServices_id }}</td>
          <td>{{ professional.status ? 'Active' : 'Inactive' }}</td>
          <td>
            <button class="btn btn-danger" @click="deleteProfessional(professional.Professional_id)">Delete</button>
            <button v-if="!professional.status" class="btn btn-success" @click="activateProfessional(professional.Professional_id)">Activate</button>
            <button v-if="professional.status" class="btn btn-danger" @click="blockProfessional(professional.Professional_id)">Block</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="container">
    <h2 class="text-center">Customers</h2>
    <input type="text" v-model="searchCustomer" placeholder="Search by name " class="search-box" />

    <table class="styled-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Full Name</th>
          <th>Email</th>
          <th>Address</th>
          <th>Pincode</th>
          <th>Role</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="customer in filteredCustomers" :key="customer.Customer_id">
          <td>{{ customer.Customer_id }}</td>
          <td>{{ customer.full_name }}</td>
          <td>{{ customer.email_id }}</td>
          <td>{{ customer.address }}</td>
          <td>{{ customer.pin_code }}</td>
          <td>{{ customer.role }}</td>
          <td>
            <button class="btn btn-danger" @click="deleteCustomer(customer.Customer_id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
      searchProfessional: "",
      searchCustomer: "",
      professionals: [],
      customers: []
    };
  },
  computed: {
  filteredProfessionals() {
    return this.professionals.filter(professional => 
      professional.full_name.toLowerCase().includes(this.searchProfessional.toLowerCase())
    );
  },
  filteredCustomers() {
    return this.customers.filter(customer => 
      customer.full_name.toLowerCase().includes(this.searchCustomer.toLowerCase())
    );
  }
},
  methods: {
    async fetchProfessionals() {
      const token = localStorage.getItem("token");
      try {
        const response = await fetch('http://127.0.0.1:5000/api/Professional', {
          method: 'GET',
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });
        const data = await response.json();
        this.professionals = data.professionals;
      } catch (error) {
        console.error('Error fetching professionals:', error);
      }
    },
    async fetchCustomers() {
      const token = localStorage.getItem("token");
      try {
        const response = await fetch('http://127.0.0.1:5000/api/Customer', {
          method: 'GET',
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });
        const data = await response.json();
        this.customers = data.customers;
      } catch (error) {
        console.error('Error fetching customers:', error);
      }
    },
    async deleteProfessional(professionalId) {
      const token = localStorage.getItem("token");
      try {
        await fetch(`http://127.0.0.1:5000/api/Professional/${professionalId}`, {
          method: 'DELETE',
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });
        this.fetchProfessionals();
      } catch (error) {
        console.error('Error deleting professional:', error);
      }
    },async activateProfessional(professionalId) {
    const token = localStorage.getItem("token");
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/Login/${professionalId}`, {
        method: 'PATCH',
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ status: 1})
      },);
      if (response.ok) {
        // After activation, refresh the professionals list
        this.fetchProfessionals();
        alert('Professional activated successfully!');
      } else {
        alert('Failed to activate professional.');
      }
    } catch (error) {
      console.error('Error activating professional:', error);
    }
  },
  async blockProfessional(professionalId) {
    const token = localStorage.getItem("token");
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/Login/${professionalId}`, {
        method: 'PATCH',
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ status: 0 })
      },);
      if (response.ok) {
        this.fetchProfessionals();
        alert('Professional Blocked successfully!');
      } else {
        alert('Failed to Block professional.');
      }
    } catch (error) {
      console.error('Error blocking professional:', error);
    }
  },

    async deleteCustomer(customerId) {
      const token = localStorage.getItem("token");
      try {
        await fetch(`http://127.0.0.1:5000/api/Customer/${customerId}`, {
          method: 'DELETE',
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });
        this.fetchCustomers();
      } catch (error) {
        console.error('Error deleting customer:', error);
      }
    }
  },
  mounted() {
    this.fetchProfessionals();
    this.fetchCustomers();
  }
};
</script>


<style scoped>
.container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin: 20px auto;
  max-width: 90%;
}

.navbar {
  display: flex;
  justify-content: space-between;
  background-color: #333;
  padding: 15px;
  color: white;
}

.navbar-links .btn {
  color: white;
  text-decoration: none;
  padding: 8px 15px;
}

.navbar-links .btn:hover {
  background-color: #555;
}

.search-box {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 5px;
  overflow: hidden;
}

.styled-table th, .styled-table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.styled-table th {
  background-color: #007bff;
  color: white;
}

.btn {
  padding: 8px 12px;
  margin: 5px;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

.btn-danger {
  background-color: red;
  color: white;
}

.btn-success {
  background-color: green;
  color: white;
}
</style>