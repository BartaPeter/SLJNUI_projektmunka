from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'key123'

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def calculate_bmi(weight, height):
    height_in_m = height / 100
    return round(weight / (height_in_m ** 2), 2)

def calculate_bmr(gender, weight, height, age):
    if gender == 1:  # Ferfi
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:  # No
        return 10 * weight + 6.25 * height - 5 * age - 161

def calculate_daily_calories(bmr, activity_level):
    activity_multipliers = {
        0: 1.2,  # Semmi aktivitas
        1: 1.375,  # Enyhe aktivitas
        2: 1.55  # Rendszeres
    }
    return round(bmr * activity_multipliers.get(activity_level, 1.2), 2)

def calculate_calorie_deficit(goal_weight_loss, days):
    total_calories_to_lose = goal_weight_loss * 7700
    return round(total_calories_to_lose / days, 2)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            age = int(request.form['Age'])
            gender = request.form['Gender']
            height = float(request.form['Height'])
            weight = float(request.form['Weight'])
            heart_rate = int(request.form['Heart_Rate'])
            physical_history = int(request.form['Physical_History'])
            weightlossgoal = int(request.form['Weight_Loss_Goal'])
            weightlosstime = int(request.form['Weight_Loss_Time']) * 30

            gender_numeric = 1 if gender.lower() == "male" else 0

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            user_id = cursor.lastrowid

            cursor.execute('''
                INSERT INTO user_data (
                    user_id, Age, Gender, Height, Weight, Avg_HR, 
                    Physical_History, Sleep_Duration, Quality_of_Sleep, Weight_Loss_Goal, Weight_Loss_Time, Distance, Calories, Time, Speed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, NULL, ?, ?, NULL, NULL, NULL, NULL)
            ''', (user_id, age, gender_numeric, height, weight, heart_rate,
                  physical_history, weightlossgoal, weightlosstime ))

            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except Exception as e:
            return render_template('register.html', error_message=f"Hiba történt: {str(e)}")

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and user['password'] == password: 
            session['user_id'] = user['id']
            return redirect(url_for('kezdolap'))
        return render_template('login.html', error_message="Hibás felhasználónév vagy jelszó!") 
    return render_template('login.html')

@app.route('/kezdolap', methods=['GET', 'POST'])
def kezdolap():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()

    user_data = conn.execute('''
        SELECT * FROM user_data WHERE user_id = ?
    ''', (user_id,)).fetchone()

    if user_data is None:
        conn.close()
        return render_template('kezdolap.html', error_message="Felhasználói adatok nem találhatók!")

    if request.method == 'POST':
        try:
            weightnew = int(request.form['Weightnew'])
            sleep_duration = int(request.form['Sleep_Duration'])
            quality_of_sleep = int(request.form['Quality_of_Sleep'])
            steps = (int(request.form['Steps']) * 0.05) #atlagos lepesszamlalo keplet
            maincalories = (int(request.form['Calories']) - steps) #kivonjuk az addigi napi lepesszamot
            bmi = calculate_bmi(weightnew, user_data['Height'])
            bmr = calculate_bmr(user_data['Gender'], weightnew, user_data['Height'], user_data['Age'])
            daily_calories = calculate_daily_calories(bmr, user_data['Physical_History'])
            calorie_deficit = calculate_calorie_deficit(user_data['Weight_Loss_Goal'], user_data['Weight_Loss_Time'])
            target_calories = max(bmr, daily_calories - calorie_deficit)

            conn.close()
            return render_template('result.html', bmi=bmi, target_calories=target_calories,day = user_data['Weight_Loss_Time'], goal=user_data['Weight_Loss_Goal'], caloriess=maincalories)

        except Exception as e:
            conn.close()
            return render_template('kezdolap.html', user_data=user_data, error_message=f"Hiba történt: {str(e)}")

    conn.close()
    return render_template('kezdolap.html', user_data=user_data)

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
