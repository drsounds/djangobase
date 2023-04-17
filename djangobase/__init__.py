from django.conf import settings
from urllib.parse import urlparse


def parse_netloc_to_domain(hostname):
    
    domains = hostname.split('.')

    protocol = ''

    parts = []

    for domain in domains:
        if not domain in ['open', 'com', 'nu', 'se']:
            parts.append(domain)
    
    protocol = '.'.join(parts)
    
    return protocol


def parse_uri(uri):
    if not uri:
        return None
    if uri.startswith('http://') or uri.startswith('https://'):
        url = urlparse(uri)
        protocol = parse_netloc_to_domain(url.netloc)
        
        pathes = url.path.split('/')

        id = pathes[1]

        return dict(
            protocol=protocol,
            type=type,
            id=id,
            query=url.query,
            fragment=url.fragment
        )
    
    uri_parts = uri.split('#', 1)
    uri_parts_2 = uri_parts[0].split('?')

    parts = uri_parts_2[0].split(':')
    type = parts[1]
    slug = parts[2]
    protocol = parts[0]
    sub_type = None
    sub_id = None
    tertiary_type = None
    if len(parts) > 3:
        sub_type = parts[3]
    if len(parts) > 4:
        sub_id = parts[4]
    if len(parts) > 5:
        tertiary_type = parts[5]
    return dict(
        slug=slug,
        id=slug,
        type=type,
        sub_type=sub_type,
        sub_id=sub_id,
        sub_slug=sub_id,
        tertiary_type=tertiary_type,
        protocol=protocol
    )
