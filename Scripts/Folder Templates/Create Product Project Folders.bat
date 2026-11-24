@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Drop one destination folder here. A Product Project subfolder will be created.
rem Existing folders and files are preserved.

if "%~1"=="" goto usage
if not "%~2"=="" goto usage
if not exist "%~f1\." goto usage
set "root=%~f1\Product Project"
if not exist "%root%\." (
    mkdir "%root%" || goto failed
)
for %%D in ("Documents\Specifications" "Documents\Manuals" "Documents\Certification" "Marketing" "Graphics" "Images\Studio" "Images\Location" "Renderings" "Video") do (
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
