[DreamFactory API](http://blog.dreamfactory.com/blog/bid/326379/Getting-Started-with-the-DreamFactory-API)
====================



DreamFactory - Auth
=======================

  * communication fully in JSON
  `{“email”:”email_value”, “password”:”password_value”}`

 
Example:
==========


    curl -k -3 -X POST https://127.0.0.1:8080/rest/user/session -H "X-DreamFactory-Application-Name: todojquery" -d "{ \"email\" : \"webmaster@btc-mining.at\", \"password\" : \"yeah12ha\" }"
    
    
    
    
    
    
    
    
    
    

    