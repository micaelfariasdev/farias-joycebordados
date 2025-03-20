from django_hosts import patterns, host

host_patterns = patterns('',
                         host(r'www', 'joycebordados.urls', name='bordado'),
                         host(r'bordado', 'clientes.urls', name='clientes'),
                         host(r'adm', 'empresa.urls', name='adm'),
                         )
