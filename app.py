from flask import Flask, request, render_template, redirect, flash
import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"

responses = list()

@app.route('/')
def homepage():
    '''Homepage landing'''
    return render_template('home.html', survey=surveys.satisfaction_survey)

@app.route('/questions/<num>')
def questions(num):
    '''questions based on questions number'''
    num = int(num)
    if num != len(responses):
        flash('Please view questions in order')
        return redirect(f'/questions/{len(responses)}')
    return render_template('question.html', question=surveys.satisfaction_survey.questions[num], num = num)

@app.route('/answer/<num>', methods=['POST'])
def answers(num):
    '''appends answer to database and then redirects to next question'''
    answer = request.form[num]
    num = int(num)
    responses.append(answer)
    if num < 3:
        return redirect(f'/questions/{num+1}')
    return redirect('/Thank_you')

@app.route('/Thank_you')
def thank_you():
    '''Thank you page'''

    return render_template('thank_you.html')
