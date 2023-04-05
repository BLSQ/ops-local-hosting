
# Make sure you have 

- the dns records pointing to the apache server
- a log file directory is available (don't forget to log rotate it)
- the proxy and proxy_http modules are enabled

if not done you can enable the mods via 

```
a2enmod proxy
a2enmod proxy_http
systemctl restart apache2
```

## Add an http site conf

```
cd /etc/apache2/sites-available
nano dataviz.conf
```

in `site-available` directory create a conf file (dataviz.conf


```
<VirtualHost *:80>

    ProxyPreserveHost On
    ProxyPass / http://xxx.xxx.traefik.xxx/

    DocumentRoot /var/www/html/
    ServerName yourdomain.com
    ErrorLog logs/yourdomain.com-error.log
    CustomLog logs/yourdomain.com-access.log common

</VirtualHost>
```

adapt the log path, yourdomain.com and the proxy pass ip address/name to the traefik instance

### Enable the https site vie lets encrypt

```
a2ensite test-apache-mbayang.conf 

journalctl -xeu apache2.service
systemctl restart apache2
```

## then enable the https

```
sudo certbot --apache 
```
answer the questions (email, contact info) then pick the domain you want to enable
rince and repeat for the other domains
