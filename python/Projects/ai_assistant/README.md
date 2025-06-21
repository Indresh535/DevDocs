# Personal AI assistant web app using Django

pip install django openai sentence-transformers chromadb



requiernt insalion python version 3.12.4

python -m venv venv

venv\Scripts\activate 

pip install -r requirements.txt

python manage.py startapp ai_assistant

Apply Migrations and Start Server

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

deactivate 