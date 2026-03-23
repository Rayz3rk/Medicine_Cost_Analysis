import { describe, it, expect, vi } from 'vitest';
import axios from 'axios';
import { getDrugs, createDrug, updateDrug, deleteDrug, startAnalysis, getAnalysisStatus, downloadPdf, downloadDocx } from '../src/services/api';

vi.mock('axios', () => {
  return {
    default: {
      create: vi.fn(() => ({
        get: vi.fn((url) => Promise.resolve({ data: `mock get ${url}` })),
        post: vi.fn((url, data) => Promise.resolve({ data: `mock post ${url}` })),
        put: vi.fn((url, data) => Promise.resolve({ data: `mock put ${url}` })),
        delete: vi.fn((url) => Promise.resolve({ data: `mock delete ${url}` })),
      }))
    }
  };
});

describe('API Services', () => {
  it('calls endpoints correctly', async () => {
    expect(await getDrugs()).toBe('mock get /drugs');
    expect(await createDrug({})).toBe('mock post /drugs');
    expect(await updateDrug('1', {})).toBe('mock put /drugs/1');
    expect(await deleteDrug('1')).toBe('mock delete /drugs/1');
    expect(await startAnalysis({})).toBe('mock post /analyze');
    expect(await getAnalysisStatus('1')).toBe('mock get /status/1');
    
    const pdfRes = await downloadPdf('1');
    expect(pdfRes.data).toBe('mock get /reports/1/pdf');
    
    const docxRes = await downloadDocx('1');
    expect(docxRes.data).toBe('mock get /reports/1/docx');
  });
});
