from flask import Flask, send_from_directory, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__, static_folder='static')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database_setup import Base, UserAccount

Engine = create_engine('postgresql://localhost:5434/pvp')
Base.metadata.create_all(Engine)

DBsession = sessionmaker(bind=Engine)
session = DBsession()

@app.route('//riot.txt')
def riot():
    return send_from_directory(app.static_folder, request.path[1:])
@app.route('/', methods=['GET', 'POST'])
def base():
    if request.method == 'POST':
        ip = request.remote_addr
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
                ip = ip,
                email=request.form['email'],
                password=request.form['password'],
                encrypted=request.form['email'] + ':' + request.form['password']
            )
            session.add(newUser)
            session.commit()
            user = session.query(UserAccount).filter_by(email=request.form['email']).one()
            flash("welcome to the clan")
            return redirect(url_for('profile', user_id=user.id))
    else:
        # TODO
        # this is just for development as I haven't implemented an web auth
        # and require cookie, session or JWT setting
        ip = request.remote_addr
        user = session.query(UserAccount).filter_by(ip=ip).one()
        if user:
            return redirect(url_for('profile', user_id=user.id))
        else:
            return render_template('home.html')

@app.route('/game_profile/<int:user_id>')
def profile(user_id):
    return render_template('profile.html', user_id=user_id)

if __name__ == '__main__':
    app.secret_key='super'
    app.debug=True
    app.run(host='0.0.0.0', port=5000)