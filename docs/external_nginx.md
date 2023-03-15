# For each domain

rails apps are verifying the "origin" and might need the X-Forwarded-\* headers

in the `sites-available` or `conf.d` (a bit less clean) create a file with your domain name (here `hesabu.mydomain.com.conf`)

the proxy_pass goes to the machine where traefik has been installed/configure (TLS_ENABLED: false in the host variables)

```
server {

        root /var/www/your_domain/html;
        index index.html index.htm index.nginx-debian.html;
        client_max_body_size 100M;

        server_name hesabu.mydomain.com;
        location / {

                  proxy_pass http://172.27.1.103:80;
  		          proxy_set_header  Host $host;
  	              proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
  		          proxy_set_header  X-Forwarded-Proto $scheme;
  		          proxy_set_header  X-Forwarded-Ssl on; # Optional
  		          proxy_set_header  X-Forwarded-Port $server_port;
 		          proxy_set_header  X-Forwarded-Host $host;


         }

}

```

then request the certificates for that domain

```
sudo certbot --nginx -d hesabu.mydomain.com
sudo nginx reload
```

then the nginx config will look like this

```
server {
        root /var/www/your_domain/html;
        index index.html index.htm index.nginx-debian.html;
        server_name hesabu.mydomain.com;
        client_max_body_size 100M;
        location / {
                  proxy_pass http://172.27.1.103:80;
  		          proxy_set_header  Host $host;
  	              proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
  		          proxy_set_header  X-Forwarded-Proto $scheme;
  		          proxy_set_header  X-Forwarded-Ssl on; # Optional
  		          proxy_set_header  X-Forwarded-Port $server_port;
 		          proxy_set_header  X-Forwarded-Host $host;
         }
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/hesabu.mydomain.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/hesabu.mydomain.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
server {
    if ($host = hesabu.mydomain.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot
        server_name hesabu.mydomain.com;
    listen 80;
    return 404; # managed by Certbot
}

```
