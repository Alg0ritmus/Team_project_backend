## Social Network - projektový manažment 
#UPDATE 08/11/2022 - Branch main changes 
# Autori:
[ks588hn](https://github.com/ks588hn)  
[ALESO8](https://github.com/ALESO8)  
[IvanGadus](https://github.com/IvanGadus)  
  

...



# Backend - key info
1) vytvorenie virtual env:  
`py -m venv env`

2) superuser:  
username: admin    
password: admin  


Vykonané kroky:

1) vytvorenie backend & frontend zlozky  
1.1) vytvorenie virtual env  
1.2) pip install potrebne moduly (django, drf, drf-simplejwt... -> pip freeze)  
2) vytvorenie django projektu (django-admin startproject backend)  
3) vytvorenie django appky (py manage.py startapp base)
4) pridanie "base "appky do INSTALLED_APPS v settings.py
5) vytvorenie urls.py v "base" 
6) uprava settings.py -> pridanie drf & jwt do INSTALLED_APPS + REST_FRAMEWORK
7) pridanie a uprava JWT settings v settings.py
8) pridanie CORS origin all (settings.py)

# Uzitocne linky:  
https://jwt.io/  
https://excalidraw.com/   

# Ako funguje JWT?  
<img src=https://developer.okta.com/assets-jekyll/blog/node-token-auth/token-authentication-flow-69804c12334715c597128cd9273bca5e32ed516b62987902310efc54d1840a40.png>

Skuska P.Z.
