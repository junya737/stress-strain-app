"use client";

import { useCallback, useRef, useState } from "react";
import { useSpecimenStore } from "@/stores/specimenStore";
import { uploadDataset } from "@/lib/apiClient";

export function FileUploader() {
  const { addDataset, setLoading, setError } = useSpecimenStore();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragOver, setIsDragOver] = useState(false);

  const handleFile = useCallback(
    async (file: File) => {
      setLoading(true);
      setError(null);
      try {
        const result = await uploadDataset(file);
        addDataset(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Upload failed");
      } finally {
        setLoading(false);
      }
    },
    [addDataset, setLoading, setError]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    [handleFile]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setIsDragOver(false);
  }, []);

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
    // Reset input so same file can be re-uploaded
    e.target.value = "";
  };

  return (
    <div>
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={handleClick}
        className={`cursor-pointer rounded-lg border-2 border-dashed p-4 text-center transition-colors ${
          isDragOver
            ? "border-primary bg-primary/5"
            : "border-border hover:border-primary/50"
        }`}
      >
        <svg
          className="mx-auto mb-1 h-8 w-8 text-foreground/30"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
        <p className="text-xs text-foreground/50">
          Drop CSV here or click to browse
        </p>
      </div>
      <input
        ref={fileInputRef}
        type="file"
        accept=".csv,.tsv,.txt"
        onChange={handleInputChange}
        className="hidden"
      />
    </div>
  );
}
