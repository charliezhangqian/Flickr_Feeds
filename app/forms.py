from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required
 
class LoginForm(Form):
    query = TextField('openid', validators = [Required()])