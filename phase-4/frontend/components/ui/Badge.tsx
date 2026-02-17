import React from "react";

export type BadgeVariant = "default" | "success" | "warning" | "danger" | "info";
export type BadgeSize = "sm" | "md";

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  size?: BadgeSize;
  className?: string;
}

const variantStyles: Record<BadgeVariant, string> = {
  default: "bg-gray-100 text-gray-700 ring-gray-300",
  success: "bg-green-50 text-green-700 ring-green-300",
  warning: "bg-yellow-50 text-yellow-700 ring-yellow-300",
  danger: "bg-red-50 text-red-700 ring-red-300",
  info: "bg-blue-50 text-blue-700 ring-blue-300",
};

const sizeStyles: Record<BadgeSize, string> = {
  sm: "px-2 py-0.5 text-xs",
  md: "px-2.5 py-1 text-sm",
};

export default function Badge({
  children,
  variant = "default",
  size = "sm",
  className = "",
}: BadgeProps) {
  return (
    <span
      className={`
        inline-flex items-center justify-center
        font-medium rounded-full
        ring-1 ring-inset
        transition-all duration-200
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${className}
      `}
    >
      {children}
    </span>
  );
}
