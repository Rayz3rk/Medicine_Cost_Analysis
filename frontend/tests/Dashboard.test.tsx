import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Dashboard from '../src/pages/Dashboard';

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

describe('Dashboard Component', () => {
  it('renders stats correctly', () => {
    render(<Dashboard />);
    expect(screen.getByText('总分析药品数')).toBeInTheDocument();
    expect(screen.getByText('本月新增')).toBeInTheDocument();
    expect(screen.getByText('112')).toBeInTheDocument();
    expect(screen.getByTestId('mock-column-chart')).toBeInTheDocument();
  });
});
