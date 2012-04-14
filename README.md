#Designbin

Often, while creating User interface for your website, you would have to share
it with your colleagues and get feedback before you push it to your repository.
This project allows you to do that! Share your temporary html/css/js/png/jpg/gif
files with colleagues and get get their feedback.

The project has been hosted in http://designb.in

Hope this project will be of use to freelancers who work in geographically distributed
fashion and for open source projects!

**Deploying the project**

* Download the project.
* Install bottle.py, apache
* Change relevant (mostly the SITE_ROOT and TOP_LEVEL_DOMAIN) configurations in config.py.
* Create an app.wsgi file with following code
    
        import os, sys, bottle
        sys.path = ['/path/to/designbin/folder/'] + sys.path
        os.chdir(os.path.dirname(__file__))

        import designbin
        application = bottle.default_app()
    
* Add the following to your apache configuration file.

        <VirtualHost *:80>
            ServerName example.com
            ServerAlias *.example.com

            WSGIDaemonProcess designbin user=www-data group=www-data processes=1 threads=5
            WSGIScriptAlias / /path/to/designbin/folder/app.wsgi

            <Directory /path/to/designbin/folder>
            WSGIProcessGroup designbin
                WSGIApplicationGroup %{GLOBAL}
                Order deny,allow
                Allow from all
            </Directory>
        </VirtualHost>
