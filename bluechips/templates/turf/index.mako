<%inherit file="/base.mako" />

<h2>Turf overview</h2>
Op deze pagina kun jij jouw laatste turfjes terug vinden.
<h4>Your recent history<h4>

${self.listTurf(c.turfEntries,False, False)}

<h4>Administratie</h4>
<a href="${h.url_for(controller='turf', action='history')}">Bekijk mijn volledige geschiedenis</a>

 
