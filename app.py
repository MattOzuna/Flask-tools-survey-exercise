from flask import Flask, request, render_template, redirect, flash, session
import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"


@app.route('/')
def homepage():
    '''Homepage landing'''
    return render_template('home.html', survey=surveys.satisfaction_survey)

@app.route('/survey-start', methods=['POST'])
def survey_start():
    '''
    sets session['responses'] to an empty string
    redirects to the first qeustion
    '''
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<num>')
def questions(num):
    '''questions based on questions number'''
    num = int(num)
    if num != len(session['responses']):
        flash('Please view questions in order')
        return redirect(f'/questions/{len(session['responses'])}')
    return render_template('question.html', question=surveys.satisfaction_survey.questions[num], num = num)

@app.route('/answer/<num>', methods=['POST'])
def answers(num):
    '''appends answer to database and then redirects to next question'''
    
    answer = request.form[num]
    num = int(num)
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    if num < 3:
        return redirect(f'/questions/{num+1}')
    return redirect('/Thank_you')

@app.route('/Thank_you')
def thank_you():
    '''Thank you page'''
    return render_template('thank_you.html')
