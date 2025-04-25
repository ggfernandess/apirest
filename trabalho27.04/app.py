
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('veiculos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')                                                                        
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    conn = sqlite3.connect('veiculos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicles')
    vehicles = [dict(id=row[0], brand=row[1], model=row[2], year=row[3]) for row in cursor.fetchall()]
    conn.close()
    return jsonify(vehicles)

@app.route('/api/vehicles', methods=['POST'])
def add_vehicle():
    data = request.json
    conn = sqlite3.connect('veiculos.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO vehicles (brand, model, year) VALUES (?, ?, ?)', (data['brand'], data['model'], data['year']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Veículo cadastrado com sucesso!'}), 201

@app.route('/api/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    conn = sqlite3.connect('veiculos.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vehicles WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Veículo deletado com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)
