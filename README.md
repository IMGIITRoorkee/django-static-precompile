django-static-precompile
========================

It provides automatic static files precompilation for django.
Currently it has support only for sass (& compass) and handlebars
as it converts sass files to css and handlebars files to (precompiled) js.


Why this?
---------

There are already many support for compression and precompilation of static files in django
i.e. django-compresser but they work only if some custom tags are used in django templates.
It causes some overhead in time every time templates are rendered because of cache management
and this issue persists still in production.

There are no such template tags here. If you request for somefile.css in browser and there exists
somefile.sass then it will automatically precompile somefile.sass to somefile.css and serve it.
Here overhead is when static files are requested not when templates are being rendered in django views.
And this overhead is gone completely in production after all static files are already collected using
`manage.py collectstatic` command.

That's it!


Quick Start
-----------

Install it by
<pre>
pip install git+https://github.com/IMGIITRoorkee/django-static-precompile.git#egg=django-static-precompile
</pre>

Add "static-precompile" to your INSTALLED_APPS setting like this::
```python
INSTALLED_APPS = (
    ...
    'static-precompile',
)
```


Settings
--------


1) By default it uses `STATIC_ROOT` as CACHE_ROOT if it is defined in settings
otherwise `PROJECT_ROOT` or `BASE_DIR` should be defined in settings.
if none is the case or you want cusom path for CACHE_ROOT then define
STATIC_PRECOMPILE_CACHE_ROOT in settings.py

`STATIC_PRECOMPILE_CACHE_ROOT = ...`

You can configure other settings too i.e.

2) Extension for sass files. (Optioanl)

`STATIC_PRECOMPILE_SASS_EXTENSION = ...` By default it's `'sass'`.

3) Using Compass (Yes/No)? (Optioanl)

`STATIC_PRECOMPILE_USE_COMPASS = ...` By default it's `True`.

4) Extension for handlebars files. (Optional)

`STATIC_PRECOMPILE_HANDLEBARS_EXTENSION = ...` By default it's `'hbs'`.

5) To precompile sass files add `'static_precompile.finders.SassFinder'` to `STATICFILES_FINDERS`.
Similarily add `'static_precompile.finders.HandlebarsFinder'` to STATICFILES_FINDERS to precompile
handlebars files.

```python
STATICFILES_FINDERS = (
    ...
    'static_precompile.finders.SassFinder',
    'static_precompile.finders.HandlebarsFinder',
)
```


Usage sass
----------

* To include `.sass` files, write your sass files path with extension `.css` while linking it in html.
It will automatically get compiled and served:

```html
<link rel="stylesheet" href="{{ STATIC_URL }}sass/../style.css" type="text/css" />
```


Usage handlebars
----------------

* Create your handlebar templates in `static/handlebars/<app_name>/` directory 
like `static/handlebars/<app_name>/abc.hbs` and `static/handlebars/<app_name>/xyz.hbs`.

* To import these templates client side just add `static/handlebars/<app_name>/templates.js`
to your javascript import list. `templates.js` is automatically created and cached by pre-compilation
of all `.hbs` files present in that folder.

* You can use individual templates in javascript by `Handlebars.<app_name>_templates.abc` and
`Handlebars.<my_app>_templates.xyz`

* To render handlebars templates in javascript,

```javascript
  var context = {
    some_key: some_value,
    ...
  };
  var rendered_html = Handlebar.<app_name>_templates.abc(context);
  // here change <app_name> with name of your app.
```

LICENCE
-------

MIT LICENCE

Copyright (c) 2015 "IMG, IIT Roorkee"















