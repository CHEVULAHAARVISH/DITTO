from flask import Flask, render_template, url_for, flash, redirect, session, request
from flaskblog.models import User, Mail
from flaskblog import app, bcrypt, db
from flaskblog.forms import RegristrtationForm, LoginForm, QrcodeForm
import subprocess
from flask_login import login_user, current_user, logout_user, login_required
import random
from flaskblog.models import Mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pyqrcode as qr
import qrcode
import pyrebase 

def generate_qrcode():
    x = random.randint(1000, 9999)
    qr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(x)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image = qr_image.resize((500, 500))
    qr_image.save("QRCODE.png")

    # Store the value of x in Firebase
    firebaseConfig = {
        "apiKey": "AIzaSyBpi-oM5Yxpp-9d0PmBUkGDUz1Q_tQpHLM",
        "authDomain": "ditto-2b57b.firebaseapp.com",
        "databaseURL": "https://ditto-2b57b-default-rtdb.firebaseio.com",
        "projectId": "ditto-2b57b",
        "storageBucket": "ditto-2b57b.appspot.com",
        "messagingSenderId": "623176561332",
        "appId": "1:623176561332:web:365da031201202ffc69de1",
        "measurementId": "G-TTT6H08PF8"
    }
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    db.child("passcode").set(x)

    return x
def send_mail(email):
    from_email = 'deliveryditto@gmail.com'
    to_email = email

    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'DITTO DELIVERY'
    html_file = "flaskblog/email.html"
    
    feedback_link = "https://forms.gle/fgku2EUcgmnTT5uh8"

    with open(html_file, 'r') as f:
        html_attachment = MIMEText(f.read(), 'html')
        msg.attach(html_attachment)

    qr_code_file = 'QRCODE.png'

    with open(qr_code_file, 'rb') as f:
        qr_code_attachment = MIMEBase('application', 'octet-stream')
        qr_code_attachment.set_payload((f).read())
        encoders.encode_base64(qr_code_attachment)
        qr_code_attachment.add_header('Content-Disposition', "attachment; filename= %s" % qr_code_file)
        msg.attach(qr_code_attachment)
    with open(html_file, 'r') as f:
        email_content = f.read()
        email_content = email_content.replace('{{feedback_link}}', feedback_link)
        html_attachment = MIMEText(email_content, 'html')
        msg.attach(html_attachment)    

    msg_str = msg.as_string()

    email_session = smtplib.SMTP('smtp.gmail.com', 587)
    email_session.starttls()
    email_session.login(from_email, 'gkbltrhhngtfsxrm')

    email_session.sendmail(from_email, to_email, msg_str)
    email_session.quit()

@app.route("/")
@app.route("/home",methods = ['GET'])
def home():
    current_page = 'home'
    image_src = "https://i.postimg.cc/rpPdGNpX/1.jpg" 
    return render_template("home.html",image_src=image_src,current_page=current_page)

@app.route("/about")
def about():
    return render_template("about.html",title = "About")

@app.route("/register",methods =['GET','POST'])
def register():
    form=RegristrtationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user=User( usernames=form.username.data,password=hashed_password,email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created successfully","success")
        return redirect(url_for("login"))
    return render_template("register.html",title = "Register",form=form)    
     
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("run_script"))
        else:
            flash("Login unsuccessful")
    return render_template("login.html", title="login", form=form)

@app.route("/run_script", methods=['GET', 'POST'])
@login_required
def run_script():
    form = QrcodeForm()
    if form.validate_on_submit():
        email = form.email.data
        mail = Mail(email=email)
        db.session.add(mail)
        db.session.commit()

        qr_code_data = generate_qrcode()
        send_mail(email)

        flash(f"Package will be delivered shortly,Check {email} for QRcode", "success")
        return redirect(url_for("home"))

    return render_template("send.html", title="Send", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
