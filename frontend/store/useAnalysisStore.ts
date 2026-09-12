import { create } from 'zustand';
import axios from 'axios';

interface AnalysisState {
  repoUrl: string;
  isLoading: boolean;
  error: string | null;
  analysisData: any | null; // İleride buraya AST ve Zafiyet tiplerini gireceğiz
  setRepoUrl: (url: string) => void;
  analyzeRepository: () => Promise<void>;
}

export const useAnalysisStore = create<AnalysisState>((set, get) => ({
  repoUrl: '',
  isLoading: false,
  error: null,
  analysisData: null,
  
  setRepoUrl: (url) => set({ repoUrl: url }),
  
  analyzeRepository: async () => {
    const { repoUrl } = get();
    if (!repoUrl) return;

    // İstek başlamadan önce loading'i aktif et, hataları temizle
    set({ isLoading: true, error: null, analysisData: null });
    
    try {
      // FastAPI backendimize POST isteği atıyoruz
      const response = await axios.post('http://127.0.0.1:8000/repositories/', {
        url: repoUrl
      });
      
      // Başarılı olursa veriyi kaydet ve loading'i kapat
      set({ analysisData: response.data, isLoading: false });
    } catch (error: any) {
      // Hata olursa yakala ve ekrana yansıt
      set({ 
        error: error.response?.data?.detail || "Analiz sırasında sunucuya ulaşılamadı.", 
        isLoading: false 
      });
    }
  }
}));