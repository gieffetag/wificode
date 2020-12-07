import pprint
import os

def config(pard):
	import site_config
	
	for k in [
			'HTTP_PROTOCOL',
			'HTTP_ADDRESS',
			'HTTP_PORT',
			'db.mysql',
			'SMTP_HOST',
			'SMTP_PORT',
			'SMTP_USER',
			'SMTP_PASSW',
			'DEFAULT_SENDER',
			'TEMPLATE_RELOAD',
			'with_static',
			'with_ws',
			'ws_auth',
			'ws_version',
			'cookie_secret',
			'DEBUG',
			'LOGLEVEL',
			'GOOGLE',
			'EMAIL',
			]:
		pard[k] = site_config.config.get(k)
	
	pard['APPLICATION_NAME'] = 'WiFiCode'
	
	_HTTP_PORT = ':' + str(pard['HTTP_PORT']) if pard['HTTP_PORT'] <> 80 else ''
	pard['APPSERVER'] = '%(HTTP_PROTOCOL)s://%(HTTP_ADDRESS)s' % pard + _HTTP_PORT
	
	pard['PROJECT'] = 'wificode'
	pard['PROJECT_SUBTITLE'] = 'Generatore di QRCode per la configurazione automatica della rete wi-fi'
	pard['PROJECT_TITLE'] = 'WiFiCode'
	pard['TITLE'] = 'WiFi QR Code'
	
	return pard

# site_config = {
#  'HTTP_PROTOCOL': 'http',
#  'HTTP_ADDRESS': 'localhost',
#  'HTTP_PORT': 8091,
#  'cookie_secret' : 'notapplicable',
#  'DEBUG': True,
#  'LOGLEVEL': 'debug',
#  'with_static': True,
#  'TEMPLATE_RELOAD': True,
#  'SMTP_HOST': '',
#  'with_ws': True,
#  'ws_auth': False,
#  'ws_version': 2,
#  }