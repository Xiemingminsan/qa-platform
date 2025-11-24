import api from './axios';
import { Question } from '../types';

export const questionsAPI = {
  getAll: async (search?: string): Promise<Question[]> => {
    const params = search ? { search } : {};
    const response = await api.get<Question[]>('/questions/', { params });
    return response.data;
  },

  getById: async (id: number): Promise<Question> => {
    const response = await api.get<Question>(`/questions/${id}`);
    return response.data;
  },

  create: async (data: { title: string; body?: string }): Promise<Question> => {
    const response = await api.post<Question>('/questions/', data);
    return response.data;
  },

  update: async (id: number, data: { title?: string; body?: string }): Promise<Question> => {
    const response = await api.put<Question>(`/questions/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/questions/${id}`);
  },
};
