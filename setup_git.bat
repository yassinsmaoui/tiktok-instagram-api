@echo off
echo Initialisation du depot Git...

git init
git add .
git commit -m "Initial commit: TikTok to Instagram automation API"
git branch -M main
git remote add origin https://github.com/yassinsmaoui/tiktok-instagram-api.git
git push -u origin main

echo.
echo Depot cree avec succes!
echo URL: https://github.com/yassinsmaoui/tiktok-instagram-api
pause
