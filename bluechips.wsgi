from paste.deploy import loadapp
import os

os.environ['PYTHON_EGG_CACHE'] = '/var/www/python_cache';

application = loadapp("config:/var/www/MarQtChips/config.ini");
