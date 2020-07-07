from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired, Email,Length


class Valid_mail(FlaskForm):
    # def __init__(self,mail):
    #     self.mail = mail
    email = StringField(validators=[Email(),DataRequired()], render_kw={'class': "form-control", 'placeholder':"change mail"})
    submit = SubmitField('save')
