<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>${self.title()}</title>
    ${h.stylesheet_link('%s/css/main.css' % request.script_name)}
    ${h.stylesheet_link('//ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/flick/jquery-ui.css')}
    ${h.javascript_link('//ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js')}
    ${h.javascript_link('//ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.min.js')}
    ${h.javascript_link('%s/js/admin.js' % request.script_name)}
  </head>
  <body>
    % if c.mobile_client:
      <div id="mobile">
        <a href="${h.url_for(request.url, use_non_mobile='no')}">Use mobile interface</a>
      </div>
    % endif
    <div id="nav" class="block">
      <table>
        <tr>
          <td>
            <h1 class="title">
              % if c.title:
                ${c.title}
              % else:
                BlueChips
              % endif
            </h1>
          </td>
          <td>
            <a href="${h.url_for(controller='status', action='index')}">
              <img src="${request.script_name}/icons/status.png" alt="">
              <span>Dashboard</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='spend', action='index')}">
              <img src="${request.script_name}/icons/spend.png" alt="">
              <span>Expense</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='transfer', action='index')}">
              <img src="${request.script_name}/icons/transfer.png" alt="">
              <span>Transfer</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='history', action='index')}">
              <img src="${request.script_name}/icons/history.png" alt="">
              <span>History</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='user', action='index')}">
              <img src="${request.script_name}/icons/user.png" alt="">
              <span>User</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='turf', action='index')}">
              <img src="${request.script_name}/icons/turf.png" alt="">
              <span>Turfing</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='list', action='index')}">
              <img src="${request.script_name}/icons/shopping.png" alt="">
              <span>Shopping</span>
            </a>
          </td>
        </tr>
      </table>
    </div>
    % for message in h.flash.pop_messages():
      <div class="flash">${message}</div>
    % endfor
    <div id="content">
      ${next.body()}
    </div>
  </body>
</html>

<%def name="title()">BlueChips
% if c.title != '':
  :: ${c.title}
% endif
</%def>

<%def name="formatUser(user)">
  % if user == request.environ['user']:
    <strong>Me</strong>
  % else:
    ${user.name}
  % endif
</%def>

<%def name="listExpenditures(es)">
  <table class="list">
    <tr>
      <th class="date">Date</th>
      <th class="user">Spender</th>
      <th class="description">Description</th>
      <th class="amount">Amount</th>
      <th class="share">My Share</th>
      <th class="editlink"></th>
      <th class="deletelink"></th>
    </tr>
    % for e in es:
      <%
        if e.involves(request.environ['user']):
          klass = 'user-involved'
        else:
          klass = 'user-not-involved'
      %>
      <tr class="${klass}">
        <td class="date">${e.date}</td>
        <td class="user">${formatUser(e.spender)}</td>
        <td class="description">${e.description}</td>
        <td class="amount">${e.amount}</td>
        <td class="share">${e.share(request.environ['user'])}</td>
        <td class="editlink">${h.link_to('Edit', h.url_for(controller='spend', action='edit', id=e.id))}</td>
        <td class="deletelink">${h.link_to('Delete', h.url_for(controller='spend', action='delete', id=e.id))}</td>
      </tr>
    % endfor
  </table>
</%def>

<%def name="listTransfers(ts)">
  <table class="list">
    <tr>
      <th class="date">Date</th>
      <th class="user">From</th>
      <th class="user">To</th>
      <th class="description">Description</th>
      <th class="amount">Amount</th>
      <th class="editlink"></th>
      <th class="deletelink"></th>
    </tr>
    % for t in ts:
      <%
        if t.involves(request.environ['user']):
          klass = 'user-involved'
        else:
          klass = 'user-not-involved'
      %>
      <tr class="${klass}">
        <td class="date">${t.date}</td>
        <td class="user">${formatUser(t.debtor)}</td>
        <td class="user">${formatUser(t.creditor)}</td>
        <td class="description">${t.description}</td>
        <td class="amount">${t.amount}</td>
        <td class="editlink">${h.link_to('Edit', h.url_for(controller='transfer', action='edit', id=t.id))}</td>
        <td class="deletelink">${h.link_to('Delete', h.url_for(controller='transfer', action='delete', id=t.id))}</td>
      </tr>
    % endfor
  </table>
</%def>

<%def name="listTurf(ts, own, admin)">
  <table class="list">
    <tr>
      <th class="date">Datum</th>
      <th class="date">Tijd</th>
      % if not own:
        <th class="user">Persoon</th>
      % endif
      % if admin:
        <th class="desciption">Pas</th>
      % endif
      <th class="description">Omschrijving</th>
      % if admin:
        <th class="deletelink">Verwijderen?</th>
      % endif
    </tr>
    % for t in ts:
      <tr>
        <td class="date">${t.entered_time.strftime("%Y-%m-%d")}</td>
        <td class="date">${t.entered_time.strftime("%H:%M:%S")}</td>
        % if not own:
          <td class="user">${formatUser(t.card.user)}</td>
        % endif
        % if admin:
          <td class="description">${t.card.description}</td>
        % endif
        <td class="description">${t.subject}</td>
        % if admin:
          <td class="deletelink">${h.link_to('Verwijder', h.url_for(controller='turf', action='delete', id=t.id))}</td>
        % endif
      </tr>
    % endfor
  </table>
</%def>
<%def name="listList(ls)">
  <table class="list">
    <tr>
      <th class="description">?</th>
      <th class="description">Description</th>
      <th class="user">Added by</th>
      <th class="date">Added on</th>
      <th class="user">Checked by</th>
      <th class="date">Checked on</th>
    </tr>
    % for l in ls:
      <tr>
        % if l.checker is None:
          <td class="description"><input type="checkbox" onclick="
             this.enabled=false;
             //alert('checking');
             if (this.checked) // other way around
             {
               $.ajax({type: 'POST',
                 url:'${h.url_for(controller='list', action='check', id=l.id)}',
                 success: function(data){this.enabled=true;},
                 error: function(data){alert('error');}
                 });
             }
             else
             {
               $.ajax({type: 'POST',
                 url:'${h.url_for(controller='list', action='uncheck', id=l.id)}',
                 success: function(data){this.enabled=true;},
                 error: function(data){alert('error');}
                 });
             }
          "/>
          </td>
        % else:
          <td class="description"><input type="checkbox" disabled checked></td>
        % endif
        <td class="description">${l.subject}</td>
        <td class="user">${formatUser(l.creater)}</td>
        <td class="date">${l.createdTime.strftime("%m-%d %H:%M")}</td>
        % if l.checker is None:
          <td class="user"></td>
          <td class="date"></td>
        % else:
          <td class="user">${formatUser(l.checker)}</td>
          <td class="date">${l.checkedTime.strftime("%m-%d %H:%M")}</td>
        % endif
      </tr>
    % endfor
  </table>
</%def>

<%def name="expenditureIcon()">
&larr;<span class="dollarsign">&rarr;
</%def>

<%def name="transferIcon()">
<span class="dollarsign">EUR</span> &rarr; <span class="dollarsign">EUR</span>
</%def>
