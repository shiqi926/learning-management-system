# is212-t7

## Reference demo
https://www.digitcoalocean.m/community/tutorials/how-to-build-a-modern-web-application-to-manage-customer-information-with-django-and-react-on-ubuntu-18-04
Careful, they may have a different file structure from us
## Windows Set up

1. `cd` to project directory (where the requirements.txt file is located)
2. `python3 -m venv ./env`
3. `env\Scripts\activate`
4. `pip install -r requirements.txt`
5. Confirm correct DATABASE config in settings.py (password = "")

## Mac Setup

1. `cd` to project directory (where requirements.txt file is located)
2. Run `python3 -m venv venv` to create a virtual environment (named venv)
3. Run `source venv/bin/activate` to activate virtual environment
4. Run `pip install -r requirements.txt` to install all dependencies in the virtual environment
5. Confirm correct DATABASE config in settings.py ("root" for mac)

## Combined Set Up (cont'd from above)

1. `cd spmg7` (where manage.py is located)
2. `python manage.py migrate`
3. `python manage.py runserver`

## Create model

1. create a new .py file in `spmg7/api/models` folder
2. name it <model_name>.py eg. course.py
3. in models/__ init __.py file add import statement eg. "from .course import Course"
4. `cd` to the `spmg7` folder (containing `manage.py`)
5. `python manage.py makemigrations`
6. `python manage.py migrate`

### Populate model with sample data

1. `python manage.py makemigrations --empty --name <model_name> api
2. find the created file in `api/migrations` folder
3. write code to create new data (check out reference demo for example)
4. `python manage.py migrate`

### Add model to serializers.py

1. Go to serializers.py in api folder
2. Import class eg. `from .models.course import Course`
3. Write serialzer (checkout reference demo for more details)

### Add model to admin.py

1. Go to admin.py in api folder
2. Import class eg `from .models.course import Course`
3. Register class eg. `admin.site.register(Course)`

### Writing and running tests
1. cd to first folder spmg7
2. create test file in tests folder, name it according to what you are testing (eg if im testing quiz views, name as quiz.py)
3. remember to register the tests in the tests folder's __init__.py
4. once done writing tests, run the tests using cli `python manage.py test`