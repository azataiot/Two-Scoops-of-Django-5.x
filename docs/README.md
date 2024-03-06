# Two Scoopes of Django 3.X Book Notes

Book notes, not complete, may refactored?

## 1. Coding style

- Make the code readable
- Avoid using `import *`
- Use `_` in python (URLConf) and `-` in templates.
- JS & CSS style guide:  https://codeguide.co/ 

## 2. Environment setup

- Use **PostgreSQL** everywhere
- Use **pip** and **venv** (virtualenv, virtualenvwrapper)
- requirements files
- **Git** + **Docker**

## 3. Project layout

```python
icecreamratings_project
├── config/
│   ├── settings/
│   ├── __init__.py
│ 	├── asgi.py
│ 	├── urls.py
│   └── wsgi.py
├── docs/
├── icecreamratings/
│   ├── media/  # Development only!
│   ├── products/
│   ├── profiles/
│   ├── ratings/
│ 	├── static/
│   └── templates/
├── .gitignore
├── Makefile
├── README.md
├── manage.py
└── requirements.txt
```

## 4. App design

>  Write programs that do one thing and do it well. 
>
> – [Douglas Mcilroy](https://en.wikipedia.org/wiki/Douglas_McIlroy)

### Common app modules

```python
# Common modules
scoops/
├── __init__.py
├── admin.py
├── forms.py
├── management/
├── migrations/
├── models.py
├── templatetags/
├── tests/
├── urls.py
├── views.py
```

### uncommon app modules

```python
# uncommon modules
 scoops/
 ├── api/  # DRF or Ninja 
 ├── behaviors.py # model mixins
 ├── constants.py # app-level settings
 ├── context_processors.py
 ├── decorators.py
 ├── db/ # custom model fields or components
 ├── exceptions.py
 ├── fields.py # custom form (model) fields
 ├── factories.py # test data factories
 ├── helpers.py # helper functions
 ├── managers.py
 ├── middleware.py
 ├── schema.py # for GraphQL 
 ├── signals.py
 ├── utils.py # synonymous with helpers.py
 ├── viewmixins.py
```

## 5. Settings & requirements files

- All settings, requirements need to be version controlled. ( git-it)
- Keep secrets keys safe
- Seperate configuration from code ( use **Environment variables** )
- Use multiple requirements files
- Use relative path with `Pathlib`

### Using multiple settings file

```python
settings/
 ├── __init__.py
 ├── base.py
 ├── local.py
 ├── staging.py
 ├── test.py
 ├── production.py
```

`settings/local.py`

```python
from .base import *
DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DATABASES = {
   'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'twoscoops',
         'HOST': 'localhost',
	}
}
INSTALLED_APPS += ['debug_toolbar', ]
```

### Handling missing secret key exceptions

`settings/base.py`

```python
# settings/base.py
import os
# Normally you should not import ANYTHING from Django directly 
# into your settings, but ImproperlyConfigured is an exception. 
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
"""Get the environment variable or return exception.""" 
  try:
    return os.environ[var_name] 
  except KeyError:
    error_msg = 'Set the {} environment variable'.format(var_name)
    raise ImproperlyConfigured(error_msg)
```

### Using multiple requirements files

```python
requirements/
   ├── base.txt
   ├── local.txt
   ├── staging.txt
   ├── production.txt
```

## Model best practices

