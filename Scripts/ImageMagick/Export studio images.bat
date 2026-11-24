@echo off
setlocal EnableExtensions DisableDelayedExpansion
rem Drop image files or folders onto this script, or pass paths on the command line.
rem Requires ImageMagick 7 (magick.exe on PATH). No Python required.
rem Makes eight JPG, PNG and WebP variants. Existing export folders are left alone.

if "%~1"=="" goto usage
where magick.exe >nul 2>&1
if errorlevel 1 (
    echo ImageMagick 7 was not found on PATH.
    pause
    exit /b 1
)
set "failed=0"

:next_input
if "%~1"=="" goto done
set "item=%~f1"
if exist "%item%\." goto folder
if not exist "%item%" goto missing
set "destination=%~dp1%~nx1 - Studio Exports"
set "source=%item%"
call :supported
if errorlevel 1 goto unsupported
call :make_destination
if errorlevel 1 goto failed_input
call :export_image
if errorlevel 1 goto failed_input
goto advance

:folder
set "destination=%item%\Studio Exports"
set "found_image="
for %%F in ("%item%\*") do (
    set "source=%%~fF"
    call :export_folder_image
    if errorlevel 1 goto failed_input
)
if not defined found_image goto unsupported
goto advance

:export_folder_image
if exist "%source%\." exit /b 0
call :supported
if errorlevel 1 exit /b 0
if not defined found_image (
    call :make_destination
    if errorlevel 1 exit /b 1
    set "found_image=1"
)
call :export_image
exit /b %errorlevel%

:supported
for %%F in ("%source%") do set "extension=%%~xF"
for %%E in (.jpg .jpeg .png .tif .tiff .psd .webp) do if /i "%extension%"=="%%E" exit /b 0
exit /b 1

:make_destination
if exist "%destination%" (
    echo Export path already exists: "%destination%"
    exit /b 1
)
mkdir "%destination%" || exit /b 1
for %%D in (high-jpg high-png high-webp low-jpg low-png low-webp web-jpg web-png) do (
    mkdir "%destination%\%%D" || exit /b 1
)
exit /b 0

:export_image
for %%F in ("%source%") do set "filename=%%~nxF"
echo Exporting "%filename%"
magick.exe "%source%[0]" -auto-orient ^
    ^( +clone -resize "4600x4600>" -background white -alpha remove -alpha off -write "%destination%\high-jpg\%filename%.jpg" +delete ^) ^
    ^( +clone -resize "4600x4600>" -write "%destination%\high-png\%filename%.png" +delete ^) ^
    ^( +clone -resize "2000x2000>" -quality 100 -write "%destination%\high-webp\%filename%.webp" +delete ^) ^
    ^( +clone -resize "1600x1600>" -background white -alpha remove -alpha off -write "%destination%\low-jpg\%filename%.jpg" +delete ^) ^
    ^( +clone -resize "1600x1600>" -write "%destination%\low-png\%filename%.png" +delete ^) ^
    ^( +clone -resize "800x800>" -quality 100 -write "%destination%\low-webp\%filename%.webp" +delete ^) ^
    ^( +clone -resize "500x500>" -background white -alpha remove -alpha off -gravity Center -extent 500x500 -write "%destination%\web-jpg\%filename%.jpg" +delete ^) ^
    ^( +clone -resize "500x500>" -background none -gravity Center -extent 500x500 -write "%destination%\web-png\%filename%.png" +delete ^) ^
    null:
exit /b %errorlevel%

:missing
echo Input not found: "%item%"
goto failed_input

:unsupported
echo No supported images found in "%item%".
goto failed_input

:failed_input
set "failed=1"

:advance
shift
goto next_input

:usage
echo Drop JPG, PNG, TIFF, PSD or WebP files or folders onto this batch file.
echo Each input gets a new Studio Exports folder. Original images remain in place.
pause
exit /b 1

:done
if "%failed%"=="1" echo Some inputs failed. Check the messages above for incomplete exports.
pause
exit /b %failed%
