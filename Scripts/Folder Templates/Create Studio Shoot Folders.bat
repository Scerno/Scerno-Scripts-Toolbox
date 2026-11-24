@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Drop one destination folder here. A Studio Shoot subfolder will be created.
rem Existing folders and files are preserved.

if "%~1"=="" goto usage
if not "%~2"=="" goto usage
if not exist "%~f1\." goto usage
set "root=%~f1\Studio Shoot"
if not exist "%root%\." (
    mkdir "%root%" || goto failed
)
for %%D in ("01 Originals" "02 Selects" "03 Corrected" "04 Editing\Archive" "05 Exports\Print" "05 Exports\Web") do (
    if not exist "%root%\%%~D\." (
        mkdir "%root%\%%~D" || goto failed
    )
)
echo Created folder layout in "%root%".
pause
exit /b 0

:usage
echo Drop one existing destination folder onto this batch file.
pause
exit /b 1

:failed
echo Could not create the complete layout in "%root%".
pause
exit /b 1
