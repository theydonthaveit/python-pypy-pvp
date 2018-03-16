from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, AnyOf

# FIXME:
# class ValidateGames(AnyOf):
#     all_games = ['League of Legends']

#     def result(self):
#         return AnyOf(self.all_games)


class RegistrationForm(FlaskForm):
    mobile = StringField('mobile', validators=[InputRequired(), Length(min=11, max=14)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])

class LoginForm(FlaskForm):
    email = StringField('email', validators=[Email(message='Invalid Email'), Length(max=50)])
    passcode = PasswordField('passcode', validators=[InputRequired(), Length(min=8, max=8)])
    remember_me = BooleanField('remeber me')

class GamerProfileForm(FlaskForm):
    # create a new type of validator to validate a game
    game = StringField('game',
        validators=[
            InputRequired(),
            AnyOf(['League of Legends'])
        ])
    region = StringField('server region',
        validators=[
            InputRequired(),
            AnyOf(['euw', 'na'])
        ])
    # create new type of validator to validate player name
    summoner_name = StringField('player name',
        validators=[
            InputRequired(),
        ])
    country = StringField('country',
        validators=[
            InputRequired(),
            AnyOf(['United Kingdom'],
            message='We currently cater for UK only')
        ])
    # create a new type of validator to validate a postcode or zipcode
    postcode_zipcode = StringField('postcode / zipcode',
        validators=[
            InputRequired()
        ])