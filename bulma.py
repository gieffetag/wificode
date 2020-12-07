
__all_rest__ = [
	'input',
	]

class Error(Exception):
	"""Base class for other exceptions"""
	pass


def input(pard, args):
	args.setdefault('field', True) # mettere false se stai ridisegnando il campo via ajax
	args.setdefault('id', '')
	args.setdefault('name', '')
	args.setdefault('label', '')
	args.setdefault('placeholder', '')
	args.setdefault('value', '')
	args.setdefault('control_class', '')
	args.setdefault('input_class', '') # is-danger
	args.setdefault('help_message', '')
	args.setdefault('help_class', '') # is-success
	args.setdefault('icon_left', '') # fa-user
	args.setdefault('icon_right', '') # fa-check
	
	if not args['label']:
		args['label'] = args['name'].replace('_', ' ').title()
	if args['icon_left']:
		args['control_class'] += ' has-icons-left'
	if args['icon_right']:
		args['control_class'] += ' has-icons-right'
	
	h = []
	if args['field']:
		if args['id']:
			h.append('<div id="%(id)s" class="field">' % args)
		else:
			h.append('<div class="field">' % args)
	h.append('<label class="label has-text-centered-touch has-text-weight-normal">%(label)s</label>' % args)
	h.append('<div class="control %(control_class)s">' % args)
	h.append('<input class="input %(input_class)s" name="%(name)s" type="text" placeholder="%(placeholder)s" value="%(value)s">' % args)
	if args['icon_left']:
		h.append('<span class="icon is-small is-left"><i class="fas %(icon_left)s"></i></span>' % args)
	if args['icon_right']:
		h.append('<span class="icon is-small is-right"><i class="fas %(icon_right)s"></i></span>' % args)
	h.append('</div>')
	if args['help_message']:
		h.append('<p class="help %(help_class)s">%(help_message)s</p>' % args)
	if args['field']:
		h.append('</div>')
	
	return '\n'.join(h)


def select(pard, args):
	args.setdefault('field', True) # mettere false se stai ridisegnando il campo via ajax
	args.setdefault('id', '')
	args.setdefault('name', '')
	args.setdefault('label', '')
	args.setdefault('value', '')
	args.setdefault('options', [])
	args.setdefault('selected', '')
	args.setdefault('control_class', '')
	args.setdefault('select_class', '') # is-primary
	args.setdefault('help_message', '')
	args.setdefault('help_class', '') # is-success
	
	h = []
	if args['field']:
		if args['id']:
			h.append('<div id="%(id)s" class="field">' % args)
		else:
			h.append('<div class="field">' % args)
	
	if args['label']:
		h.append('<label class="label">%(label)s</label>' % args)
	
	h.append('<div class="control %(control_class)s">' % args)
	
	h.append('<div class="select %(select_class)s">' % args)
	h.append('<select name="%(name)s">' % args)
	for opt in args['options']:
		if opt[0] == args['selected']:
			h.append('<option value="%s" selected>%s</option>' % opt)
		else:
			h.append('<option value="%s">%s</option>' % opt)
	h.append('</select>')
	h.append('</div>') # select
	
	h.append('</div>') # control
	
	if args['help_message']:
		h.append('<p class="help %(help_class)s">%(help_message)s</p>' % args)
	if args['field']:
		h.append('</div>') # field
	
	return '\n'.join(h)


def textarea(pard, args):
	args.setdefault('field', True) # mettere false se stai ridisegnando il campo via ajax
	args.setdefault('id', '')
	args.setdefault('name', '')
	args.setdefault('label', '')
	args.setdefault('placeholder', '')
	args.setdefault('value', '')
	args.setdefault('control_class', '')
	args.setdefault('textarea_class', '')
	args.setdefault('help_message', '')
	args.setdefault('help_class', '') # is-success
	
	if not args['label']:
		args['label'] = args['name'].replace('_', ' ').title()
	
	h = []
	if args['field']:
		if args['id']:
			h.append('<div id="%(id)s" class="field">' % args)
		else:
			h.append('<div class="field">' % args)
	h.append('<label class="label">%(label)s</label>' % args)
	h.append('<div class="control %(control_class)s">' % args)
	h.append('<textarea class="textarea %(textarea_class)s" name="%(name)s" placeholder="%(placeholder)s">%(value)s</textarea>' % args)
	h.append('</div>')
	if args['help_message']:
		h.append('<p class="help %(help_class)s">%(help_message)s</p>' % args)
	if args['field']:
		h.append('</div>')
	
	return '\n'.join(h)


def notification(pard, args):
	args.setdefault('class', '') # is-danger, is-info
	args.setdefault('is-light', 'is-light')
	args.setdefault('messaggi', [])
	h = []
	h.append('<div class="notification %(class)s %(is-light)s">' % args)
	h.append('<button class="delete"></button>')
	h.append('<br>'.join(args['messaggi']))
	h.append('</div>')
	return '\n'.join(h)


def notification_js(pard):
	h = '''
		<script>
		document.addEventListener('DOMContentLoaded', () => {
		  (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
			var $notification = $delete.parentNode;

			$delete.addEventListener('click', () => {
			  $notification.parentNode.removeChild($notification);
			});
		  });
		});
		</script>
		'''
	return h


def img(pard, args):
	args.setdefault('img_class', 'is-128x128')
	args.setdefault('img_src', 'https://bulma.io/images/placeholders/128x128.png')
	h = []
	h.append('<figure class="image %(img_class)s">' % args)
	h.append('  <img src="%(img_src)s">' % args)
	h.append('</figure>' % args)
	return '\n'.join(h)


def card(pard, args):
	h = '''
<div class="card">
  <div class="card-image">
    <figure class="image is-4by3">
      <img src="https://bulma.io/images/placeholders/1280x960.png" alt="Placeholder image">
    </figure>
  </div>
  <div class="card-content">
    <div class="media">
      <div class="media-left">
        <figure class="image is-48x48">
          <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder image">
        </figure>
      </div>
      <div class="media-content">
        <p class="title is-4">John Smith</p>
        <p class="subtitle is-6">@johnsmith</p>
      </div>
    </div>

    <div class="content">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
      Phasellus nec iaculis mauris. <a>@bulmaio</a>.
      <a href="#">#css</a> <a href="#">#responsive</a>
      <br>
      <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
    </div>
  </div>
</div>
	'''