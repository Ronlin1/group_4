import os
from django.core.wsgi import get_wsgi_application
from waitress import serve

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Todo.settings')

application = get_wsgi_application()

serve(application, host='0.0.0.0', port=8000)