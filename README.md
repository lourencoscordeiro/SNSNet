SNSNet - Web app developed as a project of a College Course

A facebook-alike web platform that is to be used by health professionals and health institutions (from portugal).

The web application is build in python with the web framework django. 

1. Dependencies:

1.1 Django installation

    run 'pip install django'

1.2 Django-email-verification 

external library that is used to validate email addresses (when creating new accounts) using token-based URLs

    run 'pip install django-email-verification'

1.3 Django-cloudinary-storage 

external library that allows the application to load media files in a cloud servers (by cloudinary) instead of using local resources

    run 'pip install django-cloudinary-storage'

1.4 Pillow 

python binary used by Django-cloudinary-storage to handle media files

    run 'pip install pillow'
    
    
2. Run project:

  run 'python manage.py runserver'

  
