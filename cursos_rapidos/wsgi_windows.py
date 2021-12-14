activate_this = 'C:/Users/Felipe/Envs/cursos_rapidos/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/Users/Felipe/Envs/cursos_rapidos/Lib/site-packages')




# Add the app's directory to the PYTHONPATH
sys.path.append('C:/Users/Felipe/cursos_rapidos')
sys.path.append('C:/Users/Felipe/cursos_rapidos/cursos_rapidos')

os.environ['DJANGO_SETTINGS_MODULE'] = 'cursos_rapidos.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cursos_rapidos.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()