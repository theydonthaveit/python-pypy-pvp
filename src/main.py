from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database_setup import Base, UserAccount

Engine = create_engine('postgresql://localhost:5434/pvp')
Base.metadata.create_all(Engine)

DBsession = sessionmaker(bind=Engine)
session = DBsession()

@app.route('/', methods=['GET', 'POST'])
def base():
    if request.method == 'POST':
        ip = request.remote_addr
        user = session.query(UserAccount).filter_by(email=request.form['email']).one()
        if user:
            flash("You are a user, sign in")
            return render_template('sign_in.html', user_email=user.email)
        else:
            newUser = UserAccount(
                ip = ip,
                email=request.form['email'],
                password=request.form['password'],
                encrypted=request.form['email'] + ':' + request.form['password']
            )
            session.add(newUser)
            session.commit()
            flash("welcome to the clan")
            return redirect(url_for('loggedIn'))
    else:
        return render_template('home.html')

@app.route('/home/')
def loggedIn():
    return 'Hi'

if __name__ == '__main__':
    app.secret_key='super'
    app.debug=True
    app.run(host='0.0.0.0', port=5000)