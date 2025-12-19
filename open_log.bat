@echo off
setlocal

rem 脚本所在目录（带末尾反斜杠）
set "ROOT=%~dp0"

rem 日志目录（相对脚本目录）
set "LOG_DIR=%ROOT%out\build\vs2022\Debug\zhiz_logs"

rem 日志文件名（按需修改）
set "LOG_FILE=%LOG_DIR%\zhiz_tool.log"

if exist "%LOG_FILE%" (
  rem 用默认程序打开日志文件
  start "" "%LOG_FILE%"
) else (
  rem 找不到日志文件：打开目录并提示
  echo [WARN] Log file not found: "%LOG_FILE%"
  if exist "%LOG_DIR%" (
    start "" "%LOG_DIR%"
  ) else (
    echo [ERROR] Log dir not found: "%LOG_DIR%"
  )
  pause
)

endlocal
