import requests
import datetime
from pprint import pprint

from flask import Flask, send_from_directory, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database_setup import Base, UserAccount, Games, UserGames
# Games, UserGames, LeagueOfLegendsPlayers

app = Flask(__name__, static_folder='static')
app.secret_key = 'super secret key'

Engine = create_engine('postgres://localhost:5434/pvp')
Base.metadata.create_all(Engine)

DBsession = sessionmaker(bind=Engine)
session = DBsession()

@app.route('/riot.txt')
def riot():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/', methods=['GET', 'POST'])
def base():
    if request.method == 'POST':
        ip = request.remote_addr
        # DB REQEUST
        user = session.query(UserAccount).filter_by(email=request.form['email']).count()
        # TODO
        # if session expired we need to ask the user to login again
        if user:
            if user.user_games:
                return redirect(url_for('profile', user_id=user.id))
            else:
                return redirect(url_for('selectGames', user_id=user.id))
        else:
            # TODO
            # password will be hashed and the encrypted column will be removed
            # this was just for testing
            newUser = UserAccount(
                ip=ip,
                email=request.form['email'],
                password=request.form['password'],
                encrypted=request.form['email'] + ':' + request.form['password'],
            )
            session.add(newUser)
            session.commit()
            # user = session.query(UserAccount).filter_by(email=request.form['email']).one()
            # flash("welcome to the clan")
            return redirect(url_for('profile', user_id=user.id))
    else:
        return render_template('home.html')

@app.route('/select_game/<int:user_id>', methods=['GET', 'POST'])
def selectGames(user_id):
    if request.method == 'POST':
        newGame = UserGames(
            user_id = user_id,
            game_id = request.form['game_id'],
            gamer_name = request.form['gamer_name'],
            location = request.form['location'],
        )
        session.add(newGame)
        session.commit()
        return 'cxool'
        # redirect(url_for('profile', user_id=user_id))
    else:
        games = session.query(Games).all()
        return render_template('select_game.html', games=games)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)