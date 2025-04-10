# 🎁 Family GiftsList

A simple web application created for the purpose of collecting information in the family about 
what each person would like to receive as a gift for a birthday, holiday, etc. Often, during the year, 
different ideas come up about what they might want to receive, and then when it comes down to it, 
they don't remember what it is.
This application allows you to:

- create (on users invitation) a user account and register the gifts you would like to receive,
- checking the wishes of other family members when you want to buy them a gift (this does not require an account, 
only the name, surname and date of birth)
- logged-in users can reserve a gift they want to buy for someone

---

## 🛠 Technologies

- Python 3.10.12
- Django 5.2
- PostgreSQL (Docker)

---

## 🚀 How to run locally

1. clone repository
```bash
git clone 
```
2. create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. install requirements.txt
```bash
pip3 install -r requirements.txt
```

4. run Docker container (docker-compose up)
```bash
docker-compise up -d
```

5. create local_settings.py file and add database configuration:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5433',
    }
}
```

6. run server: 
```bash
python3 manage.py runserver
```
