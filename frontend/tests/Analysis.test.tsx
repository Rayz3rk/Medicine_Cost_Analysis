import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import Analysis from '../src/pages/Analysis';
import '../src/locales/i18n';
import * as api from '../src/services/api';

vi.mock('../src/services/api', () => ({
  getDrugs: vi.fn(() => Promise.resolve([{ id: '1', name: '二甲双胍' }])),
  startAnalysis: vi.fn(() => Promise.resolve({ session_id: '123', status: 'started' })),
  getAnalysisStatus: vi.fn(() => Promise.resolve({
    status: 'completed',
    session_id: '123',
    report: {
      cost_summary: 'cost sum',
      pricing_strategy: 'pricing',
      supply_chain_advice: 'supply'
    }
  })),
  downloadPdf: vi.fn(() => Promise.resolve({ data: new Blob() })),
  downloadDocx: vi.fn(() => Promise.resolve({ data: new Blob() })),
}));

Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

global.ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
};

global.URL.createObjectURL = vi.fn(() => 'mock-url');

describe('Analysis Component', () => {
  it('renders analysis form', async () => {
    render(<Analysis />);
    expect(screen.getByText('参数配置')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(api.getDrugs).toHaveBeenCalled();
    });
  });
});
