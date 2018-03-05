@echo off
title This is a thing
echo Welcome Here
set /p var =< dat.txt
if var==0 (
pip install requests
pip install spotipy
pip install youtube_dl
pip install eyeD3
pip install subprocess
echo "1" > dat.txt
)
python fiifi.py
pause