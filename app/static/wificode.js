
(function() {

	const live = function(event_name, selector, callback, allow_default) {
		document.addEventListener(event_name, function(event){
			let element = event.target.closest(selector);
			if (element) {
				if(!allow_default) event.preventDefault();
				callback(element, event);
			}
		});
	};

	let xhr;
	let timeout;

	const refresh_preview = function () {
		clearTimeout(timeout);
		timeout = setTimeout(function () {
	
			xhr = new XMLHttpRequest();

			if (!xhr) {
			  alert('Giving up :( Cannot create an XMLHTTP instance');
			  return false;
			}
			xhr.onload = function () {
				render_preview(this.responseText);
			};
	
			let ssid = document.querySelector("#input_ssid input");
			let ssid_pw = document.querySelector("#input_ssid_pw input");
			let query = []
			query.push(encodeURIComponent('action') + '=' + encodeURIComponent('refresh_preview'));
			query.push(encodeURIComponent('rec[ssid]') + '=' + encodeURIComponent(ssid.value));
			query.push(encodeURIComponent('rec[ssid_pw]') + '=' + encodeURIComponent(ssid_pw.value));
			let qq = query.join('&');
		
			let url = '/?' + qq;
			xhr.open('GET', url, true);
			xhr.send();
		}, 1000);
	
	};

	const render_preview = function (resp) {
		let prev = document.getElementById('div_preview');
		prev.innerHTML = resp;
	};
	

	live('keyup', '#input_ssid input', refresh_preview);
	live('keyup', '#input_ssid_pw input', refresh_preview);

})();
