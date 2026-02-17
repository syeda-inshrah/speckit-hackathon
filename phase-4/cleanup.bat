@echo off
REM Cleanup Script for Phase 4 Deployment (Windows)
REM This script removes all deployed resources

echo ===========================
echo Phase 4 - Cleanup Script
echo ===========================
echo.

REM Uninstall Helm releases
echo Uninstalling Helm releases...

helm list | findstr "frontend" >nul
if %ERRORLEVEL% EQU 0 (
    helm uninstall frontend
    echo [OK] Frontend uninstalled
) else (
    echo [WARNING] Frontend not found
)

helm list | findstr "backend" >nul
if %ERRORLEVEL% EQU 0 (
    helm uninstall backend
    echo [OK] Backend uninstalled
) else (
    echo [WARNING] Backend not found
)

echo.

REM Delete remaining resources
echo Deleting remaining resources...

kubectl delete deployment --all 2>nul
kubectl delete service --all 2>nul
kubectl delete configmap --all 2>nul
kubectl delete secret --all 2>nul

echo [OK] Resources cleaned up

echo.

REM Show status
echo Current Status:
kubectl get all

echo.
echo [SUCCESS] Cleanup complete!
echo.
echo To stop Minikube: minikube stop
echo To delete Minikube: minikube delete
