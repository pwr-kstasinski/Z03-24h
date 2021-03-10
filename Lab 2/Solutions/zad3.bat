@ECHO OFF

net session 1>nul 2>nul 

if not %errorLevel% equ 0 (
    echo You don't have administrator privileges
)

rem 1>nul 2>nul - standard out(1) and error output(2) send to nul (hide response)