import React from "react";

interface TaskStatsProps {
  total: number;
  pending: number;
  completed: number;
}

export default function TaskStats({ total, pending, completed }: TaskStatsProps) {
  const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

  const stats = [
    {
      label: "Total Tasks",
      value: total,
      icon: "📋",
      gradient: "from-blue-500 to-blue-600",
      shadowColor: "shadow-blue-500/20",
      bgGradient: "from-blue-50 to-blue-100",
    },
    {
      label: "Active",
      value: pending,
      icon: "⏳",
      gradient: "from-yellow-500 to-orange-500",
      shadowColor: "shadow-yellow-500/20",
      bgGradient: "from-yellow-50 to-orange-100",
    },
    {
      label: "Completed",
      value: completed,
      icon: "✓",
      gradient: "from-green-500 to-green-600",
      shadowColor: "shadow-green-500/20",
      bgGradient: "from-green-50 to-green-100",
      subtitle: `${completionRate}% done`,
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      {stats.map((stat, index) => (
        <div
          key={stat.label}
          className={`
            relative overflow-hidden
            bg-white rounded-2xl shadow-lg ${stat.shadowColor}
            p-6
            transform transition-all duration-300
            hover:scale-105 hover:shadow-xl
            animate-slide-up
          `}
          style={{ animationDelay: `${index * 100}ms` }}
        >
          {/* Decorative gradient overlay */}
          <div
            className={`
              absolute top-0 right-0 w-32 h-32
              bg-gradient-to-br ${stat.gradient}
              opacity-10 rounded-full blur-2xl
              transform translate-x-8 -translate-y-8
            `}
          />

          {/* Content */}
          <div className="relative">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-medium text-gray-600">
                {stat.label}
              </span>
              <span className="text-2xl animate-pulse-slow">{stat.icon}</span>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-bold text-gray-900">
                {stat.value}
              </span>
              {stat.subtitle && (
                <span className="text-sm text-gray-500">{stat.subtitle}</span>
              )}
            </div>
          </div>

          {/* Pulse indicator */}
          <div className="absolute bottom-4 left-6">
            <div
              className={`
                w-2 h-2 rounded-full
                bg-gradient-to-r ${stat.gradient}
                animate-pulse-slow
              `}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
