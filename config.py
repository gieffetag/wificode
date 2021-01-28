import pprint
import os
import wsgian

def config(pard):
	default_config = {
		'HTTP_PROTOCOL': 'http',
		'HTTP_ADDRESS': 'localhost',
		'HTTP_PORT': '80',
		'db.mysql': {},
		'SMTP_HOST': '',
		'SMTP_PORT': '',
		'SMTP_USER': '',
		'SMTP_PASSW': '',
		'DEFAULT_SENDER': '',
		'TEMPLATE_RELOAD': False,
		'with_static': True,
		'with_ws': False,
		'ws_auth': False,
		'ws_version': 2,
		'cookie_secret': 'notapplicable',
		'DEBUG': False,
		'LOGLEVEL': 'debug',
		'GOOGLE': {},
		'EMAIL': {},
		}
	wsgian.utils.dot_env()
	for k in default_config:
		pard[k] = os.environ.get(k, default_config[k])
	
	pard['APPLICATION_NAME'] = 'WiFiCode'
	
	pard['APP_URL'] = os.environ.get('APP_URL')
	
	if pard['APP_URL']:
		pard['APPSERVER'] = pard['APP_URL']
	else:
		_HTTP_PORT = ':' + str(pard['HTTP_PORT']) if pard['HTTP_PORT'] != 80 else ''
		pard['APPSERVER'] = '%(HTTP_PROTOCOL)s://%(HTTP_ADDRESS)s' % pard + _HTTP_PORT
	
	pard['PROJECT'] = 'wificode'
	pard['PROJECT_SUBTITLE'] = 'Generatore di QRCode per la configurazione automatica della rete wi-fi'
	pard['PROJECT_TITLE'] = 'WiFiCode'
	pard['TITLE'] = 'WiFi QR Code'
	
	return pard


if __name__ == '__main__':
	import pprint
	pard = config({})
	pprint.pprint(pard)