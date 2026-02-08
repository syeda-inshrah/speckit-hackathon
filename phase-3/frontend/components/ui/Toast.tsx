"use client";

import React, { useEffect } from "react";

export type ToastType = "success" | "error" | "info" | "warning";

interface ToastProps {
  id: string;
  message: string;
  type: ToastType;
  duration?: number;
  onClose: (id: string) => void;
}

const typeStyles: Record<ToastType, { bg: string; icon: string; iconColor: string }> = {
  success: {
    bg: "bg-green-50 border-green-200",
    icon: "✓",
    iconColor: "text-green-600",
  },
  error: {
    bg: "bg-red-50 border-red-200",
    icon: "✕",
    iconColor: "text-red-600",
  },
  info: {
    bg: "bg-blue-50 border-blue-200",
    icon: "ℹ",
    iconColor: "text-blue-600",
  },
  warning: {
    bg: "bg-yellow-50 border-yellow-200",
    icon: "⚠",
    iconColor: "text-yellow-600",
  },
};

export default function Toast({
  id,
  message,
  type,
  duration = 5000,
  onClose,
}: ToastProps) {
  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        onClose(id);
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [id, duration, onClose]);

  const styles = typeStyles[type];

  return (
    <div
      className={`
        flex items-start gap-3 p-4 rounded-lg border shadow-lg
        min-w-[300px] max-w-md
        animate-slide-in-right
        ${styles.bg}
      `}
    >
      <div className={`flex-shrink-0 text-xl font-bold ${styles.iconColor}`}>
        {styles.icon}
      </div>
      <div className="flex-1 text-sm text-gray-800">{message}</div>
      <button
        onClick={() => onClose(id)}
        className="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors"
      >
        <svg
          className="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
    </div>
  );
}
