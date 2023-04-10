from db import db, Database  # importy dla bazy danych
import json
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import secrets

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
    url = 'https://stooq.pl/'
    try:
        with open('logins.json', 'r') as openfile:
            json_logins = json.load(openfile)
    except:
        return templates.TemplateResponse('error_login.html', context={'request': request,
                                                                 'uname': uname, 'psw': psw})
    for login in json_logins:
        if login == uname:
            if json_logins[uname] == psw:
                return RedirectResponse(url)
    else:
        return templates.TemplateResponse('error.html', context={'request': request,
                                                                 'uname': uname, 'psw': psw})
#endpointy dla dla signup

@app.get('/signup')
async def read_signupForm(request: Request):
    uname = 'Enter Username'
    psw1 = 'Enter password'
    psw2 = 'Repeat password'
    email = 'email'
    return templates.TemplateResponse('signup_form.html', context={'request': request, 'uname': uname,
                                                                  'psw1': psw1, 'psw2': psw2, 'email': email})

@app.post('/signup')
async def signupForm(request: Request, uname: str = Form(...),
                     psw1: str = Form(...), psw2: str = Form(...), email = Form(...)):
    if psw1 == psw2:
        users_dict[uname] = psw1
        logins_data = json.dumps(users_dict)
        with open("logins.json", "w") as outfile:
            outfile.write(logins_data)
        return templates.TemplateResponse('signup_form.html', context={'request': request, 'uname': uname,
                                                                  'psw1': psw1, 'psw2': psw2, 'email': email})
    else:
        return templates.TemplateResponse('error_signup.html', context={'request': request, 'uname': uname,
                                                                  'psw1': psw1, 'psw2': psw2, 'email': email})
    
    @app.post("/register")
    async def register(request: Request, email: str = Form(...), password: str = Form(...)):
        # generowanie losowego kodu weryfikacyjnego
        verification_code = secrets.token_urlsafe(32)
        # zapisywanie kodu weryfikacyjnego w bazie danych
        db.store_verification_code(email, verification_code)

        # konfiguracja wiadomości email
        message = MIMEMultipart()
        message["From"] = "example@gmail.com"
        message["To"] = email
        message["Subject"] = "Verification code"

        # treść wiadomości email
        text = f"""
        Hello,

        Thank you for registering. Please click on the following link to verify your email address:

        http://localhost:8000/verify?email={email}&code={verification_code}

        Best regards,
        Your App Team
        """
        message.attach(MIMEText(text, "plain"))

    # wysyłanie wiadomości email
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
            smtp.starttls()
            smtp.login("example@gmail.com", "password")
            smtp.send_message(message)

        return templates.TemplateResponse("registration_success.html", {"request": request})


@app.get("/verify")
async def verify(request: Request, email: str, code: str):
    # weryfikacja kodu weryfikacyjnego
    if db.check_verification_code(email, code):
        db.mark_email_verified(email)
        return templates.TemplateResponse("verification_success.html", {"request": request})
    else:
        return templates.TemplateResponse("verification_failure.html", {"request": request})
    


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)




