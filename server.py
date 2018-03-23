from secrets import randbelow
from flask import Flask, render_template, send_from_directory, url_for, request, redirect, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Engine, UserAccount, GamerProfile, LeagueOfLegendsProfileBase
from forms.forms import LoginForm, RegistrationForm, GamerProfileForm
from generators.passcode_generator import passcode_generator_INT
from generators.name_generator import name_generator_STRING
from BuildProfile.initialCall import initialCall
from BuildProfile.matchCall import matchCall, recentMatchCall
from BuildProfile.tierCall import tierCall


from fake.fake_name_db import fake_name_db_ARRAY
from fake.fake_logger import fake_logger_ARRAY

Base.metadata.create_all(Engine)

DBsession = sessionmaker(bind=Engine)
session = DBsession()

app = Flask(__name__, static_folder='static')
app.secret_key = 'xxxxx'
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return session.query(UserAccount).get(user_id)


@app.route('/')
def index():
    # va = 'piggy'
    # print(randbelow(999999))
    # return va
    return render_template('index.html')


@app.route('/riot')
def riot():
    return send_from_directory(app.static_folder, 'riot.txt')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        userSeekingAccess = session.query(UserAccount).filter_by(email=form.email.data).first()

        if userSeekingAccess is not None:
            if userSeekingAccess.decode_password(form.passcode.data):
                login_user(userSeekingAccess, remember=form.remember_me.data)
                return redirect(url_for('dashboard'))

            return 'bad creds'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        proposed_username = name_generator_STRING()
        proposed_password = passcode_generator_INT()

        if proposed_username in fake_name_db_ARRAY:
            proposed_username = proposed_username + ("%d" % randbelow(999))

        fake_name_db_ARRAY.append(proposed_username)
        fake_logger_ARRAY.append({proposed_username, proposed_password})

        print(fake_logger_ARRAY)

        userToBeAdded = UserAccount(
            username=name_generator_STRING(),
            mobile=form.mobile.data,
            email=form.email.data,
            passcode="%d" % proposed_password,
            ip_address=request.environ['REMOTE_ADDR']
        )
        try:
            session.add(userToBeAdded)
            session.commit()
        except:
            session.rollback()
            flash('This account already exists, please login')

    return render_template('signup.html', form=form)


@app.route('/build_gamer_profile/<int: user_id>', methods=['GET', 'POST'])
# @login_required
def buildGamerProfile(user_id):
    form = GamerProfileForm()
    if form.validate_on_submit():
        resp = initialCall(form.summoner_name.data)

        User = session.query(UserAccount).get(user_id)
        User.gamer_profile = [GamerProfile(
            game = form.game.data,
            in_game_name = form.summoner_name.data,
            country = form.country.data,
            postal_code = form.postcode_zipcode.data
        )]

        try:
            session.add(User)
            newGamerProfile = session.query(GamerProfile).order_by(desc(GamerProfile.id)).first()
            newGamerProfile.league_of_legends_profile = [
                LeagueOfLegendsProfileBase(
                    account_id=resp['accountId']
                )
            ]
            session.add(newGamerProfile)
            session.commit()
        except:
            session.rollback()
            return 'we are good'

    return render_template('build_your_profile.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(
        debug=True,
        use_reloader=True
    )