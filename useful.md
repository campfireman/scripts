# useful scripts

remove docker images
sudo docker images -aq -f 'dangling=true' | sudo  xargs docker rmi

remove dangling images
sudo docker volume ls -qf dangling=true | sudo  xargs -r docker volume rm

find files containing content
grep -rnw '/path/to/somewhere/' -e 'pattern'

compare two files and merge
```
sudo bash -c "sdiff -o merged.js /usr/share/jitsi-meet/interface_config.js interface_config.js"
```
## only office
apache config:
```
<IfModule mod_ssl.c>
<VirtualHost *:443>
ServerName office.wasmitherz.de

LoadModule authn_core_module modules/mod_authn_core.so
LoadModule authz_core_module modules/mod_authz_core.so
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_http_module modules/mod_proxy_http.so
LoadModule proxy_wstunnel_module modules/mod_proxy_wstunnel.so
LoadModule headers_module modules/mod_headers.so
LoadModule setenvif_module modules/mod_setenvif.so
LoadModule ssl_module modules/mod_ssl.so

SSLProxyEngine on
SSLCipherSuite EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:ECDHE-RSA-AES128-SHA:DHE-RSA-AES128-GCM-SHA256:AES256+EDH:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384
SSLProtocol All -SSLv2 -SSLv3
SSLCompression off
SSLHonorCipherOrder on

SetEnvIf Host "^(.*)$" THE_HOST=$1
RequestHeader setifempty X-Forwarded-Proto https
RequestHeader setifempty X-Forwarded-Host %{THE_HOST}e
ProxyAddHeaders Off

ProxyPassMatch (.*)(\/websocket)$ "ws://127.0.0.1:9981/$1$2"
ProxyPass / "http://127.0.0.1:9981/"
ProxyPassReverse / "http://127.0.0.1:9981/"

SSLCertificateFile /etc/letsencrypt/live/office.wasmitherz.de/fullchain.pem
SSLCertificateKeyFile /etc/letsencrypt/live/office.wasmitherz.de/privkey.pem
Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
</IfModule>
```

run:
```
sudo docker run -i -t -d -p 9981:80 --restart=always \
    -v /app/onlyoffice/DocumentServer/logs:/var/log/onlyoffice  \
    -v /app/onlyoffice/DocumentServer/data:/var/www/onlyoffice/Data  \
    -v /app/onlyoffice/DocumentServer/lib:/var/lib/onlyoffice \
    -v /app/onlyoffice/DocumentServer/db:/var/lib/postgresql -e JWT_ENABLED='true' -e JWT_SECRET='<token>' onlyoffice/documentserver
```
