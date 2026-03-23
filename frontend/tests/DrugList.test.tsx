import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import DrugList from '../src/pages/DrugList';
import '../src/locales/i18n';
import * as api from '../src/services/api';

vi.mock('../src/services/api', () => ({
  getDrugs: vi.fn(() => Promise.resolve([
    { id: '1', name: '二甲双胍', specifications: '0.5g', indications: '糖尿病', storage_conditions: '常温' }
  ])),
  createDrug: vi.fn(() => Promise.resolve({})),
  updateDrug: vi.fn(() => Promise.resolve({})),
  deleteDrug: vi.fn(() => Promise.resolve({})),
}));

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

describe('DrugList Component', () => {
  it('renders drug list table and handles modal and interactions', async () => {
    render(<DrugList />);
    
    await waitFor(() => {
      expect(screen.getByText('二甲双胍')).toBeInTheDocument();
    });
    
    // Open modal
    fireEvent.click(screen.getByRole('button', { name: /新增药品/i }));
    
    // Check modal
    expect(await screen.findByRole('dialog')).toBeInTheDocument();
    expect(screen.getByLabelText('药品名称')).toBeInTheDocument();
    
    // Close modal
    fireEvent.click(screen.getByRole('button', { name: /Cancel|取消/i }));
    
    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });

    // Click edit
    const editBtns = screen.getAllByRole('button', { name: /编辑/i });
    if(editBtns.length > 0) {
      fireEvent.click(editBtns[0]);
    }

    // Click delete
    const deleteBtns = screen.getAllByRole('button', { name: /删除/i });
    if(deleteBtns.length > 0) {
      fireEvent.click(deleteBtns[0]);
      
      // confirm delete
      const confirmBtns = await screen.findAllByRole('button', { name: /确定|Yes|OK/i });
      if(confirmBtns.length > 0) {
        fireEvent.click(confirmBtns[confirmBtns.length - 1]);
        await waitFor(() => {
          expect(api.deleteDrug).toHaveBeenCalledWith('1');
        });
      }
    }
  });
});
