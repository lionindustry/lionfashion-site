// Lion Fashion: colorway dots, copy buttons and the quote request form (English or Spanish by <html lang>).
(function () {
  var es = document.documentElement.lang === 'es';
  var WA = '16267029043', MAIL = 'sales@lionfashionglobal.com';

  document.addEventListener('click', function (e) {
    var b = e.target.closest('.sw');
    if (!b) return;
    var card = b.closest('.card');
    card.querySelector('.plate img').src = b.querySelector('img').getAttribute('src');
    card.querySelectorAll('.sw').forEach(function (s) { s.setAttribute('aria-pressed', s === b); });
  });

  function copyText(text, el) {
    var done = function () {
      if (!el) return;
      var o = el.textContent; el.textContent = es ? 'Copiado' : 'Copied';
      setTimeout(function () { el.textContent = o; }, 1600);
    };
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () {});
  }
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () { copyText(document.getElementById(b.dataset.copy).textContent, b); });
  });

  var form = document.getElementById('rfq');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = function (id) { return document.getElementById(id).value.trim(); };
    var err = document.getElementById('err');
    if (!v('q-co') || !v('q-mail')) {
      err.textContent = es ? 'Indique su empresa y correo para poder responderle.' : 'Add your company and email so we can reply.';
      err.hidden = false; return;
    }
    err.hidden = true;
    var CE = {"Men's boxers/trunks": 'Bóxers de hombre', "Women's briefs": 'Calzones de mujer', 'Thermal sets': 'Conjuntos térmicos', 'Sports underwear': 'Ropa interior deportiva'};
    var prog = (form.querySelector('input[name=program]:checked') || {}).value || '';
    var cats = Array.prototype.map.call(form.querySelectorAll('input[name=cat]:checked'), function (x) { return es ? CE[x.value] : x.value; }).join(', ') || (es ? 'No especificado' : 'Not specified');
    var L = es ? ['Solicitud de cotización de ropa interior', 'Empresa', 'Contacto', 'Correo', 'País', 'Programa', 'Categorías', 'Cantidad por modelo', 'Entrega deseada', 'Detalles']
               : ['Underwear quote request', 'Company', 'Contact', 'Email', 'Country', 'Program', 'Categories', 'Quantity per style', 'Target delivery', 'Details'];
    var t = L[0] + '\n' + L[1] + ': ' + v('q-co') + '\n' + L[2] + ': ' + (v('q-name') || '-') + '\n' + L[3] + ': ' + v('q-mail') + '\n' +
      L[4] + ': ' + (v('q-country') || '-') + '\n' + L[5] + ': ' + prog + '\n' + L[6] + ': ' + cats + '\n' + L[7] + ': ' + (v('q-qty') || '-') + '\n' +
      L[8] + ': ' + (v('q-date') || '-') + '\n' + L[9] + ': ' + (v('q-msg') || '-') + '\n\n' + location.href;
    document.getElementById('txt').textContent = t;
    document.getElementById('wa-link').href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(t);
    var mail = document.getElementById('mail-link');
    if (mail) mail.href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent(L[0] + ' - ' + v('q-co')) + '&body=' + encodeURIComponent(t);
    var out = document.getElementById('out'); out.hidden = false; out.scrollIntoView({ block: 'nearest' });
  });
  var ct = document.getElementById('copy-txt');
  if (ct) ct.addEventListener('click', function (e) { copyText(document.getElementById('txt').textContent, e.currentTarget); });
})();
