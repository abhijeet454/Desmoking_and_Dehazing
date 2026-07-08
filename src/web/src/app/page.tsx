"use client";

import { useState, useRef } from "react";
import Image from "next/image";
import styles from "./page.module.css";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (!selectedFile.type.startsWith("image/")) {
        setError("Please select an image file.");
        return;
      }
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setResult(null);
      setError(null);
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleSubmit = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      // In production, this URL should be configured via environment variables
      const response = await fetch("http://localhost:8000/api/dehaze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to process image. Make sure the API is running.");
      }

      const blob = await response.blob();
      setResult(URL.createObjectURL(blob));
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unknown error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className={styles.main}>
      <h1 className={styles.title}>ClearVision AI</h1>
      <p className={styles.subtitle}>Advanced Image Desmoking & Dehazing powered by UNet</p>

      <div className={styles.card}>
        {!preview ? (
          <div className={styles.uploadArea} onClick={handleUploadClick}>
            <svg
              width="48"
              height="48"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#94a3b8"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              style={{ marginBottom: "1rem" }}
            >
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
            <p style={{ color: "#94a3b8", fontSize: "1.1rem" }}>
              Drag and drop an image, or click to browse
            </p>
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept="image/*"
              className={styles.fileInput}
            />
          </div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <div className={styles.imageComparison}>
              <div className={styles.imageBox}>
                <div className={styles.imageTitle}>Original Hazy Image</div>
                <div className={styles.imageWrapper}>
                  <Image src={preview} alt="Hazy Preview" fill className={styles.image} />
                </div>
              </div>

              {result && (
                <div className={styles.imageBox}>
                  <div className={styles.imageTitle}>Dehazed Result</div>
                  <div className={styles.imageWrapper}>
                    <Image src={result} alt="Dehazed Result" fill className={styles.image} />
                  </div>
                </div>
              )}
            </div>

            {loading && <div className={styles.loader}></div>}
            
            {error && <div className={styles.error}>{error}</div>}

            <div style={{ display: "flex", gap: "1rem", marginTop: "2rem" }}>
              <button
                className={styles.uploadButton}
                style={{ background: "#475569" }}
                onClick={() => {
                  setFile(null);
                  setPreview(null);
                  setResult(null);
                  setError(null);
                  if (fileInputRef.current) fileInputRef.current.value = "";
                }}
                disabled={loading}
              >
                Choose Another
              </button>
              
              {!result && (
                <button
                  className={styles.uploadButton}
                  onClick={handleSubmit}
                  disabled={loading || !file}
                >
                  {loading ? "Processing..." : "Dehaze Image"}
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
