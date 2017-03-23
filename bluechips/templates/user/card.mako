<%inherit file="/base.mako"/>

<h2>Add card</h2>

<ul>
  <form action="${h.url_for(controller='user', action='update_card', id=c.card.id)}" method="post">
  ${h.auth_token_hidden_field()}
  <table class="form">
   <tr>
    <th><label for="serialcode">Serial code</label></th>
    <td>${h.text('serialcode',size=32, enabled="False")}</td>
  </tr>
  <tr>
    <th><label for="description">Description</label></th>
    <td>${h.text('description', size=32)}</td>
  </tr>
  <tr>
    <td colspan="2">
      <input class="submitbutton" id="none" type="submit" value="Submit" />
    </td>
  </tr>
  </table>
  </form>
</ul>
