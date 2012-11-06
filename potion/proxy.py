import urllib2
from potion.common import cfg

if cfg.has_section('proxy') and cfg.has_option('proxy','proxy_type') and cfg.has_option('proxy','proxy_address'):

    proxy_type = cfg.get('proxy', 'proxy_type')
    proxy_address = cfg.get('proxy', 'proxy_address')

    import socks
    (proxy_host,proxy_port)=proxy_address.split(':')

    try:
        proxy_port=int(proxy_port)
    except ValueError:
        proxy_port=None
        print '[EE]proxy port must be int!'

    if not proxy_host or not proxy_port:
        #maybe mispelled config, exiting with code 'incorrect usage'
        print '[EE]Error in proxy address configuration(current value: %s)!' % proxy_address
        import sys
        sys.exit(2)

    socks.setdefaultproxy(eval('socks.PROXY_TYPE_'+proxy_type), proxy_host, int(proxy_port))
    socks.wrapmodule(urllib2)
