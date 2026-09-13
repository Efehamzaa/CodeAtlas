import { create } from 'zustand';
import axios from 'axios';


export interface RepositoryFile {
  path: string;
}

export interface Dependency {
  name: string;
  version: string | null;
}

export interface Framework {
  name: string;
  ecosystem: string | null;
}

export interface SecurityFinding {
  type: string;
  severity: string;
  description: string;
  file_path: string;
  line_number: number | null;
  recommendation: string | null;
}

export interface RepositoryResponse {
  repository_url: string;
  risk_score: number;
  repository_files: RepositoryFile[];
  dependencies: Dependency[];
  frameworks: Framework[];
  vulnerabilities: SecurityFinding[];
}


interface AnalysisState {
  repoUrl: string;
  isLoading: boolean;
  error: string | null;
  analysisData: RepositoryResponse | null; 
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

    set({ isLoading: true, error: null, analysisData: null });
    
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
      
      // Axios isteğine RepositoryResponse tipini zorluyoruz
      const response = await axios.post<RepositoryResponse>(`${apiUrl}/repositories/`, {
        url: repoUrl
      });
      
      set({ analysisData: response.data, isLoading: false });
    } catch (error: any) {
      let errorMessage = "Analiz sırasında sunucuya ulaşılamadı.";
      
      // Backend'in yapılandırılmış JSON hata formatını güvenli ayrıştırma
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        errorMessage = typeof detail === 'object' && detail.message ? detail.message : detail;
      } else if (error.message) {
        errorMessage = error.message;
      }

      set({ error: errorMessage, isLoading: false });
    }
  }
}));