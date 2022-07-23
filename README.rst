=====
ML INSTAGRAM
=====

Quick start
-----------

1. Add "ml_instagram" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'ml_instagram',
    ]

2. Add the eviroments in ``settings.py`` ::

   ML_INSTAGRAM_CLIENT_ID = os.environ["ML_INSTAGRAM_CLIENT_ID"]
   ML_INSTAGRAM_CLIENT_SECRET = os.environ["ML_INSTAGRAM_CLIENT_SECRET"]
   ML_INSTAGRAM_REDIRECT_URI = os.environ["ML_INSTAGRAM_REDIRECT_URI"]


3. Run ``python manage.py migrate`` to create the instagram models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to set the instagram configs