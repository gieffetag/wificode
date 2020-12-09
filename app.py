import config
import sys
import wsgian

urls = [		
	{'pattern': '/',  'module': 'wificode'},
	{'pattern': '/pdf/{ssid}/{ssid_pw}', 'module': 'wificode', 'action': 'pdf'},
]

try:
	config = config.config({})
except ImportError:
	print 'config not found: run "python config.py" then edit site_config.py'
	sys.exit(1)

app = wsgian.App(urls, config)

if __name__ == '__main__':
	wsgian.quickstart(app, config['HTTP_ADDRESS'], config['HTTP_PORT'])

