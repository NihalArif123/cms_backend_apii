# cms-backend-api


# install python
pip install python

# create virtual env
python -m venv myvenv

 # run virtual env
myvenv\Scripts\activate

# install requirements
pip install -r requirements.txt

# To run project
python manage.py makemigrations

python manage.py migrate

python manage.py runserver
