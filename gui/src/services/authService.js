import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000/api/auth/',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const login = (username, password) => {
    return axiosInstance.post('login/', { username, password });
};

export const register = (email, username, password) => {
    return axiosInstance.post('register/', { email, username, password });
};