Flask-Compass
#############

Flask-Compass provides a simple integration of Compass_ into Flask applications
especially to help during the development process.

The extension scans the project's directory for Compass configuration files
in order to compile the associated Compass project.


Quickstart
==========

First of all you should probably place your compass project somewhere into the
static folder of your application. Let's assume for this example that your
config.rb is in /home/user/projects/app/static/.

After installing the extension simply add it to your application as usual::
    
    from flask import Flask
    from flaskext.compass import Compass

    app = Flask(__name__)
    compass = Compass(app)

When you now start your application, it will scan who whole project directory
for config.rb files, so it will find yours right in the static folder. Each
found config file will trigger the extension to invoke the compass compiler
to convert your sass or scss files into css.

Note that by default this compilation is only done when the extension is
initialized when in production. If your application is in debug-mode, the
whole process will be done with each request.

This behaviour as well as where the extension looks for your config files can
be configured as detailed in the next chapter.

.. _compass: http://compass-style.org/

.. toctree::
    :hidden:
    
    config

