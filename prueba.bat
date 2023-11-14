@echo off
:loop
    echo Haciendo GET a /ping
    curl http://localhost:8888/ping

    echo.
    timeout /t 1 /nobreak >nul

    echo Haciendo POST a /pedido con numero 5798
    curl -X POST http://localhost:8888/pedido -H "Content-Type: application/json" -d "{\"numero\": 5798}"

    echo.
    timeout /t 1 /nobreak >nul

    echo Haciendo GET a /pedidos
    curl http://localhost:8888/pedidos

    echo.
    timeout /t 1 /nobreak >nul

goto loop
