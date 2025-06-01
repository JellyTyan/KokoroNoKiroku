import { defineStore } from 'pinia';
import axios, { AxiosError } from 'axios';
import type { UserCredentials, AuthResponse, ApiError, User } from '../types/auth'; // Импортируем типы

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
  error: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
    user: null,
    loading: false,
    error: null,
  }),
  actions: {
    async login(credentials: UserCredentials): Promise<boolean> {
      this.loading = true;
      this.error = null;
      try {
        const params = new URLSearchParams();
        params.append('username', credentials.email);
        params.append('password', credentials.password);

        await axios.post('/api/auth/jwt/login', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });

        this.token = response.data.access_token;
        localStorage.setItem('token', this.token);
        this.isAuthenticated = true;
        return true;
      } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
          const axiosError = err as AxiosError<ApiError>;
          if (axiosError.response?.data?.detail) {
            if (typeof axiosError.response.data.detail === 'string') {
              this.error = axiosError.response.data.detail;
            } else if (Array.isArray(axiosError.response.data.detail)) {
              this.error = axiosError.response.data.detail.map((e) => e.msg).join(', ');
            }
          } else {
            this.error = 'Неизвестная ошибка при входе.';
          }
        } else {
          this.error = 'Ошибка подключения к серверу.';
          console.error(err);
        }
        this.token = null;
        localStorage.removeItem('token');
        this.isAuthenticated = false;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async register(credentials: UserCredentials): Promise<boolean> {
      this.loading = true;
      this.error = null;
      try {
        console.error(credentials.email)
        console.error(credentials.password)
        await axios.post(`/api/auth/register`, credentials);
        return true;
      } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
          const axiosError = err as AxiosError<ApiError>;
          if (axiosError.response?.data?.detail) {
            if (typeof axiosError.response.data.detail === 'string') {
              this.error = axiosError.response.data.detail;
            } else if (Array.isArray(axiosError.response.data.detail)) {
              this.error = axiosError.response.data.detail.map((e) => e.msg).join(', ');
            }
          } else {
            this.error = 'Неизвестная ошибка при регистрации.';
          }
        } else {
          this.error = 'Ошибка подключения к серверу.';
          console.error(err);
        }
        throw err;
      } finally {
        this.loading = false;
      }
    },

    logout(): void {
      this.token = null;
      localStorage.removeItem('token');
      this.isAuthenticated = false;
      this.user = null;
    },
  },
});
