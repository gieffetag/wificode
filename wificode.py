
import wsgian.utils
import bulma
import build_pdf
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64
from PIL import Image


def main(pard):
	pard.setdefault('action', '')
	if pard['action'] in ('', 'start'):
		pard['main_body'] = render_start(pard, {})
		pard['html'] = render_page(pard)
	elif pard['action'] in ('stampa', 'pdf'):
		if pard['action'] == 'pdf':
			rec = {'ssid': pard['ssid'], 'ssid_pw': pard['ssid_pw']}
		else:
			rec = wsgian.utils.cgi_params(pard, 'rec')
		pard['main_body'] = render_preview(pard, rec)
		pard['html'] = render_page(pard)
	elif pard['action'] == 'scarica':
		rec = wsgian.utils.cgi_params(pard, 'rec')
		pdf = build_pdf.build_pdf(pard, rec)
		pard['header'] = [
			('Content-type', 'application/pdf'),
			('Content-Disposition', 'attachment;filename="wifiqrcode.pdf"')]
		pard['html'] = pdf
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
			 'placeholder': 'SenJan2021',
			})
	
	h = '''
		<form enctype="multipart/form-data" spellcheck="false" id="wificodeForm" method="post" action="/">		
		<input type="hidden" name="action" id="action" value="stampa">

		%(input_ssid)s
		%(input_ssid_pw)s
		
		<div class="field is-grouped is-grouped-centered">
	  	  <div class="control">
    	    <button class="button is-dark" onclick="submit_form('stampa')">Stampa</button>
  		  </div>
  		  <div class="control">
    	    <button class="button is-dark" onclick="submit_form('scarica')">Scarica</button>
  		  </div>

	    </div>
	    </form>
	    <script>
	    	function submit_form(action) {
	    		var theAction = document.getElementById('action');
	    		var theForm = document.getElementById('wificodeForm');
	    		theAction.value = action;
	    		theForm.submit();
	    		}
	    </script>
		''' % rec
	return h

#   		  <div class="control">
#     	    <a class="button is-dark" href="/">Stampa</a>
# 	      </div>


def render_preview(pard, rec):
	pard['no_navbar'] = True
	if pard['action'] == 'stampa':
		pard['javascript'] = '<script>window.print();</script>'
	rec['qrcode'] = render_qrcode(pard, rec)
	buf = base64.encodestring(rec['qrcode'])
	h = []
	h.append('<div class="columns">')
	h.append('<div class="column"></div>')
	h.append('<div class="column is-half">')
	h.append('<div class="card">')
	h.append('<header class="card-header">')
	h.append('<p class="card-header-title title is-centered">WiFi</p>')
	h.append('</header>')
	h.append('<div class="card-content">')
	
	rec['img_src'] = 'data:image/jpeg;base64,' + buf
	rec['img_class'] = 'is-square'
	h.append('<figure class="image qrcode">' % rec)
	h.append('  <img src="%(img_src)s">' % rec)
	h.append('</figure>')
	
	h.append('<div class="content has-text-centered">')
	h.append('<p>')
	h.append('Per connetterti con il telefono o il tablet, scansiona con la fotocamera il QR code.<br>')
	h.append('Per gli altri dispositivi, utilizza le credenziali specificate in seguito.')
	h.append('</p>')
	h.append('<br><br>')
	h.append('<p class="mb-0">NETWORK</p>')
	h.append('<p class="title has-text-weight-medium">%(ssid)s</p>' % rec)
	h.append('<p class="mb-0">PASSWORD</p>')
	h.append('<p class="title has-text-weight-medium">%(ssid_pw)s</p>' % rec)
	h.append('</div>')
	
	h.append('<div class="content has-text-centered is-small pt-5">')
	h.append('<p>Crea il QR Code per il tuo WiFi: <strong>wifiqrcode.com</strong></p>')
	h.append('</div>')
	
	
	h.append('</div>') # card-content
	h.append('</div>') # card
	h.append('</div>') # column is-half
	h.append('<div class="column"></div>')
	h.append('</div>') # columns
	return '\n'.join(h)


def render_svg_qrcode(pard, rec):
	factory = qrcode.image.svg.SvgPathImage
	rec['qr_string'] = 'WIFI:T:WPA;S:%(ssid)s;P:%(ssid_pw)s;;' % rec
	img = qrcode.make(rec['qr_string'], image_factory=factory)
	out = BytesIO()
	img.save(out)
	out.seek(0)
	buf = out.read()
	out.close()
	return buf


def render_qrcode(pard, rec):
	rec['qr_string'] = 'WIFI:T:WPA;S:%(ssid)s;P:%(ssid_pw)s;;' % rec
	img = qrcode.make(rec['qr_string'])
	img.thumbnail((256, 256), Image.ANTIALIAS)
	out = BytesIO()
	img.save(out, 'jpeg')
	out.seek(0)
	buf = out.read()
	out.close()
	return buf



	
# ------------------------------------------------------------------- #
def render_page(pard):
	pard.setdefault('javascript', '')
	pard.setdefault('errori', [])
	pard['notification'] = ''
	if 'no_navbar' in pard:
		pard['navbar'] = ''
	else:
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
		<link rel="icon" type="image/png" href="%(APPSERVER)s/static/favicon.png">
		<style>
			.qrcode {
				width: 256px;
				height: 256px;
				margin-left: auto;
				margin-right: auto;
				}
		</style>
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



# def build_pdf(pard, rec):
# 	import pdfkit
# 	rec['APPSERVER'] = pard['APPSERVER']
# 	pdf = pdfkit.from_url('%(APPSERVER)s/pdf/%(ssid)s/%(ssid_pw)s' % rec, False, options={'quiet': ''})
# 	return pdf

