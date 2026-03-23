import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AppState {
  user: any | null;
  theme: 'light' | 'dark';
  locale: 'zh' | 'en';
  setUser: (user: any | null) => void;
  setTheme: (theme: 'light' | 'dark') => void;
  setLocale: (locale: 'zh' | 'en') => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      user: null,
      theme: 'light',
      locale: 'zh',
      setUser: (user) => set({ user }),
      setTheme: (theme) => set({ theme }),
      setLocale: (locale) => set({ locale }),
    }),
    {
      name: 'app-storage',
    }
  )
);
