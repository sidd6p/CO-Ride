import secrets
from PIL import Image
import os
import smtplib, ssl
from flask import current_app
from flask_mail import Message
from flaskFile import mail
from flask import url_for

def sendEmail(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('user.resetPassword', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)
    # token = user.getResetToken()
    # msg = Message(
    #   'Password Reset',
    #   sender ='noreply@demo.com', 
    #   recipients = [user.email]
    # )
    # msg.body = "Hello This is working"
    # msg.body = f'''To reset Your password, visit the following link: {url_for('user.resetPassword', token=token, _external=True)}
    # If you did not make this request then simply ignore this email and no changes will be made.
    # '''
    mail.send(msg)

    # port = 465    
    # smtp_server = "smtp.gmail.com"
    # sender_email = os.environ.get('co_user')
    # receiver_email = user.email
    # password = os.environ.get('co_pswd')
    # message = "Hello Siddhartha"
    # # message = f'''To reset Your password, visit the following link: {url_for('user.resetPassword', token=token, _external=True)}'''
    # # link = "{}".format(url_for('user.resetPassword', token=token, _external=True))
    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, message)

    # s = smtplib.SMTP('smtp.gmail.com', 587)
    # s.starttls()
    # s.login(sender_email, password)
    # s.sendmail(sender_email, receiver_email, message)
    # s.quit()


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