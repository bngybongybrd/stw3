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
        flash("Log in unsuccessful. Please enter email!", "danger")
        
      elif password == b'':
        flash("Log in unsuccessful. Please enter password!", "danger")
      
      elif login_result[0]:
          session['username'] = login_result[2]
          session['email'] = login_result[1]
          return redirect(url_for('real_home_page'))
      elif login_result[0] == False :
         flash("Log in unsuccessful. Please type in the correct email and corresponding password!", "danger")

    
    return render_template('real_login.html')

@app.route('/real_home_page', methods=['GET', 'POST'])
def real_home_page():
  username = session.get('username')
  if request.method == "POST":
    email = session.get('email')
    age = request.form.get('age')
    gender = request.form.get('gender')
    activity = request.form.get('activity')
    cal = request.form.get('calorie')
    carbs = request.form.get('carbs')
    fat = request.form.get('fat')
    smoking = request.form.get('smoking-status')
    alcohol = request.form.get('alcohol-status')
    pregnant = request.form.get('pregnant')
    weight = request.form.get('weight')
    height = request.form.get('height')
      
    if age != '' and gender != '' and activity != '' and cal != '' and fat != '' and smoking != '' and alcohol != '' and pregnant != '' and weight != '' and height != '':
      bmi = float(weight) /(float(height)**2)
      bmi = round(bmi,1)
      bmi = str(bmi)
      query.insert_personal_info(email, age, gender, activity,cal,carbs, fat, smoking, alcohol, bmi, pregnant)
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
    activity=info[0][3]
    cal=info[0][4]
    carbs=info[0][5]
    fat=info[0][6]
    smoking=info[0][7]
    alcohol=info[0][8]
    bmi=info[0][9]
    pregnant=info[0][10]    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
        presence_penalty = 0,
        frequency_penalty = 0,
    messages=[
        {"role": "system", "content": 
          "You are a professional and helpful Singaporean doctor. \
         You are to give a personalized recommendation based on the following \
         information provided. The information will include:\
         \n\n1. Age \
         2. Gender \
         3. Physical Actvity Level (Sendantry/ Lightly Active/ Moderately Active/ Very Active/ Extremely Active) \
         4. Calorie Intake () \
         5. Carbohydrate Intake ()\
	 6. Fat Intake ()\
         7. Smoking Status ()\
         8. Alcohol Consumption ()\
         9. Body Mass Index ()\
         10. Pregnancy status ()\
         \n\nYou are to provide the recommendation in the following format: \
         Your personal recommendation, answering in singlish ,\
         Suggestions or actions to take in point form, \
         Any other information you deem necessary"

        },
        {"role": "user", 
          "content": "Age: {}, Gender: {}, Physical activity: {}, Calorie intake: {}, Carbohydrate intake: {}, Fat intake: {},Smoking Status: {}, Alcohol Consumption : {},Body Mass index: {},Pregnancy status: {}".format(age, gender, activity, cal, carbs, fat, smoking, alcohol, bmi, pregnant)},
        ],
        temperature=0.2
    )

    responses = response['choices'][0]['message']['content']
    responses = responses.split('\n')

    
    return render_template('results.html', username=username, age=info[0][1], gender=info[0][2], activity=info[0][3], cal=info[0][4], carbs=info[0][5], fat=info[0][6], smoking=info[0][7], alcohol=info[0][8], bmi=info[0][9], pregnant=info[0][10], responses=responses)



app.run(host='0.0.0.0', port=81)
