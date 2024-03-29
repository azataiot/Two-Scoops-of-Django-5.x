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

## 6. Model best practices

```python
# core/models.py
from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created' and 'updated' fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # prevent django from creating a table for this model.
        abstract = True
```

```python
# flavors/models.py
from django.db import models

# Create your models here.

from core.models import TimeStampedModel


class Flavor(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title
```

![CleanShot 2024-03-11 at 14.49.42](https://raw.githubusercontent.com/azataiot/images/master/2024/03/upgit_20240311_1710157789.png)

recommended 3rd parties: 

- `django-model-utils`
- `django-extensions`

Recommendations:

- Avoid using BinaryField
- Try to avoid using generic relations 
- Make choices and sub-choices model constants
- `objects = models.Manager()` should be defined manually above any custom model manager.

## 7. Queries and the Database Layer

- Use `get_object_or_404` for single object

​	Note: there is also `get_list_or_404`

​	**Only use it in views**

- Queries that might throws exceptions (models) 

  - `execpt Flavor.DoseNotExist`
  - `except ObjectDoseNotExist`

- Use lazy evaluation to make queries legible 

- Chaining queries for legibility

  ```python
  # promos/views.py
  from .models import Promo
  from django.db.models import Q
  
  
  def fun_function(name=None):
      """Find working ice cream promo"""
      qs = (
          Promo
          .objects
          .active()
          .filter(
              Q(name__startswith=name) |
              Q(description__icontains=name)
          )
          .exclude(status='melted')
          .select_related('flavors')
      )
      return qs
  ```

- Instead of managing data with Python, always try to use Django’s advanced query tools

- Use Database Functions   https://docs.djangoproject.com/en/5.0/ref/models/database-functions/ 

- Don’t drop down to raw SQL until it’s necessary 

- Add indexes as needed 

  - start with no index 
  - add if used frequently, as in 10-25% of all queries. 

- Use transaction when need **ACID**

  ```python
  ...
    with transaction.atomic():
    # This code executes inside a transaction. 
      flavor.status = status 
      flavor.latest_status_change_success = timezone.now() 
      flavor.save()
    return HttpResponse('Hooray')
  ```

- It’s imposiible to handle transaction errors in `django.http.StreamingHttpResponse`

## 8. Function and Class based views

![CleanShot 2024-03-11 at 17.01.21](https://raw.githubusercontent.com/azataiot/images/master/2024/03/upgit_20240311_1710165690.png)

- Prefer CBVs for most views. 

- Keep view logic out of **URLConf**

  ```python
  # tastings/views.py
  
  from django.views.generic import ListView, DetailView, UpdateView
  from .models import Tasting
  from django.urls import reverse
  
  
  class TasteListView(ListView):
      model = Tasting
  
  
  class TasteDetailView(DetailView):
      model = Tasting
  
  
  class TasteResultsView(ListView):
      template_name = 'tastings/results.html'
  
  
  class TasteUpdateView(UpdateView):
      model = Tasting
  
      def get_success_url(self):
          return reverse('tastings:detail',
                         kwargs={
                             'pk': self.object.pk,
                         })
  ```
  
  ```python
  # tastings/urls.py
  from django.urls import path
  from . import views
  
  urlpatterns = [
      path(
          route='',
          view=views.TasteListView.as_view(),
          name='list'
      ),
      path(
          route='<int:pk>/',
          view=views.TasteDetailView.as_view(),
          name='detail'
      ),
      path(
          route='<int:pk>/results/',
          view=views.TasteResultsView.as_view(),
          name='results'
      ),
      path(
          route='<int:pk>/update/',
          view=views.TasteUpdateView.as_view(),
          name='update'
      ),
  ]
  ```
  
- Makes for Shorter, More Intuitive, and Don’t Repeat Yourself URL Names

## 9. Best practices for function based views

## 10. Best Practices for class based views

```python
# Example 10.1: Using Mixins in a View

class FreshFruitMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_fresh_fruit"] = True
        return context


class FruityFlavorView(FreshFruitMixin, TemplateView):
    template_name = "fruity_flavor.html"
```

- Mixin must always go on the far left side.
- The base view class must always go on the far right side.
- Performing Custom Actions on Views With Valid Forms `def form_valid(self, form):`
- Performing Custom Actions on Views With Invalid Forms `def form_invalid(self, form):` 

```html
{% if messages %}
<ul class="messages">
   {% for message in messages %}
   <li id="message_{{ forloop.counter }}"
   {% if message.tags %} class="{{ message.tags }}" {% endif %}>
   {{ message }}
   </li>
   {% endfor %} 
</ul>
{% endif %}
```

## 11. Asynchronous views

