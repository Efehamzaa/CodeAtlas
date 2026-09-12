"use client";

import { Terminal, ShieldCheck, Loader2, FileCode2, AlertOctagon, Activity, Folder, FileText } from "lucide-react";
import { useAnalysisStore } from "../store/useAnalysisStore";

export default function Home() {
  const { repoUrl, isLoading, error, analysisData, setRepoUrl, analyzeRepository } = useAnalysisStore();

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-50 flex flex-col items-center p-6 selection:bg-cyan-900">
      {/* Neon Vurgulu Sabit Arkaplan */}
      <div className="fixed top-0 z-[-2] h-screen w-screen bg-zinc-950 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(6,182,212,0.15),rgba(255,255,255,0))]"></div>

      {/* DURUM 1: HENÜZ VERİ YOKSA (Arama Ekranı) */}
      {!analysisData ? (
        <div className="max-w-3xl w-full space-y-8 text-center mt-32 z-10">
          <div className="space-y-4">
            <div className="flex justify-center mb-4">
              <div className="p-3 bg-zinc-900 border border-zinc-800 rounded-2xl shadow-[0_0_30px_rgba(6,182,212,0.2)]">
                <ShieldCheck className="w-12 h-12 text-cyan-400" />
              </div>
            </div>
            <h1 className="text-5xl font-extrabold tracking-tight lg:text-7xl text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-600">
              CodeAtlas
            </h1>
            <p className="text-xl text-zinc-400 font-medium">Understand Any Repository.</p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 items-center bg-zinc-900/50 p-2 rounded-xl border border-zinc-800 backdrop-blur-sm shadow-2xl transition-all focus-within:border-cyan-500/50 focus-within:ring-4 focus-within:ring-cyan-500/10">
            <input 
              type="text" 
              placeholder="https://github.com/kullanici/repo" 
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && analyzeRepository()}
              disabled={isLoading}
              className="flex-1 w-full bg-transparent border-none outline-none px-4 py-3 text-lg text-zinc-200 placeholder:text-zinc-600 disabled:opacity-50"
            />
            <button 
              onClick={analyzeRepository}
              disabled={isLoading}
              className="w-full sm:w-auto bg-cyan-600 hover:bg-cyan-500 text-white px-8 py-3 rounded-lg font-semibold flex gap-2 items-center justify-center transition-colors shadow-[0_0_15px_rgba(6,182,212,0.4)] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <><Loader2 className="w-5 h-5 animate-spin" /> Analiz Ediliyor...</>
              ) : (
                <><Terminal size={20} /> Analizi Başlat</>
              )}
            </button>
          </div>
          
          {error && (
            <div className="text-red-400 bg-red-400/10 border border-red-400/20 p-4 rounded-lg mt-4">
              {error}
            </div>
          )}
        </div>
      ) : (
        /* DURUM 2: VERİ GELDİYSE (Dashboard Ekranı) */
        <div className="max-w-6xl w-full space-y-6 mt-10 mb-20 z-10 animate-in fade-in duration-700">
          
          {/* Üst Bilgi Barı */}
          <div className="flex items-center justify-between bg-zinc-900/50 p-6 rounded-2xl border border-zinc-800 backdrop-blur-sm shadow-lg">
            <div>
              <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-600">
                Analiz Raporu
              </h2>
              <p className="text-zinc-400 mt-1">{repoUrl}</p>
            </div>
            <button 
              onClick={() => window.location.reload()}
              className="bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors border border-zinc-700"
            >
              Yeni Analiz
            </button>
          </div>

          {/* Metrik Kartları */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-zinc-900/50 p-6 rounded-2xl border border-zinc-800 shadow-lg flex items-center gap-5">
              <div className="p-4 bg-blue-500/10 rounded-xl text-blue-400"><FileCode2 size={28} /></div>
              <div>
                <p className="text-sm font-medium text-zinc-400">Bulunan Bağımlılık</p>
                <p className="text-3xl font-bold text-zinc-100">
                  {analysisData.dependencies?.length || 0}
                </p>
              </div>
            </div>
            <div className="bg-zinc-900/50 p-6 rounded-2xl border border-zinc-800 shadow-lg flex items-center gap-5">
              <div className="p-4 bg-red-500/10 rounded-xl text-red-400"><AlertOctagon size={28} /></div>
              <div>
                <p className="text-sm font-medium text-zinc-400">Çatı (Framework)</p>
                <p className="text-3xl font-bold text-zinc-100">
                  {analysisData.frameworks?.length || 0}
                </p>
              </div>
            </div>
            
            {/* Dinamik Risk Skoru Kartı */}
            <div className="bg-zinc-900/50 p-6 rounded-2xl border border-zinc-800 shadow-lg flex items-center gap-5">
              <div className={`p-4 rounded-xl ${
                (analysisData.risk_score || 0) > 70 ? "bg-red-500/10 text-red-400 shadow-[0_0_15px_rgba(248,113,113,0.2)]" : 
                (analysisData.risk_score || 0) > 30 ? "bg-amber-500/10 text-amber-400" : 
                "bg-emerald-500/10 text-emerald-400 shadow-[0_0_15px_rgba(52,211,153,0.1)]"
              }`}>
                <Activity size={28} />
              </div>
              <div>
                <p className="text-sm font-medium text-zinc-400">Yapay Zeka Risk Skoru</p>
                <div className="flex items-baseline gap-2 mt-1">
                  <p className="text-3xl font-bold text-zinc-100">
                    {analysisData.risk_score || 0}
                  </p>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-sm uppercase tracking-wider border ${
                    (analysisData.risk_score || 0) > 70 ? "bg-red-950/50 text-red-400 border-red-900/50" : 
                    (analysisData.risk_score || 0) > 30 ? "bg-amber-950/50 text-amber-400 border-amber-900/50" : 
                    "bg-emerald-950/50 text-emerald-400 border-emerald-900/50"
                  }`}>
                    {(analysisData.risk_score || 0) > 70 ? "KRİTİK" : 
                     (analysisData.risk_score || 0) > 30 ? "UYARI" : "GÜVENLİ"}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Teknolojiler ve Bağımlılıklar Panelleri */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-in slide-in-from-bottom-4 duration-700">
            <div className="bg-zinc-900/50 p-6 rounded-2xl border border-zinc-800 shadow-lg h-[300px] flex flex-col">
              <h3 className="text-xl font-bold text-cyan-400 mb-4 flex items-center gap-2 shrink-0">
                <Terminal size={20} /> Tespit Edilen Bağımlılıklar
              </h3>
              <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-3">
                {analysisData.dependencies?.map((dep: any, index: number) => (
                  <div key={index} className="flex justify-between items-center p-3 bg-zinc-950 rounded-lg border border-zinc-800/50 hover:border-cyan-900/50 transition-colors">
                    <span className="font-medium text-zinc-300">{dep.name}</span>
                    <span className="text-xs px-2.5 py-1 bg-cyan-950/50 text-cyan-400 rounded-md border border-cyan-900/50 font-mono">
                      v{dep.version || "Bilinmiyor"}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-zinc-900/50 p-6 rounded-2xl border border-zinc-800 shadow-lg h-[300px] flex flex-col">
              <h3 className="text-xl font-bold text-blue-400 mb-4 flex items-center gap-2 shrink-0">
                <FileCode2 size={20} /> Çatı Mimarisi
              </h3>
              <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-3">
                {analysisData.frameworks?.map((fw: any, index: number) => (
                  <div key={index} className="flex justify-between items-center p-3 bg-zinc-950 rounded-lg border border-zinc-800/50 hover:border-blue-900/50 transition-colors">
                    <span className="font-medium text-zinc-300">{fw.name || fw}</span>
                    <span className="text-xs px-2.5 py-1 bg-blue-950/50 text-blue-400 rounded-md border border-blue-900/50 font-mono">
                      {fw.ecosystem || "Sistem"}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Zafiyetler ve Mimari (AST) Panelleri */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-in slide-in-from-bottom-5 duration-700 delay-150">
            
            {/* Özel Zafiyet (Vulnerability) Kartı */}
            <div className="bg-zinc-900/50 p-6 rounded-2xl border border-zinc-800 shadow-lg flex flex-col h-[450px]">
              <h3 className="text-xl font-bold text-red-400 mb-4 flex items-center gap-2 shrink-0">
                <AlertOctagon size={20} /> Güvenlik Zafiyetleri
              </h3>
              <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-3">
                {!analysisData.vulnerabilities || analysisData.vulnerabilities.length === 0 ? (
                  <div className="flex flex-col items-center justify-center h-full text-zinc-500 gap-2">
                    <ShieldCheck size={32} className="text-zinc-600" />
                    <p>Tespit edilen zafiyet bulunamadı.</p>
                  </div>
                ) : (
                  <div className="w-full space-y-2">
                    {analysisData.vulnerabilities.map((vuln: any, index: number) => (
                      <div key={index} className="border border-red-900/30 bg-zinc-950 rounded-lg overflow-hidden">
                        <div className="flex items-center justify-between w-full p-4 border-b border-red-900/20">
                          <span className="font-semibold text-red-400 text-left">{vuln.type || "Bilinmeyen Zafiyet"}</span>
                          <span className="text-[10px] uppercase tracking-wider px-2 py-1 bg-red-950/50 text-red-400 rounded-sm font-bold">
                            {vuln.severity || "YÜKSEK"}
                          </span>
                        </div>
                        <div className="p-4 text-zinc-400 space-y-3">
                          <p className="text-sm leading-relaxed">{vuln.description}</p>
                          <div className="bg-zinc-900 p-3 rounded border border-zinc-800 font-mono text-xs">
                            <span className="text-zinc-500 block mb-1">// Tespit Edilen Konum:</span>
                            <span className="text-cyan-400">{vuln.file_path || "Belirtilmemiş"}</span>
                          </div>
                          {vuln.recommendation && (
                            <div className="bg-emerald-950/30 border border-emerald-900/30 p-3 rounded text-emerald-400/90 text-sm">
                              <strong>Çözüm Önerisi:</strong> {vuln.recommendation}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* İkonlu Dosya Mimarisi (AST) Kartı */}
            <div className="bg-zinc-900/50 p-6 rounded-2xl border border-zinc-800 shadow-lg flex flex-col h-[450px]">
              <h3 className="text-xl font-bold text-emerald-400 mb-4 flex items-center gap-2 shrink-0">
                <FileCode2 size={20} /> Proje Mimarisi (AST)
              </h3>
              <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-1">
                {!analysisData.repository_files || analysisData.repository_files.length === 0 ? (
                  <div className="flex flex-col items-center justify-center h-full text-zinc-500">
                    <p>Dosya yapısı okunamadı.</p>
                  </div>
                ) : (
                  <div className="bg-zinc-950 p-4 rounded-lg border border-zinc-800/50 font-mono text-sm">
                    {analysisData.repository_files.map((file: any, index: number) => {
                      const isFolder = file.path?.endsWith('/') || !file.path?.includes('.');
                      return (
                        <div key={index} className="flex items-center gap-2 p-1.5 hover:bg-zinc-900 rounded cursor-pointer transition-colors group">
                          {isFolder ? (
                            <Folder size={16} className="text-emerald-500/70 group-hover:text-emerald-400" />
                          ) : (
                            <FileText size={16} className="text-zinc-500 group-hover:text-zinc-300" />
                          )}
                          <span className={`${isFolder ? 'text-emerald-400/90' : 'text-zinc-400'} truncate`}>
                            {file.path || file.name || file}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>

          </div>
        </div>
      )}
    </main>
  );
}