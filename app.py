from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient
import gridfs
import io

app = Flask(__name__)

# Conectar a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["imagenes_db"]  # Base de datos
fs = gridfs.GridFS(db)  # GridFS para almacenar archivos

# Ruta para subir imágenes
@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({"message": "No se seleccionó ninguna imagen"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"message": "Nombre de archivo vacío"}), 400

    image_id = fs.put(image, filename=image.filename)  # Guardar en GridFS
    return jsonify({"message": "Imagen subida exitosamente", "image_id": str(image_id)})

# Ruta para obtener imágenes por ID
@app.route('/image/<image_id>', methods=['GET'])
def get_image(image_id):
    try:
        image = fs.get(image_id)
        return send_file(io.BytesIO(image.read()), mimetype="image/jpeg")
    except Exception as e:
        return jsonify({"message": "Imagen no encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
