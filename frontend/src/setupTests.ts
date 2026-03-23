import '@testing-library/jest-dom';
import { vi } from 'vitest';
import React from 'react';

if (typeof window.URL.createObjectURL === 'undefined') {
  window.URL.createObjectURL = () => '';
}
if (typeof window.URL.revokeObjectURL === 'undefined') {
  window.URL.revokeObjectURL = () => {};
}

if (typeof window.Worker === 'undefined') {
  class Worker {
    url: string | URL;
    onmessage: ((this: Worker, ev: MessageEvent) => any) | null = null;
    constructor(stringUrl: string | URL) {
      this.url = stringUrl;
    }
    postMessage() {}
    terminate() {}
    addEventListener() {}
    removeEventListener() {}
    dispatchEvent() { return false; }
  }
  window.Worker = Worker as any;
}

// Mock Ant Design Charts to avoid canvas issues in jsdom
vi.mock('@ant-design/charts', () => ({
  Column: () => React.createElement('div', { 'data-testid': 'mock-column-chart' }),
  Pie: () => React.createElement('div', { 'data-testid': 'mock-pie-chart' })
}));
