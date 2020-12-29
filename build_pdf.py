

from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph, PageBreak
from reportlab.platypus import Flowable, Image
from reportlab.lib.units import cm
from reportlab.rl_config import defaultPageSize
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

import PIL.Image
import qrcode
from io import BytesIO

class MCLine(Flowable):
	def __init__(self, width, height=0):
		Flowable.__init__(self)
		self.width = width
		self.height = height

	def __repr__(self):
		return "Line(w=%s)" % self.width

	def draw(self):
		"""
		draw the line
		"""
		self.canv.line(0, self.height, self.width, self.height)


def build_pdf(pard, rec):
	
	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(
			name='Center',
			alignment=TA_CENTER,
			fontSize=12,
			#spaceAfter=6,
			leading=18,
			textColor='#6e6e6e',
			))
	styles.add(ParagraphStyle(
			name='Center14',
			parent=styles['Center'],
			fontSize=14,
			))
	styles.add(ParagraphStyle(
			name='Center8',
			parent=styles['Center'],
			fontSize=8,
			))
	
	
	story = []	
	story.append(Paragraph('Wi-Fi', styles['Title']))
	
	line = MCLine(440)
	story.append(line)
	story.append(Spacer(1,12))
	
	## QRCode
	rec['qr_string'] = 'WIFI:T:WPA;S:%(ssid)s;P:%(ssid_pw)s;;' % rec
	img = qrcode.make(rec['qr_string'])
	img.thumbnail((256, 256), PIL.Image.ANTIALIAS)
	out = BytesIO()
	img.save(out, 'jpeg')
	out.seek(0)
	im = Image(out)
	story.append(im)
	
	story.append(Spacer(1,12))
	
	story.append(Paragraph(
		'Per connetterti con il telefono o il tablet, scansiona il <i>QR code</i> con la fotocamera.',
		styles['Center']))
	story.append(Paragraph(
		'Per gli altri dispositivi, utilizza le credenziali specificate in seguito.',
		styles['Center']))
	
	story.append(Spacer(1,12))
	story.append(Paragraph(
		'NETWORK',
		styles['Center']))
	story.append(Paragraph(
		rec['ssid'],
		styles['Title']))

	story.append(Spacer(1,12))
	story.append(Paragraph(
		'PASSWORD',
		styles['Center']))
	story.append(Paragraph(
		rec['ssid_pw'],
		styles['Title']))

	story.append(Spacer(1,90))
	story.append(Paragraph(
		'Crea il QR Code per il tuo WiFi:<b>wifiqrcode.com</b>',
		styles['Center8']))
	
	filename = BytesIO()
	
	doc = SimpleDocTemplate(filename, pagesize=(A4), showBoundary=None)	
	doc.build(story)
	
	filename.seek(0)
	buf = filename.read()
	filename.close()
	out.close()
	
	return buf


if __name__ == '__main__':
	import config
	pard = config.config({})
	buf = build_pdf(pard, {'ssid': 'WiFiAzzurro', 'ssid_pw': 'SenJan2021'})
	open('pippo.pdf', 'wb').write(buf)
	
	



