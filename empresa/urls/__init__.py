from . import carrossel_urls
from . import cliente_urls
from . import dados_urls
from . import dash_urls
from . import global_urls
from . import pedidos_urls

app_name = 'adm'

urlpatterns = carrossel_urls.urlpatterns + cliente_urls.urlpatterns + \
    dados_urls.urlpatterns + dash_urls.urlpatterns + \
    global_urls.urlpatterns + pedidos_urls.urlpatterns
