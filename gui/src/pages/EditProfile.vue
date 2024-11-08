<template>
<div class="edit-profile-page">
  <EditProfileForm :initialData="userData" @saveProfile="editProfile" @goToHome="goToHome" />
</div>
</template>

<script>
import EditProfileForm from '@/components/editprofile-form.vue';
import axios from 'axios';

export default {
  name: 'EditProfile',
  components: {
    EditProfileForm
  },
  data() {
    return {
       userData: {
        username: '',
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        curp: '',
        rfc: '',
        birthDate: '',
        password: ''
      }
    };
  },
  methods: {
    async editProfile(profileData) {
      try {
        const response = await axios.post(
          'http://localhost:8000/api/auth/register/',
          { user_name: profileData.username, name: profileData.name, last_name: profileData.lastName, email: profileData.email, user_curp: profileData.curp, user_rfc: profileData.rfc, phone_number: profileData.phone, birth_date: profileData.birthDate, password_hash: profileData.password },
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
	if (response.status === 200) {
          alert('User data updated successfully!');
        } else {
          alert('Failed to save data');
        }
      } catch (error) {
        console.error('Update failed:', error);
        alert('There was an issue with saving the user data. Please try again.');
      }
    },
    goToHome() {
      this.$router.push('/home');
    }
  }
};
</script>

<style scoped>
.edit-profile-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-family: "Wix Madefor Display", sans-serif;
}
</style>
