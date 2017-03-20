<%inherit file="/base.mako"/>

<h2>User Settings</h2>

<ul>
  <li><a href="${h.url_for(controller='user', action='email')}">Set e-mail address</a></li>
% if request.environ['user'].resident:
  <li><a href="${h.url_for(controller='user', action='new')}">Register a new user</a></li>
  <li><a href="${h.url_for(controller='user', action='add_card')}">Register card</a></li>
% endif
</ul>
<h2>You own the following cards:</h2>
<ul>
% for card in c.cards:
 <li>${card.description} - serial: ${card.serial} <a href="${h.url_for(controller='user', action='remove_card')}">Unregister card</a></li>
% endfor
 <li><a href="${h.url_for(controller='user', action='add_card')}">Register new card</a></li>

</ul>
