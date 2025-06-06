# C:\scripts\deploy.ps1
cd C:\www\myapp
git pull origin main

cd api
npm install
pm2 start index.js --name api -f

cd ../web
npm install
npm run build
pm2 start "npm run start" --name web -f
