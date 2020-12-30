
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
	elif pard['action'] == 'stampa':
		rec = wsgian.utils.cgi_params(pard, 'rec')
		pard['main_body'] = render_preview(pard, rec)
		pard['html'] = render_page(pard)
	elif pard['action'] == 'refresh_preview':
		rec = wsgian.utils.cgi_params(pard, 'rec')
		pard['html'] = render_preview(pard, rec)
	elif pard['action'] in ('scarica', 'pdf'):
		if pard['action'] == 'pdf':
			rec = {'ssid': pard['ssid'], 'ssid_pw': pard['ssid_pw']}
		else:
			rec = wsgian.utils.cgi_params(pard, 'rec')
		pdf = build_pdf.build_pdf(pard, rec)
		pard['header'] = [
			('Content-type', 'application/pdf'),
			('Content-Disposition', 'attachment;filename="wificode.pdf"')]
		pard['html'] = pdf
	else:
		pard['html'] = wsgian.utils.dump(pard['action'])
	
	return pard


def render_start(pard, rec):
	tile = {}
	tile['form'] = render_form(pard, rec)
	tile['preview'] = render_preview(pard, rec)
	tile['info'] = render_info(pard)
	h = '''
		<div class="tile is-ancestor">
		  <div class="tile is-6 is-vertical is-parent">
			<div class="tile is-child box">
			  <p class="title is-4 has-text-centered">Crea il tuo WiFi Code</p>
			  <p class="subtitle has-text-centered pb-4">Inserisci le credenziali</p>
			  %(form)s
			</div>
			<div class="tile is-child box">
			  %(info)s
			</div>
		  </div>
		  <div class="tile is-parent">
			<div class="tile is-child box has-background-black">
			  <p class="title pb-4 has-text-white has-text-centered">Anteprima</p>
			  <div id="div_preview">%(preview)s</div>
			</div>
		  </div>
		</div>
		''' % tile
	return h


def render_info(pard):
	h = '''
		<p class="title has-text-centered">Che cos'&egrave;?</p>
		<div class="block">
		<p>
		  La maggior parte dei telefoni e dei tablet permettono di configurare
		  in automatico la rete <i>wi-fi</i> tramite la scansione di un QR Code
		  opportunamente costruito.
		</p>
		<p>
		  Dentro al codice ci sono le
		  istruzioni che permettono al telefono di configurare la rete, <b>senza
		  bisogno di doverla ricercare e senza dover digitare una lunga password.</b>
		</p>
		</div>
		
		<div class="block">
		  Questa applicazione permette di creare velocemente un foglio
		  stampabile con le credenziali del vostro wi-fi.
		</div>
		
		<div class="block">
		<p class="is-size-5"><b>&Egrave; Sicuro?</b></p>
		<p>
		  Certo! Le credenziali vengono trasmesse in modo sicuro e
		  nessun dato viene registrato, conservato o esposto.
		</p>
		</div>
		
		<div class="block">
		<p class="is-size-5"><b>Sei un web developer?</b></p>
		<p>
		  Vuoi far scaricare il PDF direttamente dal sito o dalla app?
		</p>
		<p>
		  &Egrave; semplicissimo, usa questo link:
		  <span class="tag is-info">https://wificode.com/pdf/codice_ssid/password</span>
		</p>
		<p>Ma non metterlo direttamente sul sito o esporrai le credenziali
		della rete wi-fi.</p>
		</div>
		<div class="block">
		<p class="is-size-5"><b>Chi siamo?</b></p>
		<p><i>WiFi Code</i> &egrave; stato scritto da
		 <a href="http://www.inputidea.it/we.html">InputIdea</a>.
		 Forniamo soluzioni e servizi per il web, il commercio
		 elettronico e i market place.
		</p>
		</div>
		'''
	return h

def render_form(pard, rec):
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
		
		<div class="field is-grouped is-grouped-centered pt-5">
	  	  <div class="control">
    	    <button class="button is-dark" onclick="submit_form('stampa')">Stampa</button>
  		  </div>
  		  <div class="control">
    	    <button class="button is-dark" onclick="submit_form('scarica')">Scarica PDF</button>
  		  </div>

	    </div>
	    </form>
	    <script src="/static/wificode.js"></script>
	    <script>
	    const submit_form = function (action) {
	    	event.preventDefault();
	    	var ssid = document.querySelector("#input_ssid input");
			var ssid_pw = document.querySelector("#input_ssid_pw input");
			if (ssid.value == '') {
				ssid.classList.add("is-danger");
				ssid.focus();
				return false;
			}
			else {
				ssid.classList.remove("is-danger");
			};
			if (ssid_pw.value == '') {
				ssid_pw.classList.add("is-danger");
				ssid_pw.focus();
				return false;
			};
			var theAction = document.getElementById('action');
			var theForm = document.getElementById('wificodeForm');
			theAction.value = action;
			theForm.submit();
		};
	    </script>
		''' % rec
	return h


def render_preview(pard, rec):
	if pard['action'] == 'stampa':
		pard['no_navbar'] = True
		pard['javascript'] = '''
			<script>
			document.addEventListener('DOMContentLoaded', function() {
   				setTimeout(function(){
 					window.print();
				}, 500);
			}, false);
			</script>
			'''
	if not rec['ssid']:
		rec['ssid'] = 'WiFiAzzurro'
	if not rec['ssid_pw']:
		rec['ssid_pw'] = 'SenJan2021'
	rec['qrcode'] = render_qrcode(pard, rec)
	buf = base64.encodestring(rec['qrcode'])
	h = []
	h.append('<div class="columns">')
	h.append('<div class="column"></div>')
	h.append('<div class="column">')
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
	h.append('Per connetterti con il telefono o il tablet, scansiona il QR code con la fotocamera.<br>')
	h.append('Per gli altri dispositivi, utilizza le credenziali specificate in seguito.')
	h.append('</p>')
	h.append('<br><br>')
	h.append('<p class="mb-0">NETWORK</p>')
	h.append('<p class="title has-text-weight-medium">%(ssid)s</p>' % rec)
	h.append('<p class="mb-0">PASSWORD</p>')
	h.append('<p class="title has-text-weight-medium">%(ssid_pw)s</p>' % rec)
	h.append('</div>')
	
	h.append('<div class="content has-text-centered is-small pt-5">')
	h.append('<p>Crea il QR Code per il tuo WiFi: <strong>wificode.com</strong></p>')
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
	  %(javascript)s
	  </body>
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
	  <span class="title is-4">WiFi Code</span>
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

