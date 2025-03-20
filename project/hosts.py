from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'bordado', 'clientes.urls', name='bordado-client'),
    host(r'bordado2', 'joycebordados.urls', name='bordado'),  # Ajuste para o nome correto
    host(r'adm', 'empresa.urls', name='adm'),
)
