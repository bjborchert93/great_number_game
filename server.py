from crypt import methods
from tokenize import Number
from flask import Flask, render_template, session, request, redirect
import random

app = Flask(__name__)
app.secret_key = "secrets secrets are no fun..."

@app.route('/')
def home():
    print(f"session length: {len(session)}")
    if len(session) == 0:
        print('no random number found in session. making one now.')
        session['rand_number'] = random.randint(1,100)
        print(f"the random number I'm thinking of is {session['rand_number']}")
        session['replay_disp_prop'] = "none"
        session['fdbk_disp_prop'] = "none"
        session['guess_disp_prop'] = "block"
        session['attempts'] = 0

    return render_template('index.html')

@app.route('/guess_handler', methods=['POST'])
def handle_guess():

    # store the user's guess in session
    session['guess'] = request.form['guess']

    # initialize amount of attempts if it hasn't been intitialized yet, otherwise increment
    if 'attempts' in session:
        session['attempts'] += 1
    else:
        session['attempts'] = 1

    # make sure the guess the user entered is actually a number. (Negative numbers will return false)
    if session['guess'].isnumeric() == False or int(session['guess']) > 100:
        print('the value entered was not valid')
        session['fdbk_disp_prop'] = "block"
        session['feedback'] = "Enter a number between 1 and 100"
        session['color'] = "red"
        return redirect('/')

    # Store user's guess and the random number in variables to make calculations easier
    rand_number = int(session['rand_number'])
    guess = int(session['guess'])
    attempts = int(session['attempts'])
    print(f"the last guess was {session['guess']}")

    # decide what to display on the redirect ("/home" route) based on the user's guess 
    if guess == rand_number: # user guessed correctly
        print("you got it!")
        session['feedback'] = f"{session['guess']} was the number!"
        session['fdbk_disp_prop'] = "block"
        session['replay_disp_prop'] = "block"
        session['color'] = "green"
        session['guess_disp_prop'] = "none"
    else:
        if attempts == 5: # 5 failed attempts will result in a loss
            print("you lose!")
            session['feedback'] = "You lose!"
            session['replay_disp_prop'] = "block"
            session['guess_disp_prop'] = "none"
            session['color'] = "red"
        else:
            if guess > rand_number: # user guessed too high
                print("too high!")
                session['feedback'] = "Too high!"
                session['color'] = "red"
            else:
                print("too low!") # user guessed too low
                session['feedback'] = "Too low!!"

            # these session values will be set if the user didn't guess correctly
            session['color'] = "red"
            session['fdbk_disp_prop'] = "block"
            session['replay_disp_prop'] = "none"
            session['guess_disp_prop'] = "block"
    return redirect('/')

@app.route('/destroy_session')
def destroy_session():
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)