import axios from 'axios';
import {auth_server } from '@root/settings';
import {get_cookie,set_cookie} from '@utils/utils'



const auth_api = axios.create({
  baseURL: auth_server,
});

auth_api.interceptors.request.use(
  (config) => {
    const token = get_cookie('token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

auth_api.interceptors.response.use(
  async (response) => {
    return response;
  },
  async (error) => {

    if (error.response.status === 401 && error.response.data.error !== 'expired_token'){
        // parte il flusso oauth, non ci sono i token
    } 

    else if (error.response.status === 401 && error.response.data.error === 'expired_token') {
      const refreshToken = get_cookie('refresh_token');
      if (!refreshToken) {
        // parte il flusso oauth, il token di refresh non c'è
      }
      try {
        const response = await auth_api.post('/refresh_token', {}, {
          headers: {
            Authorization: `Bearer ${refreshToken}`,
          },
        });
        const newToken = response.data.message;
        set_cookie('token', newToken);
        return auth_api.request(error.config);
      } catch (err) {
        // il token di refresh è scaduto, parte il flusso oauth
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);
export { auth_api };