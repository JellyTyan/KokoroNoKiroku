import { defineStore } from 'pinia';
import axios, { AxiosError } from 'axios';
import type { UserCredentials, ApiError, User } from '../types/auth';

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
  error: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    isAuthenticated: false,
    user: null,
    loading: false,
    error: null,
  }),

  actions: {
    async login(credentials: UserCredentials): Promise<boolean> {
      this.loading = true;
      this.error = null;
      try {
        await axios.post(
          'http://localhost:5003/api/auth/jwt/login',
          new URLSearchParams({
            username: credentials.email,
            password: credentials.password,
          }),
          {
            withCredentials: true,
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          }
        );

        await this.fetchUser();
        return true;
      } catch (err: unknown) {
        this.handleError(err, 'при входе');
        return false;
      } finally {
        this.loading = false;
      }
    },

    async register(credentials: UserCredentials): Promise<boolean> {
      this.loading = true;
      this.error = null;
      try {
        await axios.post('http://localhost:5003/api/auth/register', credentials, {
          withCredentials: true,
        });
        return true;
      } catch (err: unknown) {
        this.handleError(err, 'при регистрации');
        return false;
      } finally {
        this.loading = false;
      }
    },

    async fetchUser(): Promise<void> {
      try {
        const response = await axios.get<User>('http://localhost:5003/api/users/me', {
          withCredentials: true,
        });
        this.user = response.data;
        this.isAuthenticated = true;
      } catch (err) {
        this.user = null;
        this.isAuthenticated = false;
      }
    },

    async logout(): Promise<void> {
      await axios.post('http://localhost:5003/auth/jwt/logout', null, {
        withCredentials: true,
      });
      this.user = null;
      this.isAuthenticated = false;
    },

    handleError(err: unknown, context: string): void {
      if (axios.isAxiosError(err)) {
        const axiosError = err as AxiosError<ApiError>;
        if (axiosError.response?.data?.detail) {
          const detail = axiosError.response.data.detail;
          if (typeof detail === 'string') {
            this.error = detail;
          } else if (Array.isArray(detail)) {
            this.error = detail.map((e) => e.msg).join(', ');
          }
        } else {
          this.error = `Неизвестная ошибка ${context}.`;
        }
      } else {
        this.error = `Ошибка подключения ${context}.`;
        console.error(err);
      }
    },
  },
});
