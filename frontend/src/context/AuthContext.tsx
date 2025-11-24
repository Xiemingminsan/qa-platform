import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI } from '../api/auth';
import { LoginCredentials, RegisterData, User } from '../types';
import toast from 'react-hot-toast';

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Load user data from localStorage if token exists
    const savedUser = localStorage.getItem('user');
    if (savedUser && token) {
      setUser(JSON.parse(savedUser));
    }
  }, [token]);

  const login = async (credentials: LoginCredentials) => {
    try {
      const authResponse = await authAPI.login(credentials);
      setToken(authResponse.access_token);
      localStorage.setItem('token', authResponse.access_token);

      // Create user object with data from backend
      const userData: User = {
        id: 0, // Will be populated from JWT or API call
        username: authResponse.username,
        email: authResponse.email,
        created_at: new Date().toISOString(),
      };

      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      toast.success('Logged in successfully!');
    } catch (error: any) {
      console.error('Login error:', error);
      toast.error(error.response?.data?.detail || 'Login failed');
      throw error;
    }
  };

  const register = async (data: RegisterData) => {
    try {
      await authAPI.register(data);
      toast.success('Registration successful! Please login.');
    } catch (error: any) {
      console.error('Registration error:', error);
      toast.error(error.response?.data?.detail || 'Registration failed');
      throw error;
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    toast.success('Logged out successfully');
  };

  const value = {
    user,
    token,
    login,
    register,
    logout,
    isAuthenticated: !!token,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
