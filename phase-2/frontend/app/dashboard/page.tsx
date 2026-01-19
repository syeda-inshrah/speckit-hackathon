"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { authApi, tasksApi } from "@/lib/api-client";
import CreateTaskForm from "@/components/CreateTaskForm";
import TaskList from "@/components/TaskList";
import TaskStats from "@/components/ui/TaskStats";
import LoadingSkeleton from "@/components/ui/LoadingSkeleton";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import { useToast } from "@/components/ui/ToastContainer";

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const { showToast } = useToast();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<"all" | "pending" | "completed">("all");
  const [loading, setLoading] = useState(true);
  const [createLoading, setCreateLoading] = useState(false);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const user = authApi.getCurrentUser();
      if (!user) {
        router.push("/signin");
        return;
      }
      const data = await tasksApi.list(user.id);
      setTasks(data);
    } catch (err: any) {
      showToast(err.response?.data?.detail || "Failed to fetch tasks", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (data: {
    title: string;
    description?: string;
  }) => {
    try {
      setCreateLoading(true);
      const user = authApi.getCurrentUser();
      if (!user) {
        router.push("/signin");
        return;
      }
      const newTask = await tasksApi.create(user.id, data);
      setTasks([newTask, ...tasks]);
      showToast("Task created successfully!", "success");
    } catch (err: any) {
      showToast(err.response?.data?.detail || "Failed to create task", "error");
    } finally {
      setCreateLoading(false);
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    try {
      const user = authApi.getCurrentUser();
      if (!user) {
        router.push("/signin");
        return;
      }
      const updatedTask = await tasksApi.toggleComplete(user.id, taskId);
      setTasks(
        tasks.map((task) => (task.id === taskId ? updatedTask : task))
      );
      showToast(
        updatedTask.completed ? "Task completed! 🎉" : "Task marked as pending",
        "success"
      );
    } catch (err: any) {
      showToast(err.response?.data?.detail || "Failed to update task", "error");
    }
  };

  const handleUpdateTask = async (
    taskId: number,
    data: { title: string; description?: string }
  ) => {
    try {
      const user = authApi.getCurrentUser();
      if (!user) {
        router.push("/signin");
        return;
      }
      const updatedTask = await tasksApi.update(user.id, taskId, data);
      setTasks(
        tasks.map((task) => (task.id === taskId ? updatedTask : task))
      );
      showToast("Task updated successfully!", "success");
    } catch (err: any) {
      showToast(err.response?.data?.detail || "Failed to update task", "error");
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    try {
      const user = authApi.getCurrentUser();
      if (!user) {
        router.push("/signin");
        return;
      }
      await tasksApi.delete(user.id, taskId);
      setTasks(tasks.filter((task) => task.id !== taskId));
      showToast("Task deleted successfully", "info");
    } catch (err: any) {
      showToast(err.response?.data?.detail || "Failed to delete task", "error");
    }
  };

  const handleSignOut = () => {
    authApi.signout();
  };

  const stats = {
    total: tasks.length,
    pending: tasks.filter((t) => !t.completed).length,
    completed: tasks.filter((t) => t.completed).length,
  };

  // Get time-based greeting
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return "Good morning";
    if (hour < 18) return "Good afternoon";
    return "Good evening";
  };

  const completionRate = stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
      {/* Premium Navigation Bar with Glass Effect */}
      <nav className="sticky top-0 z-40 glass-effect border-b border-white/20 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
                <span className="text-2xl">✓</span>
              </div>
              <h1 className="text-2xl font-bold gradient-text">Todo App</h1>
            </div>
            <div className="flex items-center gap-4">
              <div className="hidden sm:flex items-center gap-2 px-4 py-2 bg-white/50 rounded-lg">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse-slow"></div>
                <span className="text-sm font-medium text-gray-700">
                  {stats.pending} pending
                </span>
              </div>
              <Button variant="ghost" size="sm" onClick={handleSignOut}>
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
                    d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                  />
                </svg>
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <LoadingSkeleton />
        ) : (
          <div className="space-y-8">
            {/* Welcome Section */}
            <div className="relative overflow-hidden bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 rounded-3xl shadow-2xl shadow-blue-500/20 p-8 animate-slide-up">
              <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl transform translate-x-32 -translate-y-32"></div>
              <div className="relative">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
                  <div>
                    <h2 className="text-3xl font-bold text-white mb-2">
                      {getGreeting()}! 👋
                    </h2>
                    <p className="text-blue-100 text-lg">
                      {stats.pending === 0
                        ? "You're all caught up! Great job! 🎉"
                        : `You have ${stats.pending} task${stats.pending === 1 ? "" : "s"} to complete today.`}
                    </p>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-center">
                      <div className="text-4xl font-bold text-white mb-1">
                        {completionRate}%
                      </div>
                      <div className="text-sm text-blue-100">Complete</div>
                    </div>
                    <div className="w-24 h-24 relative">
                      <svg className="transform -rotate-90 w-24 h-24">
                        <circle
                          cx="48"
                          cy="48"
                          r="40"
                          stroke="rgba(255,255,255,0.2)"
                          strokeWidth="8"
                          fill="none"
                        />
                        <circle
                          cx="48"
                          cy="48"
                          r="40"
                          stroke="white"
                          strokeWidth="8"
                          fill="none"
                          strokeDasharray={`${2 * Math.PI * 40}`}
                          strokeDashoffset={`${2 * Math.PI * 40 * (1 - completionRate / 100)}`}
                          strokeLinecap="round"
                          className="transition-all duration-1000"
                        />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Statistics Cards */}
            <TaskStats
              total={stats.total}
              pending={stats.pending}
              completed={stats.completed}
            />

            {/* Create Task Form */}
            <CreateTaskForm
              onCreateTask={handleCreateTask}
              loading={createLoading}
            />

            {/* Filter Buttons */}
            <div className="flex flex-wrap gap-3 animate-slide-up">
              <button
                onClick={() => setFilter("all")}
                className={`
                  flex items-center gap-2 px-6 py-3 rounded-xl font-medium
                  transition-all duration-300
                  ${
                    filter === "all"
                      ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg shadow-blue-500/30 scale-105"
                      : "bg-white text-gray-700 hover:bg-gray-50 shadow-md hover:shadow-lg"
                  }
                `}
              >
                All Tasks
                <Badge variant={filter === "all" ? "default" : "default"} size="sm">
                  {stats.total}
                </Badge>
              </button>
              <button
                onClick={() => setFilter("pending")}
                className={`
                  flex items-center gap-2 px-6 py-3 rounded-xl font-medium
                  transition-all duration-300
                  ${
                    filter === "pending"
                      ? "bg-gradient-to-r from-yellow-500 to-orange-500 text-white shadow-lg shadow-yellow-500/30 scale-105"
                      : "bg-white text-gray-700 hover:bg-gray-50 shadow-md hover:shadow-lg"
                  }
                `}
              >
                Pending
                <Badge variant={filter === "pending" ? "default" : "warning"} size="sm">
                  {stats.pending}
                </Badge>
              </button>
              <button
                onClick={() => setFilter("completed")}
                className={`
                  flex items-center gap-2 px-6 py-3 rounded-xl font-medium
                  transition-all duration-300
                  ${
                    filter === "completed"
                      ? "bg-gradient-to-r from-green-600 to-green-700 text-white shadow-lg shadow-green-500/30 scale-105"
                      : "bg-white text-gray-700 hover:bg-gray-50 shadow-md hover:shadow-lg"
                  }
                `}
              >
                Completed
                <Badge variant={filter === "completed" ? "default" : "success"} size="sm">
                  {stats.completed}
                </Badge>
              </button>
            </div>

            {/* Task List */}
            <TaskList
              tasks={tasks}
              filter={filter}
              onToggleComplete={handleToggleComplete}
              onUpdate={handleUpdateTask}
              onDelete={handleDeleteTask}
            />
          </div>
        )}
      </main>
    </div>
  );
}
