from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
from urllib.parse import urlparse

PORT = 3000
BASE_DIR = Path(__file__).resolve().parent
tareas = []
siguiente_id = 1


class Handler(BaseHTTPRequestHandler):
    def enviar_json(self, estado, datos):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(estado)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        global siguiente_id
        ruta = urlparse(self.path).path

        if ruta == "/api/tareas":
            self.enviar_json(200, tareas)
            return

        nombre = "trabajo.html" if ruta == "/" else ruta.lstrip("/")
        archivo = (BASE_DIR / nombre).resolve()

        if BASE_DIR not in archivo.parents and archivo != BASE_DIR:
            self.send_error(404)
            return

        if not archivo.is_file():
            self.send_error(404)
            return

        tipos = {".html": "text/html", ".css": "text/css", ".js": "text/javascript"}
        contenido = archivo.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", tipos.get(archivo.suffix, "application/octet-stream") + "; charset=utf-8")
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

    def do_POST(self):
        ruta = urlparse(self.path).path
        if ruta != "/api/tareas":
            self.send_error(404)
            return

        longitud = int(self.headers.get("Content-Length", "0"))
        datos = json.loads(self.rfile.read(longitud) or b"{}")
        texto = str(datos.get("texto", "")).strip()

        if not texto:
            self.enviar_json(400, {"error": "La tarea no puede estar vacía"})
            return

        global siguiente_id
        tarea = {"id": siguiente_id, "texto": texto}
        siguiente_id += 1
        tareas.append(tarea)
        self.enviar_json(201, tarea)

    def do_DELETE(self):
        ruta = urlparse(self.path).path
        prefijo = "/api/tareas/"

        if not ruta.startswith(prefijo):
            self.send_error(404)
            return

        try:
            tarea_id = int(ruta[len(prefijo):])
        except ValueError:
            self.send_error(404)
            return

        global tareas
        tareas = [tarea for tarea in tareas if tarea["id"] != tarea_id]
        self.enviar_json(200, {"ok": True})

    def log_message(self, formato, *argumentos):
        print(f"{self.address_string()} - {formato % argumentos}")


if __name__ == "__main__":
    servidor = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Servidor listo en http://localhost:{PORT}")
    servidor.serve_forever()
