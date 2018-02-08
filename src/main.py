from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database_setup import Base, UserAccount, Games, UserGames

Engine = create_engine('postgresql://localhost:5434/pvp')
Base.metadata.create_all(Engine)

DBsession = sessionmaker(bind=Engine)
session = DBsession()

@app.route('/', methods=['GET', 'POST'])
def base():
    if request.method == 'POST':
        ip = request.remote_addr
        # DB REQEUST
        user = session.query(UserAccount).filter_by(email=request.form['email']).one()
        # TODO
        # if session expired we need to ask the user to login again
        if user:
            flash("You are a user, sign in")
            return render_template('sign_in.html', user_email=user.email, user_id=user.id)
        else:
            # TODO
            # password will be hashed and the encrypted column will be removed
            # this was just for testing
            newUser = UserAccount(
                ip=ip,
                email=request.form['email'],
                password=request.form['password'],
                encrypted=request.form['email'] + ':' + request.form['password']
            )
            session.add(newUser)
            session.commit()
            # DB REQEUST
            user = session.query(UserAccount).filter_by(email=request.form['email']).one()
            flash("welcome to the clan")
            return redirect(url_for('profile', user_id=user.id))
    else:
        # TODO
        # this is just for development as I haven't implemented an web auth
        # and require cookie, session or JWT setting
        ip = request.remote_addr
        # DB REQEUST
        user = session.query(UserAccount).filter_by(ip=ip).one()
        if user:
            return redirect(url_for('profile', user_id=user.id))
        else:
            return render_template('home.html')

@app.route('/game_profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if request.method == 'POST':
        # DB REQUEST
        # TODO
        # not simply look up user etc.
        # you want to know if they should add this game or not
        user = session.query(UserGames).filter_by(user_id=user_id).first()
        if user:
            return 'You got games'
        else:
            newGameForUser = UserGames(
                user_id=user_id,
                location=request.form['location'],
                gamer_name=request.form['gamer_name'],
                game_id=request.form['game_id'],
            )
            session.add(newGameForUser)
            session.commit()
            return 'Im good'
    else:
        # DB REQUEST
        # TODO
        # needs to look if the user has a game associated with their account
        # user = session.query(UserAccount).filter_by(id=user_id).one()
        games = 0
        if games:
            return render_template('profile.html', user_id=user_id)
        else:
            games = session.query(Games).all()
            return render_template('selet_game.html', games=games, user_id=user_id)
            # return redirect(url_for('select_game', user_id=user_id))

if __name__ == '__main__':
    app.secret_key='super'
    app.debug=True
    app.run(host='0.0.0.0', port=5000)