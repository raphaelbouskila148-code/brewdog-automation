@echo off
REM Builds the Allure report from the last test run and saves it as allure-report\index.html
set "TOOLS=%USERPROFILE%\Downloads\allure_tools"
set "JAVA_HOME=%TOOLS%\jdk-21.0.13+9-jre"
set "PATH=%JAVA_HOME%\bin;%TOOLS%\allure-2.46.1\bin;%PATH%"
if not exist "%~dp0allure-results" (
    echo No allure-results folder found. Run the tests first, then try again.
    pause
    exit /b
)
call allure generate "%~dp0allure-results" -o "%~dp0allure-report" --clean --single-file
echo Report saved to: %~dp0allure-report\index.html
start "" "%~dp0allure-report\index.html"
pause
