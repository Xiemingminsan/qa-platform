import api from './axios';
import { VoteResponse } from '../types';

export const votesAPI = {
  voteQuestion: async (questionId: number, voteType: 'upvote' | 'downvote'): Promise<VoteResponse> => {
    const response = await api.post<VoteResponse>(`/questions/${questionId}/vote`, { vote_type: voteType });
    return response.data;
  },

  voteAnswer: async (answerId: number, voteType: 'upvote' | 'downvote'): Promise<VoteResponse> => {
    const response = await api.post<VoteResponse>(`/answers/${answerId}/vote`, { vote_type: voteType });
    return response.data;
  },
};
