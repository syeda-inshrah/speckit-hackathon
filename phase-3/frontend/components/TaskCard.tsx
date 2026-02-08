"use client";

import { useState } from "react";
import Badge from "./ui/Badge";
import Button from "./ui/Button";
import Modal from "./ui/Modal";

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskCardProps {
  task: Task;
  onToggleComplete: (taskId: number) => void;
  onUpdate: (taskId: number, data: { title: string; description?: string }) => void;
  onDelete: (taskId: number) => void;
}

export default function TaskCard({
  task,
  onToggleComplete,
  onUpdate,
  onDelete,
}: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({
    title: task.title,
    description: task.description || "",
  });
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  const handleSave = () => {
    if (editData.title.trim()) {
      onUpdate(task.id, {
        title: editData.title,
        description: editData.description || undefined,
      });
      setIsEditing(false);
    }
  };

  const handleCancel = () => {
    setEditData({
      title: task.title,
      description: task.description || "",
    });
    setIsEditing(false);
  };

  const handleDelete = () => {
    onDelete(task.id);
    setShowDeleteModal(false);
  };

  // Calculate task age
  const getTaskAge = () => {
    const created = new Date(task.created_at);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - created.getTime());
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return `${Math.floor(diffDays / 30)} months ago`;
  };

  return (
    <>
      <div
        className={`
          relative overflow-hidden
          bg-white rounded-2xl shadow-md
          p-6
          transition-all duration-300
          hover:shadow-xl hover:scale-[1.01]
          animate-slide-up
          ${task.completed ? "opacity-75" : ""}
        `}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {/* Decorative gradient overlay */}
        <div
          className={`
            absolute top-0 right-0 w-32 h-32
            bg-gradient-to-br from-blue-500 to-purple-500
            opacity-0 rounded-full blur-2xl
            transform translate-x-8 -translate-y-8
            transition-opacity duration-300
            ${isHovered ? "opacity-10" : ""}
          `}
        />

        {/* Completion indicator bar */}
        {task.completed && (
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-green-500 to-green-600" />
        )}

        {isEditing ? (
          <div className="space-y-4 relative">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Title
              </label>
              <input
                type="text"
                value={editData.title}
                onChange={(e) => setEditData({ ...editData, title: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="Task title"
                maxLength={200}
              />
              <p className="mt-1 text-xs text-gray-500">
                {editData.title.length}/200 characters
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                value={editData.description}
                onChange={(e) =>
                  setEditData({ ...editData, description: e.target.value })
                }
                className="w-full px-4 py-2 border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="Task description (optional)"
                rows={3}
                maxLength={1000}
              />
              <p className="mt-1 text-xs text-gray-500">
                {editData.description.length}/1000 characters
              </p>
            </div>
            <div className="flex gap-2">
              <Button variant="primary" size="sm" onClick={handleSave}>
                Save Changes
              </Button>
              <Button variant="ghost" size="sm" onClick={handleCancel}>
                Cancel
              </Button>
            </div>
          </div>
        ) : (
          <>
            <div className="flex items-start gap-4 relative">
              {/* Custom Checkbox */}
              <button
                onClick={() => onToggleComplete(task.id)}
                className={`
                  flex-shrink-0 mt-1
                  w-7 h-7 rounded-lg border-2
                  flex items-center justify-center
                  transition-all duration-300
                  ${
                    task.completed
                      ? "bg-gradient-to-br from-green-500 to-green-600 border-green-600 shadow-lg shadow-green-500/30"
                      : "border-gray-300 hover:border-blue-500 hover:shadow-md"
                  }
                `}
              >
                {task.completed && (
                  <svg
                    className="w-5 h-5 text-white animate-scale-in"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={3}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                )}
              </button>

              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2 mb-2">
                  <h3
                    className={`
                      text-lg font-semibold
                      transition-all duration-300
                      ${
                        task.completed
                          ? "line-through text-gray-500"
                          : "text-gray-900"
                      }
                    `}
                  >
                    {task.title}
                  </h3>
                  {task.completed && (
                    <Badge variant="success" size="sm" className="animate-bounce-in">
                      ✓ Done
                    </Badge>
                  )}
                </div>

                {task.description && (
                  <p
                    className={`
                      text-sm mb-3
                      transition-colors duration-300
                      ${task.completed ? "text-gray-400" : "text-gray-600"}
                    `}
                  >
                    {task.description}
                  </p>
                )}

                <div className="flex items-center gap-3 text-xs text-gray-400">
                  <span className="flex items-center gap-1">
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    {getTaskAge()}
                  </span>
                </div>
              </div>
            </div>

            {/* Action Buttons - Appear on hover */}
            <div
              className={`
                mt-4 flex gap-2
                transition-all duration-300
                ${isHovered ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2"}
              `}
            >
              <Button
                variant="secondary"
                size="sm"
                onClick={() => setIsEditing(true)}
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                  />
                </svg>
                Edit
              </Button>
              <Button
                variant="danger"
                size="sm"
                onClick={() => setShowDeleteModal(true)}
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
                Delete
              </Button>
            </div>
          </>
        )}
      </div>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onConfirm={handleDelete}
        title="Delete Task"
        description="Are you sure you want to delete this task? This action cannot be undone."
        confirmText="Delete"
        cancelText="Cancel"
        variant="danger"
      />
    </>
  );
}
