import axios from 'axios'

import { API_DOMAIN } from './constants/api'


const api = axios.create({
	baseURL: `http://${API_DOMAIN}`,
})


export default api
