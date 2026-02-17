# Todo App - Frontend

A modern, full-stack task management application built with Next.js 16+, featuring authentication, CRUD operations, and a responsive UI.

## 🚀 Features

### Phase II - Basic Level Features (Completed)
- ✅ **User Authentication** - Signup and signin with JWT tokens
- ✅ **Add Task** - Create new todo items with title and description
- ✅ **View Tasks** - Display all tasks with filtering options
- ✅ **Update Task** - Edit task details inline
- ✅ **Delete Task** - Remove tasks with confirmation dialog
- ✅ **Mark Complete** - Toggle task completion status with checkbox

### Additional Features
- 🔒 **Secure Authentication** - JWT-based authentication with Better Auth
- 🎨 **Modern UI** - Clean, responsive design with Tailwind CSS
- 📊 **Task Statistics** - Real-time stats for total, pending, and completed tasks
- 🔍 **Task Filtering** - Filter tasks by all, pending, or completed status
- ⚡ **Real-time Updates** - Instant UI updates after task operations
- 🛡️ **Route Protection** - Middleware-based authentication guards
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices

## 🛠️ Technology Stack

- **Next.js 16+** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **Better Auth** - Authentication library
- **js-cookie** - Cookie management

## 📋 Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Backend API running on `http://localhost:8000`

## 🔧 Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd phase-2/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**

   Create a `.env.local` file:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=X9Wk9_Pqznh1o6aAIHSd8xvOqy5iy21QqNH_-9k8cxU
   BETTER_AUTH_URL=http://localhost:3000
   ```

## 🚀 Running the Application

### Development Mode

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Production Build

```bash
npm run build
npm start
```

## 📁 Project Structure

```
frontend/
├── app/                      # Next.js App Router pages
│   ├── page.tsx             # Home/landing page
│   ├── signup/page.tsx      # Signup page
│   ├── signin/page.tsx      # Signin page
│   └── dashboard/page.tsx   # Main dashboard
├── components/              # Reusable React components
│   ├── TaskCard.tsx        # Individual task card
│   ├── TaskList.tsx        # List of tasks
│   └── CreateTaskForm.tsx  # Form to create tasks
├── lib/                     # Utility libraries
│   ├── api-client.ts       # API client with interceptors
│   └── auth.ts             # Auth configuration
├── middleware.ts            # Route protection
└── .env.local              # Environment variables
```

## 🔐 Authentication Flow

1. **Signup** - Create account with name, email, password
2. **Signin** - Authenticate with email and password
3. **JWT Token** - Stored in cookies for API requests
4. **Route Protection** - Middleware guards protected routes
5. **Signout** - Clears token and redirects to signin

## 📊 API Integration

### Authentication Endpoints
- `POST /api/auth/signup` - Create new user
- `POST /api/auth/signin` - Authenticate user

### Task Endpoints
- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion
- `DELETE /api/{user_id}/tasks/{id}` - Delete task

## 🧪 Testing

### Start Both Servers

```bash
# Terminal 1: Backend
cd phase-2/backend
uvicorn src.main:app --reload

# Terminal 2: Frontend
cd phase-2/frontend
npm run dev
```

### Manual Testing Checklist

- [ ] Signup with valid credentials
- [ ] Signin with valid credentials
- [ ] Create task with title and description
- [ ] View all tasks
- [ ] Filter by pending/completed
- [ ] Mark task as complete
- [ ] Edit task details
- [ ] Delete task with confirmation
- [ ] Signout functionality

## 🐛 Troubleshooting

**"Failed to fetch tasks" error:**
- Ensure backend is running on port 8000
- Check `.env.local` has correct API URL
- Verify JWT token in browser cookies

**Authentication not working:**
- Ensure `BETTER_AUTH_SECRET` matches backend
- Clear browser cookies and try again

**CORS errors:**
- Verify backend CORS includes `http://localhost:3000`

## 🚢 Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import repository to Vercel
3. Set root directory to `phase-2/frontend`
4. Add environment variables
5. Deploy

## ✅ Phase II Status

**Frontend Implementation: 100% Complete**

All 5 Basic Level features implemented:
- ✅ Add Task
- ✅ Delete Task
- ✅ Update Task
- ✅ View Task List
- ✅ Mark as Complete

---

**Built with ❤️ using Next.js, TypeScript, and Tailwind CSS**
