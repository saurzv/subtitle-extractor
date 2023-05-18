# Subtitle Extractor

[link](http://ec2-3-7-68-172.ap-south-1.compute.amazonaws.com)

---

### Dependencies

#### Required binaries

(_Must be installed on local machine_)

- ##### ccextractor
  - To extract closed caption
- ##### redis
  - Used as message broker for celery

#### Required pip modules

- ##### boto3
  - To connect with DynamoDB
- ##### celery
  - To offload task in background
- ##### django
- ##### djago-celery-results
  - To store the task results in django database
- ##### django-storages
  - To store files in remote server (_AWS S3 in this case_)
- ##### djangorestframework
  - To make REST API

---

### Run on local machine

Install the required binaries
Clone the repository and install required pip modules

```bash
git clone https://github.com/saurzv/subtitle-extractor.git
cd subtitle-extractor
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Create a .env file with these values :

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
DJANGO_SECRET_KEY
```

Make migratations and run server

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

In another terminal with same virtual enivronment, run celery

```bash
celery -A server worker -l info
```

Visit the site at http://127.0.0.1:8000/

_commands are written with bash shell in mind_

---

### Further scope of improvements

- Uploading large files can lead to the user being stuck on the homepage for a very long time. POST requests can be offloaded to celery in the background, and a waiting page can be shown with a polling API.
- Progress bar for file upload.
- Error pages can be implemented.
- Option to download the extracted _.srt_ file can be implemented.
