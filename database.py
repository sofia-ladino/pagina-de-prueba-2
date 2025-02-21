from pymongo import MongoClient
import gridfs


# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["imagenes_db"]  # Base de datos
fs = gridfs.GridFS(db)  # GridFS para almacenamiento de imágenes
