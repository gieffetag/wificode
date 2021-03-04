import json
import os
import wsgian

wsgian.utils.dot_env()

# Server socket
port = os.getenv("HTTP_PORT", "8091")
bind = '0.0.0.0:{port}'.format(port=port)

# Workers
workers = 2
keepalive = 60
worker_class = 'gthread'
threads = 4

if os.path.isdir("/dev/shm"):
	worker_tmp_dir = '/dev/shm'
else:
	worker_tmp_dir = None

# Logging
errorlog = "-"
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s (%({x-forwarded-for}i)s) %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(L)s'

conf_data = {
	'bind': bind,
	'workers': workers,
	'keepalive': keepalive,
	'threads': threads,
	'worker_class': worker_class,
	'errorlog': errorlog,
	'loglevel': loglevel,
	'accesslog': accesslog,
	'access_log_format': access_log_format,
	'worker_tmp_dir': worker_tmp_dir,
}
print(json.dumps(conf_data, indent=4))