===========
locallinks
===========

A tool for mapping community-produced research about the things people value where they live. 
Built with Django, Leaflet.js and Twitter Bootstrap.

Requirements
============

* Python 2.7+
* Django 1.5.4
* Pillow 2.4.0 https://pypi.python.org/pypi/Pillow
* Whoosh 2.5.7 https://pypi.python.org/pypi/Whoosh/
* Haystack 2.0.0 http://haystacksearch.org/
* django.tinymce https://github.com/aljosa/django-tinymce
* django-image-cropping https://github.com/jonasundderwolf/django-image-cropping
* django-taggit https://github.com/alex/django-taggit

Installation
============

Once you have installed all the dependencies, edit settings.py to reflect your database configuration - the included settings.py defaults to SQLite with a file in the project root called map.db.

Note: the default configuration is set up to run using the built-in Django test webserver. Don't use this in production environments!

Run '''python manage.py syncdb''' from the project root.

Run '''python manage.py runserver 0.0.0.0:8000'''

Log in to the admin site at '''http://your_ip_here:8000/admin/''' using the account details you entered when you ran syncdb.

Add a new 'map' in the 'maps' admin, giving it a title and a latitude and longitude. When you visit '''http://your_ip_here/''', you should now see a leaflet map centered on the coordinates you've given.

Add layers in the admin. These allow you to classify your assets and adds a layer control to the leaflet map.

Once you've finished these steps, you've got the basic configuration in place. You can now add places and pages as you see fit. 

Once you've done this, you should update your search index by running '''python manage.py rebuild_index'''. It'd be worth adding a cron job for this so your search stays up to date automatically as you add new items.

