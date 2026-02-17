import React from "react";

export type ButtonVariant = "primary" | "secondary" | "danger" | "ghost" | "success";
export type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  fullWidth?: boolean;
}

const variantStyles: Record<ButtonVariant, string> = {
  primary: `
    bg-gradient-to-r from-blue-600 to-blue-700
    hover:from-blue-700 hover:to-blue-800
    text-white shadow-lg shadow-blue-500/30
    hover:shadow-xl hover:shadow-blue-500/40
    active:scale-95
  `,
  secondary: `
    bg-gradient-to-r from-gray-100 to-gray-200
    hover:from-gray-200 hover:to-gray-300
    text-gray-700 shadow-md
    hover:shadow-lg
    active:scale-95
  `,
  danger: `
    bg-gradient-to-r from-red-600 to-red-700
    hover:from-red-700 hover:to-red-800
    text-white shadow-lg shadow-red-500/30
    hover:shadow-xl hover:shadow-red-500/40
    active:scale-95
  `,
  ghost: `
    bg-transparent hover:bg-gray-100
    text-gray-700 hover:text-gray-900
    active:scale-95
  `,
  success: `
    bg-gradient-to-r from-green-600 to-green-700
    hover:from-green-700 hover:to-green-800
    text-white shadow-lg shadow-green-500/30
    hover:shadow-xl hover:shadow-green-500/40
    active:scale-95
  `,
};

const sizeStyles: Record<ButtonSize, string> = {
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2 text-base",
  lg: "px-6 py-3 text-lg",
};

export default function Button({
  children,
  variant = "primary",
  size = "md",
  isLoading = false,
  fullWidth = false,
  disabled,
  className = "",
  ...props
}: ButtonProps) {
  return (
    <button
      disabled={disabled || isLoading}
      className={`
        inline-flex items-center justify-center gap-2
        font-medium rounded-lg
        transition-all duration-200
        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
        disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${fullWidth ? "w-full" : ""}
        ${className}
      `}
      {...props}
    >
      {isLoading && (
        <svg
          className="animate-spin h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}
      {children}
    </button>
  );
}
