import secrets
from PIL import Image
import os
from flask import current_app
from flask_mail import Message
from flaskFile import mail
from flask import url_for

def sendEmail(user):
    token = user.getResetToken()
    msg = Message('Password Reset', sender='this.corride@gmail.com', recipients=[user.email])
    msg.body = "To reset Your password, visit the following link {}".format(url_for('resetPassword', token=token, _external=True))
    mail.send(msg)

def save_picture(formPicture):
    random_hex = secrets.token_hex(8)
    _, fileExt = os.path.splitext(formPicture.filename)
    pictureName = random_hex + fileExt
    picturePath = os.path.join(current_app.root_path, 'static\profile_pics', pictureName)
    outputSize = (125, 125)
    i = Image.open(formPicture)
    i.thumbnail(outputSize)
    i.save(picturePath)
    return pictureName