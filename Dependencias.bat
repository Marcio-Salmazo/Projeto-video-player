@echo off
echo Instalando bibliotecas Python necessarias...
python -m pip install --upgrade pip
python -m pip install opencv-python PyQt5 numpy python-vlc
echo.
echo Instalacao concluida!
pause