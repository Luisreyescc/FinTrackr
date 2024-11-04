<template>
  <div>
    <header>Crear Usuario</header>
    <hr />
    <form @submit.prevent="createUser">
      <div>
        <label for="username">Usuario:</label>
        <input type="text" v-model="user.user_name" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="user.email" required />
      </div>
      <div>
        <label for="password">Contraseña:</label>
        <input type="password" v-model="user.password_hash" required />
      </div>
      <button type="submit">Crear Usuario</button>
    </form>
    
    <hr />
    
    <header>Iniciar Sesión</header>
    <form @submit.prevent="loginUser">
      <div>
        <label for="login_username">Usuario:</label>
        <input type="text" v-model="login.user_name" required />
      </div>
      <div>
        <label for="login_password">Contraseña:</label>
        <input type="password" v-model="login.password_hash" required />
      </div>
      <button type="submit">Iniciar Sesión</button>
    </form>
    
    <hr />
    
    <header>Data Generada Desde Django</header>
    <div v-for="(output, id) in details" :key="id">
      <h2>{{ output.user_name }}</h2>
      <h3>{{ output.email }}</h3>
    </div>
    
    <div v-if="loginMessage">{{ loginMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: {
        user_name: '',
        email: '',
        password_hash: ''
      },
      login: {
        user_name: '',
        password_hash: ''
      },
      details: [],
      loginMessage: ''
    };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
      axios.get('http://localhost:8000/api/users')
        .then(res => {
          this.details = res.data;
        })
        .catch(err => {
          console.error(err);
        });
    },
    createUser() {
      axios.post('http://localhost:8000/api/users/', this.user, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(res => {
        this.details.push(res.data);
        this.user.user_name = '';
        this.user.email = '';
        this.user.password_hash = '';
      })
      .catch(err => {
        console.error(err);
      });
    },
    loginUser() {
      axios.get(`http://localhost:8000/api/users/?username=${this.login.user_name}`)
        .then(res => {
          // this.loginMessage = res.data;
          const user = res.data[0];
          if (user && user.password_hash === this.login.password_hash) {
            this.loginMessage = 'Inicio de sesión exitoso!';
          } else {
            this.loginMessage = 'Credenciales incorrectas.';
          }
        })
        .catch(err => {
          console.error(err);
          this.loginMessage = 'Error al verificar el usuario.';
        });
    }
  }
};
</script>

<style scoped>
form {
  margin-bottom: 20px;
}

div {
  margin-bottom: 10px;
}
</style>
