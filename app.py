from flask import Flask, render_template, redirect, url_for, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
import torch
import os

app = Flask(__name__, static_folder="LifePlan_frontend/static", template_folder="LifePlan_frontend/templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Создаем подключение к базе данных
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Инициализация модели ИИ
model_name = 'xlm-roberta-base'
tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)  # Используем XLMRobertaTokenizer
model = XLMRobertaForSequenceClassification.from_pretrained(model_name)  # Используем XLMRobertaForSequenceClassification


# Модели базы данных
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Главная страница (Дашборд)
@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

# Страница авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

# Страница выхода
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Запрос к модели ИИ
@app.route('/predict', methods=['POST'])
@login_required
def predict():
    text = request.json.get('text')
    inputs = tokenizer(text, return_tensors='pt')
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=-1).item()
    return jsonify({'prediction': prediction})

# Для доступа к статическим файлам фронтенда
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    # Создание всех необходимых таблиц при запуске
    with app.app_context():  # Окружение в контексте приложения
        if not os.path.exists('users.db'):
            db.create_all()

    # Запуск приложения с SSL (если нужно)
    app.run(ssl_context=('mkcert+1.pem', 'mkcert+1-key.pem'), debug=True, host="0.0.0.0", port=5000)
