import json
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse


app = FastAPI()
templates = Jinja2Templates(directory="templates/")

users_dict = {}


# endpointy dla LoginForm

@app.get('/login/')
async def read_loginForm(request: Request):
    uname = 'Enter Username'
    psw = 'Enter password'
    return templates.TemplateResponse('login_form.html', context={'request': request,
                                                                  'uname': uname, 'psw': psw})

@app.post('/login/')
async def loginForm(request: Request, uname: str = Form(...), psw: str = Form(...)):
    url = 'https://www.youtube.com/watch?v=mM8nGt4Z8lI'
    try:
        with open('logins.json', 'r') as openfile:
            json_logins = json.load(openfile)
    except:
        return {"brak dostępu do bazy (logins) -proszę o rejestracje użytkownika |Sign Up|"}
    for login in json_logins:
        if login == uname:
            if json_logins[uname] == psw:
                return RedirectResponse(url)
    else:
        return templates.TemplateResponse('error_login.html', context={'request': request,
                                                                 'uname': uname, 'psw': psw})
#endpointy dla dla signup

@app.get('/signup')
async def read_signupForm(request: Request):
    uname = 'Enter Username'
    psw1 = 'Enter password'
    psw2 = 'Repeat password'
    return templates.TemplateResponse('signup_form.html', context={'request': request, 'uname': uname,
                                                                  'psw1': psw1, 'psw2': psw2})

@app.post('/signup')
async def signupForm(request: Request, uname: str = Form(...),
                     psw1: str = Form(...), psw2: str = Form(...)):
    if psw1 == psw2:
        users_dict[uname] = psw1
        logins_data = json.dumps(users_dict)
        with open("logins.json", "w") as outfile:
            outfile.write(logins_data)
        return templates.TemplateResponse('signup_form.html', context={'request': request, 'uname': uname,
                                                                  'psw1': psw1, 'psw2': psw2})
    else:
        return templates.TemplateResponse('error_signup.html', context={'request': request, 'uname': uname,
                                                                  'psw1': psw1, 'psw2': psw2})



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)




