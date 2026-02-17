@echo off
REM Quick Start Script for Phase 4 Deployment (Windows)
REM This script automates the deployment process to Minikube

echo ========================================
echo Phase 4 - Todo App Kubernetes Deployment
echo ========================================
echo.

REM Check prerequisites
echo Checking prerequisites...

where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not installed
    exit /b 1
)
echo [OK] Docker is installed

where minikube >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Minikube is not installed
    exit /b 1
)
echo [OK] Minikube is installed

where kubectl >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] kubectl is not installed
    exit /b 1
)
echo [OK] kubectl is installed

where helm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Helm is not installed
    exit /b 1
)
echo [OK] Helm is installed

echo.

REM Start Minikube
echo Starting Minikube...
minikube status | findstr "Running" >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Minikube is already running
) else (
    minikube start --cpus=4 --memory=8192 --disk-size=40g --driver=docker
    echo [OK] Minikube started
)

echo.

REM Configure Docker
echo Configuring Docker to use Minikube's daemon...
@FOR /f "tokens=*" %%i IN ('minikube docker-env --shell cmd') DO @%%i
echo [OK] Docker configured

echo.

REM Build images
echo Building Docker images...

echo   Building backend image...
docker build -t todo-backend:latest -f backend\Dockerfile backend
echo [OK] Backend image built

echo   Building frontend image...
docker build -t todo-frontend:latest -f frontend\Dockerfile frontend
echo [OK] Frontend image built

echo.

REM Verify images
echo Verifying images...
docker images | findstr todo
echo.

REM Deploy with Helm
echo Deploying with Helm...

REM Check environment variables
if "%DATABASE_URL%"=="" (
    echo [WARNING] DATABASE_URL not set. Using example value.
    set DATABASE_URL=postgresql://user:password@host:5432/database
)

if "%BETTER_AUTH_SECRET%"=="" (
    echo [WARNING] BETTER_AUTH_SECRET not set. Using example value.
    set BETTER_AUTH_SECRET=example-secret-key-min-32-characters-long
)

if "%GROQ_API_KEY%"=="" (
    echo [WARNING] GROQ_API_KEY not set. Using example value.
    set GROQ_API_KEY=example-groq-api-key
)

REM Install backend
echo   Installing backend...
helm upgrade --install backend helm\backend ^
    --set secrets.databaseUrl="%DATABASE_URL%" ^
    --set secrets.betterAuthSecret="%BETTER_AUTH_SECRET%" ^
    --set secrets.groqApiKey="%GROQ_API_KEY%" ^
    --wait
echo [OK] Backend deployed

REM Install frontend
echo   Installing frontend...
helm upgrade --install frontend helm\frontend --wait
echo [OK] Frontend deployed

echo.

REM Wait for pods
echo Waiting for pods to be ready...
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-backend --timeout=120s
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-frontend --timeout=120s
echo [OK] All pods are ready

echo.

REM Show status
echo Deployment Status:
echo.
kubectl get pods
echo.
kubectl get services
echo.

REM Get frontend URL
echo Access Information:
echo.
echo Frontend URL: Run 'minikube service frontend-todo-frontend --url'
echo Backend API: http://localhost:8001 (via port-forward)
echo.

echo [SUCCESS] Deployment complete!
echo.
echo Next steps:
echo   1. Get frontend URL: minikube service frontend-todo-frontend --url
echo   2. Port-forward backend: kubectl port-forward service/backend-todo-backend 8001:8001
echo   3. View logs: kubectl logs -f [pod-name]
echo.
