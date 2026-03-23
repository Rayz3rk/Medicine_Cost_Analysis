import { describe, it, expect, beforeEach } from 'vitest';
import { useAppStore } from '../src/store';

describe('useAppStore', () => {
  beforeEach(() => {
    // Reset store before each test
    useAppStore.setState({ user: null, theme: 'light', locale: 'zh' });
  });

  it('should have initial state', () => {
    const state = useAppStore.getState();
    expect(state.user).toBeNull();
    expect(state.theme).toBe('light');
    expect(state.locale).toBe('zh');
  });

  it('should update theme', () => {
    useAppStore.getState().setTheme('dark');
    expect(useAppStore.getState().theme).toBe('dark');
  });

  it('should update locale', () => {
    useAppStore.getState().setLocale('en');
    expect(useAppStore.getState().locale).toBe('en');
  });

  it('should update user', () => {
    const user = { name: 'Admin', role: 'admin' };
    useAppStore.getState().setUser(user);
    expect(useAppStore.getState().user).toEqual(user);
  });
});
