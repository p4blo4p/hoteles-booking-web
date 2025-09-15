from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# Cargar datos de hoteles desde JSON
def cargar_hoteles():
    with open('data/hoteles.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    hoteles = cargar_hoteles()
    return render_template('index.html', hoteles=hoteles)

@app.route('/hotel/<hotel_id>')
def hotel_detalle(hotel_id):
    hoteles = cargar_hoteles()
    hotel = next((h for h in hoteles if h['id'] == hotel_id), None)
    
    if not hotel:
        return "Hotel no encontrado", 404
    
    return render_template('hotel.html', hotel=hotel)

@app.route('/api/hoteles')
def api_hoteles():
    hoteles = cargar_hoteles()
    return jsonify(hoteles)

if __name__ == '__main__':
    app.run(debug=True)
