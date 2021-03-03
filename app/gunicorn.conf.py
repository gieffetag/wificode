import json
import multiprocessing
import os
import wsgian

wsgian.utils.dot_env()

# Server socket
port = os.getenv("HTTP_PORT", "8091")
bind = '0.0.0.0:{port}'.format(port=port)

# Workers
cores = multiprocessing.cpu_count()
if os.getenv("ENV", "svil") == 'prod':
	workers = 2 * cores
else:
	workers = 2
keepalive = 60

# Logging
errorlog = "-"
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s (%({x-forwarded-for}i)s) %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(L)s'

conf_data = {
	'bind': bind,
	'workers': workers,
	'keepalive': keepalive,
	'errorlog': errorlog,
	'loglevel': loglevel,
	'accesslog': accesslog,
	'access_log_format': access_log_format,
}
print(json.dumps(conf_data, indent=4))