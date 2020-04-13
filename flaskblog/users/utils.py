import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message


# saving the file itself, returns the file name
def save_pic(form_picture):
    # create random hex
    ran_hex = secrets.token_hex(8)
    # if you're not using the variable, just use underscore
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_fn = ran_hex + f_ext
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_fn)
    # resizing before saving
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)
    # form_picture.save(pic_path)
    return pic_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', sender='noreply@dori.com', recipients=[user.email])
    msg.body = f'''Hi! This is yoondor.
To reset your pw, visit the following link. :
{url_for('users.reset_token', token=token, _external=True)}    
If you did not make this request, simply ignore this email and no change will be made.

p.s. HAIL SATAN

안녕! 윤돌이다.
비밀번호를 리셋하려면 다음 링크를 클릭해:
{url_for('users.reset_token', token=token, _external=True)}
네가 이 요청을 하지 않았다면, 그냥 이 메일을 무시하면 돼.
좋은 하루 보내!
'''

    mail.send(msg)
