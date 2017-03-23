<%inherit file="/base.mako" />

<h2>Uitgebreide geschiedenis</h2>
% if c.own == 1:
  <a href="${h.url_for(controller='turf', action='history', own=0)}">Klik hier om de hele geschiedenis te zien</a>
% else:
  <a href="${h.url_for(controller='turf', action='history', own=1)}">Klik hier om alleen je eigen geschiedenis te zien</a>
% endif
<br><br>
${c.turfEntries.pager('page $page: $link_previous $link_next ~4~')}
${self.listTurf(c.turfEntries, False, True)}


 
