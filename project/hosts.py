from django_hosts import patterns, host

host_patterns = patterns('',
                         host(r'bordado', 'joycebordados.urls', name='bordado'),
                         host(r'adm', 'empresa.urls', name='adm'),
                         )
