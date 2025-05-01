from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)

# Criar banco de dados se não existir
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS searches
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  image_url TEXT,
                  result TEXT,
                  date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Simular pesquisa de imagem
def fake_image_search(image_url):
    # Aqui você poderá conectar APIs ou scraper futuramente
    return f"Resultado fictício para a imagem {image_url}"

# Endpoint para busca de imagem
@app.route('/search', methods=['POST'])
def search_image():
    data = request.json
    image_url = data.get('image_url')

    if not image_url:
        return jsonify({"error": "Imagem não enviada"}), 400

    result = fake_image_search(image_url)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO searches (image_url, result, date) VALUES (?, ?, ?)",
              (image_url, result, str(datetime.datetime.now())))
    conn.commit()
    conn.close()

    return jsonify({"image_url": image_url, "result": result})

# Endpoint para ver histórico de buscas
@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM searches")
    rows = c.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "image_url": row[1],
            "result": row[2],
            "date": row[3]
        })

    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True)
