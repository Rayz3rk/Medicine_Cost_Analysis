import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect, vi } from 'vitest';
import MainLayout from '../src/layouts/MainLayout';
import '../src/locales/i18n';

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

describe('MainLayout Component', () => {
  it('renders layout and handles toggles', () => {
    render(
      <BrowserRouter>
        <MainLayout />
      </BrowserRouter>
    );
    
    // Check initial render
    expect(screen.getByText('Drug Cost Analysis')).toBeInTheDocument();
    
    // Toggle theme
    const themeSwitch = screen.getByRole('switch');
    fireEvent.click(themeSwitch);
    
    // Toggle language
    const langButton = screen.getByText('EN');
    fireEvent.click(langButton);
  });
});
