export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
}

export interface Question {
  id: number;
  title: string;
  body?: string;
  user_id: number;
  view_count: number;
  created_at: string;
  updated_at?: string;
  vote_score: number;
  answer_count: number;
  author_username: string;
}

export interface Answer {
  id: number;
  body: string;
  question_id: number;
  user_id: number;
  created_at: string;
  updated_at?: string;
  vote_score: number;
  author_username: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  username: string;
  email: string;
}

export interface VoteData {
  vote_type: 'upvote' | 'downvote';
}

export interface VoteResponse {
  message: string;
  new_score: number;
}
