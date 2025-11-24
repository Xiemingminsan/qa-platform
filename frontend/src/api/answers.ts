import api from './axios';
import { Answer } from '../types';

export const answersAPI = {
  getByQuestionId: async (questionId: number): Promise<Answer[]> => {
    const response = await api.get<Answer[]>(`/questions/${questionId}/answers`);
    return response.data;
  },

  create: async (questionId: number, body: string): Promise<Answer> => {
    const response = await api.post<Answer>(`/questions/${questionId}/answers`, { body });
    return response.data;
  },

  update: async (id: number, body: string): Promise<Answer> => {
    const response = await api.put<Answer>(`/answers/${id}`, { body });
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/answers/${id}`);
  },
};
