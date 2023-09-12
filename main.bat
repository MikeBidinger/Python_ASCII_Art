@echo OFF
set CONDAPATH=C:\Users\MB91448\Anaconda3
set ENVNAME=base
set FILEPATH=main.py

if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)

call %CONDAPATH%\Scripts\activate.bat %ENVPATH%

python %FILEPATH%

call conda deactivate

pause
@REM timeout /t 21600
