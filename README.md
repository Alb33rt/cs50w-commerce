# cs50w-commerce
This is a commerce-based web application from the web course CS50W from Harvard. This is my version of the code that is open to my friends for use, and I have written all the code by myself.

The application has several features, which will be outlined below the instructions for bootup.



#### Installing basic packages 
Make sure that ``pip`` -- the Python package installer is up-to-date before you install anything.

+ The commerce-application is run on Django, you can install Django by running ``pip install django==3.1.0`` inside the terminal.
+ Image storage is run on Pillow version 8.1.0 , install using ``pip install Pillow==8.1.0``.



## Starting the application
You can start the application by running ``python manage.py runserver`` after navigating to the main directory, in this case ``cs50w-commerce``.

The local server host ip address should be ``127.0.0.1:8000``, the link to the admin page should be ``/admin``.


#### Making Migrations

To make migrations for the web application, run
``python manage.py makemigrations auctions``

then, 
``python manage.py migrate``

The server should update the database for you according to the changes you have made.
