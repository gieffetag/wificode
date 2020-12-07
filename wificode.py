
import wsgian.utils
import bulma


def main(pard):
	pard.setdefault('action', '')
	if pard['action'] in ('', 'start'):
		pard['main_body'] = render_start(pard, {})
		pard['html'] = render_page(pard)
	else:
		pard['html'] = wsgian.utils.dump(pard['action'])
	
	return pard


def render_start(pard, rec):
	rec.setdefault('ssid', '')
	rec.setdefault('ssid_pw', '')
	
	rec['input_ssid'] = bulma.input(pard,
			{'id': 'input_ssid',
			 'name': 'rec[ssid]',
			 'label': 'Nome rete WiFi (SSID)',
			 'value': rec['ssid'],
			 'placeholder': 'WiFiAzzurro',
			})

	rec['input_ssid_pw'] = bulma.input(pard,
			{'id': 'input_ssid_pw',
			 'name': 'rec[ssid_pw]',
			 'label': 'Password',
			 'value': rec['ssid_pw'],
			 'placeholder': 'Juan2021',
			})
	
	h = '''
		<form enctype="multipart/form-data" id="wificodeForm" method="post" action="/">		
		<input type="hidden" name="action" id="action" value="scarica">

		%(input_ssid)s
		%(input_ssid_pw)s
		
		<div class="field is-grouped is-grouped-centered">
  		  <div class="control">
    	    <a class="button is-dark" href="/">Stampa</a>
	      </div>
	  	  <div class="control">
    	    <button class="button is-dark" onclick="document.getElementById('wificodeForm').submit()">Scarica PDF</button>
  		  </div>
	    </div>
	    </form>
		''' % rec
	return h


# ------------------------------------------------------------------- #
def render_page(pard):
	pard.setdefault('javascript', '')
	pard.setdefault('errori', [])
	pard['notification'] = ''
	pard['navbar'] = render_navbar(pard)
	if pard['errori']:
		pard['notification'] = bulma.notification(pard, 
				{'class': 'is-danger',
				 'is-light': 'is-light',
				 'messaggi': pard['errori'],
				})
		pard['javascript'] += bulma.notification_js(pard)
	html = '''
	<!DOCTYPE html>
	<html>
	  <head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>%(TITLE)s</title>
		<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.1/css/bulma.min.css">
		<script defer src="https://use.fontawesome.com/releases/v5.14.0/js/all.js"></script>
	  </head>
	  <body>
	  %(navbar)s
	  <section class="section">
		<div class="container">
		%(notification)s
		%(main_body)s
		</div>
	  </section>
	  </body>
	  %(javascript)s
	</html>
	''' % pard	
	return html


def render_navbar(pard):
	h = '''
	<nav class="navbar has-shadow" role="navigation" aria-label="main navigation">
	<div class="navbar-brand">
  
	<a class="navbar-item" href="%(APPSERVER)s">
	  <span class="icon is-medium mr-2">
	    <i class="fas fa-lg fa-wifi"></i>
	  </span>
	  <span class="title is-4">WiFi QR Code</span>
	</a>
	
	</div>	
	</nav>	
	''' % pard
	return h

