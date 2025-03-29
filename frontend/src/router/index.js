import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/components/HomePage.vue'
import LoginPage from '@/components/LoginPage.vue'
import CustomerSignup from '@/components/CustomerSignup.vue'
import ProfessionalSignup from '@/components/ProfessionalSignup.vue'
import AdminDashboard from '@/components/AdminDashboard.vue'
import MainServices from '@/components/MainServices.vue'
import services from '@/components/services.vue'
import Professionals_Customers from '@/components/Professionals_Customers.vue'
import EditService from '@/components/EditService.vue'
import customerdashboard from '@/components/customerdashboard.vue'
import MyBookings from '@/components/MyBookings.vue'
import edit_booking from '@/components/edit_booking.vue'
import review from '@/components/review.vue'
import professionaldashboard from '@/components/professionaldashboard.vue'
import MyProfile_Professional from '@/components/MyProfile_Professional.vue'
import MyProfile_Customer from '@/components/MyProfile_Customer.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    {
      path: '/LoginPage',
      name: 'LoginPage',
      component: LoginPage,
    },
    {
      path: '/CustomerSignup',
      name: 'CustomerSignup',
      component: CustomerSignup,
    },
    {
      path: '/ProfessionalSignup',
      name: 'ProfessionalSignup',
      component: ProfessionalSignup,
    },
    {
      path: '/admindashboard', 
      name: 'AdminDashboard',
      component: AdminDashboard,
    },
    {
      path: '/mainservices', 
      name: 'MainServices',
      component: MainServices,
    },
    {
      path:'/services',
      name:'services',
      component: services,
    },
    {
      path:'/Professionals_Customers',
      name:'Professionals_Customers',
      component: Professionals_Customers,
    },
    {
      path: "/editservice/:id",
      name: "EditService",
      component: EditService, 
    },
    {
      path: '/customerdashboard',
      name: 'customerdashboard',
      component: customerdashboard,
    },
    {
      path: '/MyBookings',
      name: 'MyBookings',
      component: MyBookings,
    },
    {
      path: '/edit_booking/:booking_id',
      name: 'edit_booking',
      component: edit_booking,
    },
    {
      path: '/review/:booking_id',
      name: 'review',
      component: review,
    },
    {
      path: '/professionaldashboard',
      name: 'professionaldashboard',
      component: professionaldashboard,
    },
    {
      path: '/MyProfile_Professional',
      name: 'MyProfile_Professional',
      component: MyProfile_Professional,
    },
    {
      path: '/MyProfile_Customer',
      name: 'MyProfile_Customer',
      component: MyProfile_Customer,
    },
    
  ],
})

export default router
