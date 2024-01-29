from waitress import serve

from cold_fusion_fishing.wsgi import application
from django.conf import settings

serve(application, port=settings.WAITRESS_PORT, host=settings.WAITRESS_HOST)