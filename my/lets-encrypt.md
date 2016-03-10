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


Using LEGO - 
=========================
Da es ein GO program ist, deckt es eine breite Pallete an Betriebsystemen ab.

[LEGO-release](https://github.com/xenolf/lego/releases)


## lego
### Argument example
 * **Command with arguments**: `~/lego --email="username@gmail.com" --domains="yourdomain.de" run`
 * **Description**: Create SSL certs for following Domain
 * **Output**:
   * <div class="slide" style="cursor: pointer;"> **OS:** Show/Hide</div><div class="view"><code>2016/03/10 07:11:52 [INFO][yourdomain.de] acme: Obtaining bundled SAN certificate
2016/03/10 07:11:52 [INFO][yourdomain.de] acme: Trying to solve HTTP-01
2016/03/10 07:11:53 [INFO] Served key authentication
2016/03/10 07:11:54 [INFO][yourdomain.de] The server validated our request
2016/03/10 07:11:54 [INFO][yourdomain.de] acme: Validations succeeded; requesting certificates
2016/03/10 07:11:54 [INFO] acme: Requesting issuer cert from https://acme-v01.api.letsencrypt.org/acme/issuer-cert
2016/03/10 07:11:55 [INFO][yourdomain.de] Server responded with a certificate.
    </code></div>






