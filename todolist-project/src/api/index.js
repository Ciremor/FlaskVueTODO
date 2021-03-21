import axios from 'axios';

export function authenticate(user) {
    return axios.post('http://127.0.0.1:5001/api/login', user)

}
