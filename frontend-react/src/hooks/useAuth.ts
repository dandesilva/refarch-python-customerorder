import { create } from 'zustand';
import { authApi } from '../services/api';

interface AuthState {
  token: string | null;
  username: string | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuth = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  username: localStorage.getItem('username'),
  isAuthenticated: !!localStorage.getItem('token'),
  login: async (username: string, password: string) => {
    const data = await authApi.login(username, password);
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('username', data.username);
    set({ token: data.access_token, username: data.username, isAuthenticated: true });
  },
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    set({ token: null, username: null, isAuthenticated: false });
  },
}));
