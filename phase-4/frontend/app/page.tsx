import Link from "next/link";
import Button from "@/components/ui/Button";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-indigo-50 relative overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse-slow" />
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: "1s" }} />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Navigation */}
        <nav className="flex items-center justify-between py-6 animate-slide-up">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
              <span className="text-3xl">✓</span>
            </div>
            <h1 className="text-2xl font-bold gradient-text">Todo App</h1>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/signin">
              <Button variant="ghost" size="md">
                Sign In
              </Button>
            </Link>
            <Link href="/signup">
              <Button variant="primary" size="md">
                Get Started
              </Button>
            </Link>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="flex flex-col items-center justify-center text-center py-20 sm:py-32 animate-fade-in">
          <div className="mb-8 inline-flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full shadow-lg animate-bounce-in">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse-slow"></div>
            <span className="text-sm font-medium text-gray-700">
              ✨ Premium Task Management
            </span>
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold text-gray-900 mb-6 animate-slide-up">
            Organize Your Life
            <br />
            <span className="gradient-text">One Task at a Time</span>
          </h1>

          <p className="text-xl sm:text-2xl text-gray-600 mb-12 max-w-3xl animate-slide-up" style={{ animationDelay: "100ms" }}>
            A beautiful, modern task management application designed to help you
            stay productive and focused. Built with cutting-edge technology.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 mb-16 animate-slide-up" style={{ animationDelay: "200ms" }}>
            <Link href="/signup">
              <Button variant="primary" size="lg">
                <svg
                  className="w-5 h-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
                Start Free Today
              </Button>
            </Link>
            <Link href="/signin">
              <Button variant="secondary" size="lg">
                <svg
                  className="w-5 h-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M14 5l7 7m0 0l-7 7m7-7H3"
                  />
                </svg>
                Sign In
              </Button>
            </Link>
          </div>

          {/* Feature Preview Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl">
            {[
              {
                icon: "✓",
                title: "Easy Task Management",
                description: "Create, update, and organize tasks with an intuitive interface",
                gradient: "from-blue-500 to-blue-600",
                delay: "0ms",
              },
              {
                icon: "🔒",
                title: "Secure & Private",
                description: "Your data is protected with JWT authentication and encryption",
                gradient: "from-purple-500 to-purple-600",
                delay: "100ms",
              },
              {
                icon: "⚡",
                title: "Lightning Fast",
                description: "Built with Next.js and FastAPI for optimal performance",
                gradient: "from-indigo-500 to-indigo-600",
                delay: "200ms",
              },
            ].map((feature, index) => (
              <div
                key={index}
                className="relative overflow-hidden bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl p-8 transform transition-all duration-300 hover:scale-105 hover:shadow-2xl animate-slide-up"
                style={{ animationDelay: feature.delay }}
              >
                <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${feature.gradient} opacity-10 rounded-full blur-2xl transform translate-x-8 -translate-y-8`} />
                <div className="relative">
                  <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center text-3xl mb-4 shadow-lg`}>
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">
                    {feature.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Stats Section */}
        <div className="py-16 border-t border-gray-200/50 animate-fade-in">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {[
              { value: "10K+", label: "Active Users" },
              { value: "50K+", label: "Tasks Completed" },
              { value: "99.9%", label: "Uptime" },
              { value: "24/7", label: "Support" },
            ].map((stat, index) => (
              <div key={index} className="animate-slide-up" style={{ animationDelay: `${index * 100}ms` }}>
                <div className="text-4xl font-bold gradient-text mb-2">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <footer className="py-8 border-t border-gray-200/50 text-center text-gray-600 animate-fade-in">
          <p className="text-sm">
            Built with Next.js 16, FastAPI, and PostgreSQL
          </p>
          <p className="text-xs mt-2">
            © 2026 Todo App. All rights reserved.
          </p>
        </footer>
      </div>
    </div>
  );
}
