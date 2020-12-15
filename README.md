## Semanticflix by Panda-Chan

A Netflix Movies and TV Shows database using RDF.
Semantic Web - Faculty of Computer Science, University of Indonesia.

Application: https://semanticflix.herokuapp.com/
Dataset: https://www.kaggle.com/shivamb/netflix-shows

Members:
1. Annida Safira Arief - 1706040050
2. Bunga Amalia Kurniawati - 1706022104
3. Pande Ketut Cahya Nugraha - 1706028663

For development:
1. Create new virtual environment using `python -m venv env`
2. Activate the virtual environment. For Windows user using `source env/Scripts/activate`. For Mac/Linux user using `source env/bin/activate`.
3. Install requirements using `python -m pip install -r requirements.txt`
4. Applied migrations using `python manage.py migrate`
5. Convert SCSS to CSS using `python manage.py sass static/scss/ static/css/`
6. Collect static `python manage.py collectstatic --no-input`
7. Run application using `python manage.py runserver`
