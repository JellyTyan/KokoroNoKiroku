import axios, { AxiosError } from 'axios';
import type { AnimeCreate, AnimeUpdate, AnimeResponse } from '@/types/anime';

interface ApiErrorResponse {
  detail: string;
  message?: string;
  errors?: any[];
}

const api = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public errors?: any[]
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export const handleApiError = (error: unknown): never => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiErrorResponse>;
    const response = axiosError.response;
    
    if (response?.status === 422) {
      const detail = response.data;
      throw new ApiError(
        detail.message || 'Validation error',
        response.status,
        detail.errors
      );
    }
    
    throw new ApiError(
      response?.data?.detail || axiosError.message,
      response?.status || 500
    );
  }
  
  throw new ApiError(
    error instanceof Error ? error.message : 'Unknown error',
    500
  );
};

export const animeApi = {
  addToList: async (data: AnimeCreate): Promise<AnimeResponse> => {
    try {
      const response = await api.post<AnimeResponse>('/anime-list/', data);
      return response.data;
    } catch (error) {
      return handleApiError(error);
    }
  },

  updateAnime: async (malId: number, data: AnimeUpdate): Promise<AnimeResponse> => {
    try {
      const response = await api.patch<AnimeResponse>(`/anime-list/${malId}`, data);
      return response.data;
    } catch (error) {
      return handleApiError(error);
    }
  },

  deleteAnime: async (malId: number): Promise<void> => {
    try {
      await api.delete(`/anime-list/${malId}`);
    } catch (error) {
      return handleApiError(error);
    }
  },

  getAnimeByStatus: async (status: string): Promise<AnimeResponse[]> => {
    try {
      const response = await api.get<AnimeResponse[]>(`/anime-list/${status}`);
      return response.data;
    } catch (error) {
      return handleApiError(error);
    }
  }
}; 