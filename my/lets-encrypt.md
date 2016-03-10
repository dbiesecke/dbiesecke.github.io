Let's Encrypt
=============================
Endlich ist es soweit! Gratis SSL Cert's & vorallem FREE - für alle!
Das Project steht wirklich noch am Anfang, jedoch funktionieren die ersten Tools schon wunderbar!
... der offizielle Installer macht jedoch bei mir immer wieder Probleme, aber gibt ja noch [LEGO](https://github.com/xenolf/lego) & dutzemde andere Projecte


| Tools/Libs                    | Lang | DL                                              | My-opinion                                                |
|-------------------------------|------|-------------------------------------------------|-----------------------------------------------------------|
| Caddy - HTTP Server           | GO   | [LINK](https://caddyserver.com/download)        | fast Webserver and will auto-generate a SSL cert for you! |
| LEGO - Go Lets Encrypt Client | GO   | [LINK](https://github.com/xenolf/lego/releases) | Easy to use Client to generate Certs                      |
|                               |      |                                                 |                                                           |

LEGO
=====================

Install LEGO
------------------
`curl -kL https://github.com/xenolf/lego/releases/download/v0.1.1/lego_linux_amd64.tar.xz > out.tar.xz`


Using LEGO 
--------------------------------
Da es ein GO program ist, deckt es eine breite Pallete an Betriebsystemen ab.

[LEGO-release](https://github.com/xenolf/lego/releases)


## lego
### Create a valid SSL cert
 * **Command with arguments**: `~/lego --email="username@gmail.com" --domains="yourdomain.de" run`
 * **Description**: Create SSL certs for following Domain
 * **Example CRON**: `@reboot     cd "/root";  /root/lego --email=admin@nated.at --domains=lair.nated.at run;cp -R ~/.lego/certificates/* /etc/ssl/private/`








