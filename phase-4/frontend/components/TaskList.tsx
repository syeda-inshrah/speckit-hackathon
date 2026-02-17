"use client";

import { useState, useMemo } from "react";
import TaskCard from "./TaskCard";
import Badge from "./ui/Badge";

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  filter: "all" | "pending" | "completed";
  onToggleComplete: (taskId: number) => void;
  onUpdate: (taskId: number, data: { title: string; description?: string }) => void;
  onDelete: (taskId: number) => void;
}

export default function TaskList({
  tasks,
  filter,
  onToggleComplete,
  onUpdate,
  onDelete,
}: TaskListProps) {
  const [searchQuery, setSearchQuery] = useState("");

  // Filter and search tasks
  const filteredTasks = useMemo(() => {
    let filtered = tasks;

    // Apply status filter
    if (filter === "pending") {
      filtered = filtered.filter((task) => !task.completed);
    } else if (filter === "completed") {
      filtered = filtered.filter((task) => task.completed);
    }

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (task) =>
          task.title.toLowerCase().includes(query) ||
          task.description?.toLowerCase().includes(query)
      );
    }

    return filtered;
  }, [tasks, filter, searchQuery]);

  // Empty state messages
  const getEmptyStateMessage = () => {
    if (searchQuery.trim()) {
      return {
        icon: "🔍",
        title: "No tasks found",
        message: `No tasks match "${searchQuery}". Try a different search term.`,
      };
    }

    if (filter === "completed") {
      return {
        icon: "🎯",
        title: "No completed tasks yet",
        message: "Complete some tasks to see them here!",
      };
    }

    if (filter === "pending") {
      return {
        icon: "🎉",
        title: "All caught up!",
        message: "You have no pending tasks. Great job!",
      };
    }

    return {
      icon: "📝",
      title: "No tasks yet",
      message: "Create your first task to get started!",
    };
  };

  const emptyState = getEmptyStateMessage();

  return (
    <div className="space-y-6">
      {/* Search Bar */}
      {tasks.length > 0 && (
        <div className="relative animate-slide-up">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg
              className="h-5 w-5 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search tasks..."
            className="
              w-full pl-12 pr-4 py-3
              bg-white rounded-xl
              border border-gray-200
              shadow-sm
              focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
              transition-all duration-200
              placeholder-gray-400
            "
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="
                absolute inset-y-0 right-0 pr-4
                flex items-center
                text-gray-400 hover:text-gray-600
                transition-colors
              "
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
          )}
        </div>
      )}

      {/* Task List */}
      {filteredTasks.length > 0 ? (
        <div className="space-y-4">
          {/* Section Header */}
          <div className="flex items-center gap-3 animate-slide-up">
            <div className="h-1 w-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full" />
            <h2 className="text-lg font-semibold text-gray-900">
              {filter === "all" && "All Tasks"}
              {filter === "pending" && "Pending Tasks"}
              {filter === "completed" && "Completed Tasks"}
            </h2>
            <Badge variant="default" size="md">
              {filteredTasks.length}
            </Badge>
          </div>

          {/* Tasks with staggered animation */}
          <div className="space-y-4">
            {filteredTasks.map((task, index) => (
              <div
                key={task.id}
                style={{
                  animationDelay: `${index * 50}ms`,
                }}
                className="animate-slide-up"
              >
                <TaskCard
                  task={task}
                  onToggleComplete={onToggleComplete}
                  onUpdate={onUpdate}
                  onDelete={onDelete}
                />
              </div>
            ))}
          </div>
        </div>
      ) : (
        /* Empty State */
        <div className="text-center py-16 animate-fade-in">
          <div className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-gradient-to-br from-blue-50 to-purple-50 mb-6 animate-float">
            <span className="text-5xl">{emptyState.icon}</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">
            {emptyState.title}
          </h3>
          <p className="text-gray-600 max-w-md mx-auto">
            {emptyState.message}
          </p>
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="
                mt-6 px-6 py-2
                bg-gradient-to-r from-blue-600 to-blue-700
                text-white font-medium rounded-lg
                shadow-lg shadow-blue-500/30
                hover:shadow-xl hover:shadow-blue-500/40
                transform hover:scale-105
                transition-all duration-200
              "
            >
              Clear Search
            </button>
          )}
        </div>
      )}
    </div>
  );
}
