<%inherit file="/base.mako" />

<h2>Your recent history</h2>

${self.listTurf(c.turfEntries, True, False)}

<h2>Administratie</h2>
<a href="${h.url_for(controller='turf', action='history')}">Bekijk mijn volledige geschiedenis</a>

 
