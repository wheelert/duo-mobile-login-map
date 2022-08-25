# duo-mobile-login-map
This generates an OpenStreet Map with markers showing locations of user logins for different applications as reported 
from your Duo Security account. 

This is a quick hack to generate a map with markers showing where users are loging in from. If time permits I may do this right 
and put it in geodjango or simular.


Requires Duo mobile client and admin-api access

Change Config peramaters in MapGen.py:
<pre>
 ikey='Duo Admin API integration key',
 skey='Duo integration secret key',
 host='api-....duosecurity.com',
</pre>
