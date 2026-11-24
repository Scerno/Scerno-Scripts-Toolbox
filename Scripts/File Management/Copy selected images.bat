@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Drop selected image files here. Copies go into Selected Images beside each source.
rem Uses your Explorer selection. It does not inspect rating metadata.

if "%~1"=="" goto usage
set "failed=0"

:next
if "%~1"=="" goto done
set "source=%~f1"
set "destination=%~dp1Selected Images"
set "target=%destination%\%~nx1"
if not exist "%source%" goto invalid
if exist "%source%\." goto invalid
for %%E in (.jpg .jpeg .png .tif .tiff .psd .webp .cr2 .cr3 .dng .nef .arw .raf .orf .rw2 .heic .gif .bmp .avif) do if /i "%~x1"=="%%E" goto copy_file
goto invalid

:copy_file
if exist "%target%" goto exists
if not exist "%destination%\." (
    mkdir "%destination%" || goto invalid
)
copy /-Y /B "%source%" "%target%" <nul >nul
if errorlevel 1 goto invalid
echo Copied "%source%" to "%target%"
goto advance

:exists
echo Skipped existing file: "%target%"
goto advance

:invalid
echo Could not copy image: "%source%"
set "failed=1"

:advance
shift
goto next

:usage
echo Drop selected image files onto this batch file.
echo Copies go into Selected Images beside each original.
pause
exit /b 1

:done
pause
exit /b %failed%
