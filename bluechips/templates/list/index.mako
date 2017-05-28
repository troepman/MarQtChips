<%inherit file="/base.mako" />

<h2>Shopping list</h2>

${self.listList(c.listEntries)} 

<h2>New item</h2>
<form action="${h.url_for(controller='list', action='add')}", method="POST">
${h.auth_token_hidden_field()}
${h.text('subject', size=32, value="")}
<input class="submitbutton" type="submit" value="Add!">
</form>
