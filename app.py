from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForMaskedLM
import torch
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os




app = Flask(__name__)


# Разрешение CORS для фронтенда
CORS(app, resources={r"/*": {"origins": "https://asel-it.github.io/lifeplan/"}})


# Конфигурация базы данных
db_config = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'lifeplan_user'),
    'password': os.environ.get('DB_PASSWORD', 'lp_data'),
    'database': os.environ.get('DB_NAME', 'lp_db')
}


# Путь к модели
MODEL_PATH = "C:/Users/Public/work/LifePlan_backend/xlm-roberta-base"


# Загрузка токенизатора и модели с локального пути (передаем путь к папке, а не к файлу)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForMaskedLM.from_pretrained(MODEL_PATH, local_files_only=True)


# Подготовка входных данных
text = "Replace me by any text you'd like."
encoded_input = tokenizer(text, return_tensors='pt')


# Прогон модели
output = model(**encoded_input)


# Вывод результатов
print(output)






# Подключение к базе данных
def get_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Ошибка подключения к базе данных: {err}")
        raise


# Инициализация базы данных
def init_db():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Инициализация базы данных завершена.")
    except Exception as e:
        print(f"Ошибка инициализации базы данных: {e}")
        raise


# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    if not username or not password:
        return jsonify({'error': 'Имя пользователя и пароль обязательны'}), 400


    hashed_password = generate_password_hash(password, method='sha256')


    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()
        return jsonify({'message': 'Пользователь успешно зарегистрирован'}), 201
    except mysql.connector.Error as err:
        if err.errno == 1062:  # Ошибка уникального ограничения
            return jsonify({'error': 'Имя пользователя уже существует'}), 400
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()


# Авторизация пользователя
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    if not username or not password:
        return jsonify({'error': 'Имя пользователя и пароль обязательны'}), 400


    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()


        if user and check_password_hash(user[2], password):
            return jsonify({'message': 'Успешный вход'}), 200
        else:
            return jsonify({'error': 'Неверные учетные данные'}), 401
    finally:
        cursor.close()
        conn.close()


# Генерация текста
@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    prompt = data.get('prompt', '')


    if not prompt:
        return jsonify({'error': 'Требуется запрос'}), 400


    try:
        with torch.no_grad():
            inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
            outputs = model(**inputs)
            generated_text = tokenizer.decode(outputs.logits.argmax(dim=-1)[0], skip_special_tokens=True)
        return jsonify({'response': generated_text}), 200
    except Exception as e:
        return jsonify({'error': f"Ошибка генерации текста: {e}"}), 500


# Отдача статических файлов
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)


# Инициализация базы данных при необходимости
init_db()


# Запуск Flask-приложения
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # По умолчанию порт 10000
    app.run(host="0.0.0.0", port=port)




