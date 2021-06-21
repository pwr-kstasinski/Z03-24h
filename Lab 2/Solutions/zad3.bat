@echo OFF

net session >nul 2>&1
if %errorLevel% == 0 (
    echo "Skrypt uruchomiony jako admin"
) else (
    echo "Skrypt uruchomiony jako user"
)