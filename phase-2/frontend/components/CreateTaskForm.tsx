"use client";

import { useState, FormEvent } from "react";
import Button from "./ui/Button";

interface CreateTaskFormProps {
  onCreateTask: (data: { title: string; description?: string }) => void;
  loading?: boolean;
}

export default function CreateTaskForm({
  onCreateTask,
  loading = false,
}: CreateTaskFormProps) {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
  });
  const [error, setError] = useState("");
  const [isExpanded, setIsExpanded] = useState(false);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    setError("");

    if (!formData.title.trim()) {
      setError("Task title is required");
      return;
    }

    if (formData.title.length > 200) {
      setError("Task title must be 200 characters or less");
      return;
    }

    if (formData.description && formData.description.length > 1000) {
      setError("Task description must be 1000 characters or less");
      return;
    }

    onCreateTask({
      title: formData.title.trim(),
      description: formData.description.trim() || undefined,
    });

    // Reset form
    setFormData({ title: "", description: "" });
    setIsExpanded(false);
  };

  return (
    <div className="relative overflow-hidden bg-white rounded-2xl shadow-lg animate-slide-up">
      {/* Decorative gradient background */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-blue-500 to-purple-500 opacity-5 rounded-full blur-3xl transform translate-x-32 -translate-y-32" />

      <div className="relative p-6">
        {!isExpanded ? (
          /* Collapsed State - Quick Add Button */
          <button
            onClick={() => setIsExpanded(true)}
            className="
              w-full flex items-center gap-3 p-4
              bg-gradient-to-r from-blue-50 to-purple-50
              hover:from-blue-100 hover:to-purple-100
              rounded-xl
              transition-all duration-300
              group
            "
          >
            <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/30 group-hover:shadow-xl group-hover:shadow-blue-500/40 transition-all">
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 4v16m8-8H4"
                />
              </svg>
            </div>
            <div className="flex-1 text-left">
              <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                Add a new task
              </h3>
              <p className="text-sm text-gray-500">
                Click to create a task with title and description
              </p>
            </div>
            <svg
              className="w-5 h-5 text-gray-400 group-hover:text-blue-600 transition-colors"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </button>
        ) : (
          /* Expanded State - Full Form */
          <form onSubmit={handleSubmit} className="space-y-5 animate-scale-in">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-gray-900">
                Create New Task
              </h2>
              <button
                type="button"
                onClick={() => {
                  setIsExpanded(false);
                  setFormData({ title: "", description: "" });
                  setError("");
                }}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg
                  className="w-6 h-6"
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

            {error && (
              <div className="rounded-lg bg-red-50 border border-red-200 p-4 animate-scale-in">
                <div className="flex items-start gap-3">
                  <svg
                    className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <p className="text-sm text-red-800">{error}</p>
                </div>
              </div>
            )}

            <div>
              <label
                htmlFor="title"
                className="block text-sm font-semibold text-gray-700 mb-2"
              >
                Title <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                id="title"
                value={formData.title}
                onChange={(e) =>
                  setFormData({ ...formData, title: e.target.value })
                }
                className="
                  w-full px-4 py-3
                  bg-gray-50 border border-gray-200
                  rounded-xl
                  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:bg-white
                  transition-all duration-200
                  placeholder-gray-400
                "
                placeholder="Enter task title..."
                maxLength={200}
                disabled={loading}
                autoFocus
              />
              <div className="mt-2 flex items-center justify-between">
                <p className="text-xs text-gray-500">
                  {formData.title.length}/200 characters
                </p>
                {formData.title.length > 180 && (
                  <span className="text-xs text-yellow-600 font-medium">
                    ⚠ Approaching limit
                  </span>
                )}
              </div>
            </div>

            <div>
              <label
                htmlFor="description"
                className="block text-sm font-semibold text-gray-700 mb-2"
              >
                Description <span className="text-gray-400 font-normal">(optional)</span>
              </label>
              <textarea
                id="description"
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                className="
                  w-full px-4 py-3
                  bg-gray-50 border border-gray-200
                  rounded-xl
                  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:bg-white
                  transition-all duration-200
                  placeholder-gray-400
                  resize-none
                "
                placeholder="Add more details about this task..."
                rows={4}
                maxLength={1000}
                disabled={loading}
              />
              <div className="mt-2 flex items-center justify-between">
                <p className="text-xs text-gray-500">
                  {formData.description.length}/1000 characters
                </p>
                {formData.description.length > 900 && (
                  <span className="text-xs text-yellow-600 font-medium">
                    ⚠ Approaching limit
                  </span>
                )}
              </div>
            </div>

            <div className="flex gap-3 pt-2">
              <Button
                type="submit"
                variant="primary"
                size="lg"
                fullWidth
                isLoading={loading}
                disabled={loading || !formData.title.trim()}
              >
                {loading ? "Creating..." : "Create Task"}
              </Button>
              <Button
                type="button"
                variant="ghost"
                size="lg"
                onClick={() => {
                  setIsExpanded(false);
                  setFormData({ title: "", description: "" });
                  setError("");
                }}
                disabled={loading}
              >
                Cancel
              </Button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
