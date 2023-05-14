import os
from flask import Flask, render_template, request, flash, redirect, url_for, session
import query
import openai

my_secret = os.environ['OPEN AI KEY']
openai.api_key = my_secret

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b9540e7c60e0b2a2a36e3b96387e50c9'

@app.route('/', methods=['GET', 'POST'])
def real_login():
    if request.method == "POST":
      
      email = request.form.get('email')
      password = request.form.get('password').encode('utf-8')
      login_result = query.login_check(email, password)
      if email == '':
        flash("Logged in unsuccessful. Please enter email!", "danger")
        
      elif password == b'':
        flash("Logged in unsuccessful. Please enter password!", "danger")
      
      elif login_result[0]:
          session['username'] = login_result[2]
          session['email'] = login_result[1]
          return redirect(url_for('real_home_page'))
      elif login_result[0] == False :
         flash("Logged in unsuccessful. Please type in the correct email and corresponding password!.", "danger")

    
    return render_template('real_login.html')

@app.route('/real_home_page', methods=['GET', 'POST'])
def real_home_page():
  username = session.get('username')
  if request.method == "POST":
    email = session.get('email')
    age = request.form.get('age')
    gender = request.form.get('gender')
    cholesterol = request.form.get('cholesterol')
    bp = request.form.get('blood-pressure')
    smoking = request.form.get('smoking-status')
    if age != '' and gender != '' and cholesterol != '' and bp != '' and smoking != '':
      query.insert_personal_info(email, age, gender, cholesterol, bp, smoking)
      return redirect(url_for('results'))
  return render_template('real_home_page.html', username=username)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
      email_input = request.form.get('email') 
      pw_input = request.form.get('password').encode('utf-8')
      username_input = request.form.get('username')
      if query.sign_up(email_input, pw_input, username_input):
        return redirect(url_for('real_login'))
      else:
        flash("Email already exists", "warning")
    return render_template('sign_up.html')

@app.route('/results')
def results():
    info = query.get_personal_info(session.get('email'))
    username = session.get('username')
    age = info[0][1]
    gender=info[0][2]
    ch=info[0][3]
    bp=info[0][4]
    smoking=info[0][5]

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a professional and helpful doctor. \
         You are to give a personalized recommendation based on the following \
         information provided. The information will include:\
         \n\n1. Age Range \
         2. Gender \
         3. Cholesterol (mmol/L) \
         4. Blood Pressure (mmHg) \
         5. Smoking Status \
         \n\nYou are to provide the recommendation in the following format: \
         Your personal recommendation, \
         Suggestions or actions to take in point form, \
         Any other information you deem necessary"
        },
        {"role": "user", 
          "content": "Age: {}, Gender: {}, Cholesterol: {}, Blood Pressure: {}, Smoking Status: {}".format(age, gender, ch, bp, smoking)},
        ],
        temperature=0.2
    )

    responses = response['choices'][0]['message']['content']
    responses = responses.split('\n')

    age_weight = 0.3
    gender_weight = 0.2
    bp_weight = 0.4
    ch_weight = 0.1

    age_l =age.split('-')
    age_val = int(age_l[0]) + int(age[1])
    age_val = age_val // 2

    if gender == 'male':
        gender_val = 1
    else:
        gender_val = 0
    
    bp_l = bp[:7]
    bp_l = bp_l.split("-")
    bp_val = int(bp_l[0]) + int(bp_l[1])
    bp_val = int(bp_val//2)

    ch_l = ch[:7]
    ch_l = ch_l.split("-")
    ch_val = float(ch_l[0]) + float(ch_l[1])
    ch_val = int(ch_val//2)
    
    
    if smoking == "smoke":
        risk_score = (age_val *age_weight + gender_weight*gender_val + bp_val*bp_weight + ch_val*ch_weight) + 1
    else:
        risk_score = (age_val *age_weight + gender_weight*gender_val + bp_val*bp_weight + ch_val*ch_weight)

    if risk_score >=50:
        risk = '(High Risk)'
    elif risk_score < 50 and risk_score >=35:
        risk = ("Medium Risk")
    else:
        risk = '(Low Risk)'

    
    risk_a = f"{risk_score} {risk}"
    
    return render_template('results.html', username=username, age=info[0][1], gender=info[0][2], ch=info[0][3], bp=info[0][4], smoking=info[0][5], responses=responses, risk_a=risk_a)



app.run(host='0.0.0.0', port=81)
