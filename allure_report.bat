@echo off
REM Opens a temporary Allure report from the last test run (like "allure serve").
REM Uses the Java + Allure copy in Downloads\allure_tools, so nothing needs to be installed.
set "TOOLS=%USERPROFILE%\Downloads\allure_tools"
set "JAVA_HOME=%TOOLS%\jdk-21.0.13+9-jre"
set "PATH=%JAVA_HOME%\bin;%TOOLS%\allure-2.46.1\bin;%PATH%"
if not exist "%~dp0allure-results" (
    echo No allure-results folder found. Run the tests first, then try again.
    pause
    exit /b
)
call allure serve "%~dp0allure-results"
