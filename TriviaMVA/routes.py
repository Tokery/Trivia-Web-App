from flask import Flask, url_for, request, render_template;
from app import app;
import redis;


r = redis.StrictRedis(host='localhost',port=6379,db=0, charset="utf-8", decode_responses=True);

#Small Change

# server/
@app.route('/')
def hello():
    
    """Renders a sample page."""
    createLink = "<a href='" + url_for('create') + "'>Create a question</a>";
    return "<html><head><title>Hello, World!</title></head><body>" + createLink + "</body></html>"

# server/create
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        # send user the form
        return render_template ('CreateQuestion.html');
    elif request.method == "POST":
        # read form data and save it
        title = request.form['title'];
        answer = request.form['answer'];
        question = request.form['question'];

        # Store data in database
        # Key name will be whatever titlte they typed in
        # E.g. music:question countries:question

        r.set(title +':question', question)
        r.set(title +':answer', answer)

        return render_template ('CreatedQuestion.html', question = question);
    else:   
        return "<h2>Invalid Request</h2>";

#server/question/<title>
@app.route('/question/<title>', methods=['GET', 'POST'])
def question(title):
    if request.method == "GET":
        # send the user the form
       
        # Read question from database
        question = r.get(title +':question')

        return render_template ('AnswerQuestion.html', question = question);
    elif request.method == "POST":
        # User has attempted answer. Check if they are correct
        submittedAnswer = request.form['submittedAnswer'];
        
        # Read answer from database
        answer = r.get(title +':answer')

        if submittedAnswer == answer:
            return render_template('Correct.html');
        else:
            return render_template ('Incorrect.html', submittedAnswer = submittedAnswer, answer = answer);

    else:
        return '<h2> Invalid request </h2>';
    return "<h2>" + title + "</h2>";