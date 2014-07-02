Django User App
============
A simple, reusable Django application that 
provides basic user functionality for a web app.

Installation
------------
Clone the repository, and place the 'user' folder 
into your project alongside other applications. In 
a typical Django setup, this is usually in the 
same directory as the manage.py file.

Open your project's urls.py file. This may be 
in the project root as well, or it may be in the same 
folder as the settings.py file (typically a subdirectory 
of your project that has the same name as your project).

In your project's urls.py file, add an import for 'user'. 
Then add the following URL patterns to route URLs to the 
application urls.py file. 

It is recommended that you use the patterns as they are listed 
here as that is the test configuration for the app. If you 
choose to use a different setup, your mileage may vary. 
Changing the accounts/login url requires some Django 
settings changes.

	url(r'^user/', include('user.urls')),
	url(r'^accounts/login/$', 'user.views.login_user')

You then need to add the application to the "INSTALLED_APPS" 
array in your project's settings.py file. Following 
that, you should be good to go. You will need to run 
the initial syncdb for Django if you haven't, but 
otherwise this application does not have any additional 
models.

For more information see the about page, which is linked 
in the footer of the user pages, and can be found in 
the templates folder with the filename "user_aboutapp.html"

License
---------
Included software is distributed under the BSD license. 
See LICENSE for full license text.  

Though not required by the license terms, please consider contributing, 
providing feedback, or simply dropping a line to say that this software 
was useful to you. Pull requests are always welcome.
