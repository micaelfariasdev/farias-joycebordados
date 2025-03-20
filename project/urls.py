

from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'bordado', 'project.bordado_urls', name='bordado'),
    host(r'adm', 'project.adm_urls', name='adm'),
)

urlpatterns = [
]
