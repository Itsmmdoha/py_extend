import requests
from bs4 import BeautifulSoup

username = input("username: ") 
password= input("password: ") 

url ='https://www.pythonanywhere.com'
login_route = '/login/'

s = requests.Session()
s.headers.update({'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'})
   
r = s.get(url)

csrftoken = r.cookies['csrftoken']

payload = {
    'auth-username': username,
    'auth-password': password,
    'csrfmiddlewaretoken': csrftoken,
    'login_view-current_step': 'auth'
}

headers={
    'referer':url+login_route,
    'origin' : url
        }
        
        
s.headers.update(headers)

def login():
    lres = s.post(url+login_route,data=payload)
    return lres
    
    
login_res = login()
csrftoken = login_res.cookies["csrftoken"] #the token changes after login
print("obtained login csrf:",csrftoken)

def get_expiry():
    r = s.get(url+f"/user/{username}/webapps")
    soup = BeautifulSoup(r.content,"html.parser")
    p_tag = soup.find("p",{"class":"webapp_expiry"})
    return p_tag.find("strong").text
old_expiry = get_expiry()
print("Old expiry is:",old_expiry)

data = {
    "csrfmiddlewaretoken":csrftoken
}
extend = s.post(url+f"/user/{username}/webapps/{username}.pythonanywhere.com/extend",data=data)
new_expiry = get_expiry()
if extend.status_code == 200:
  print("Extended to:",new_expiry)
else:
  print(extend)
