@echo off
echo Ajout des fichiers Streamlit au repository...

git add .
git commit -m "Add Streamlit interface"
git push origin main

echo.
echo Fichiers pousses vers GitHub!
echo Vous pouvez maintenant deployer sur Streamlit Cloud:
echo https://share.streamlit.io/
pause
