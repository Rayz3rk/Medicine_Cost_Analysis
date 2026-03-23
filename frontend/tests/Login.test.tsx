import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect, vi } from 'vitest';
import Login from '../src/pages/Login';

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

describe('Login Component', () => {
  it('renders login form correctly', () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    expect(screen.getByText('系统登录')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Username')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /登 录/i })).toBeInTheDocument();
  });

  it('shows validation errors when submitting empty form', async () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    fireEvent.click(screen.getByRole('button', { name: /登 录/i }));
    
    // antd validation takes a moment
    expect(await screen.findByText('请输入用户名!')).toBeInTheDocument();
    expect(await screen.findByText('请输入密码!')).toBeInTheDocument();
  });
});
