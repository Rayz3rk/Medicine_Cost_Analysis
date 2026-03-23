import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

export const getDrugs = () => api.get('/drugs').then(res => res.data);
export const createDrug = (data: any) => api.post('/drugs', data).then(res => res.data);
export const updateDrug = (id: string, data: any) => api.put(`/drugs/${id}`, data).then(res => res.data);
export const deleteDrug = (id: string) => api.delete(`/drugs/${id}`).then(res => res.data);

export const startAnalysis = (data: any) => api.post('/analyze', data).then(res => res.data);
export const getAnalysisStatus = (sessionId: string) => api.get(`/status/${sessionId}`).then(res => res.data);

export const downloadPdf = (sessionId: string) => 
  api.get(`/reports/${sessionId}/pdf`, { responseType: 'blob' });
export const downloadDocx = (sessionId: string) => 
  api.get(`/reports/${sessionId}/docx`, { responseType: 'blob' });

export default api;
