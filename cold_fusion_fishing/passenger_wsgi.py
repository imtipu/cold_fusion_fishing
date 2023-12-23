import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'cold_fusion_fishing.settings'

application = get_wsgi_application()
