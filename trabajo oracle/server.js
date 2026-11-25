const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = 3000;
let tareas = [];
let siguienteId = 1;

function enviarJson(respuesta, estado, datos) {
  respuesta.writeHead(estado, { "Content-Type": "application/json; charset=utf-8" });
  respuesta.end(JSON.stringify(datos));
}

const servidor = http.createServer((peticion, respuesta) => {
  const url = new URL(peticion.url, `http://${peticion.headers.host}`);

  if (url.pathname === "/api/tareas" && peticion.method === "GET") {
    return enviarJson(respuesta, 200, tareas);
  }

  if (url.pathname === "/api/tareas" && peticion.method === "POST") {
    let cuerpo = "";
    peticion.on("data", (parte) => cuerpo += parte);
    peticion.on("end", () => {
      const datos = JSON.parse(cuerpo || "{}");
      if (!datos.texto || !datos.texto.trim()) {
        return enviarJson(respuesta, 400, { error: "La tarea no puede estar vacía" });
      }
      const tarea = { id: siguienteId++, texto: datos.texto.trim() };
      tareas.push(tarea);
      enviarJson(respuesta, 201, tarea);
    });
    return;
  }

  if (url.pathname.startsWith("/api/tareas/") && peticion.method === "DELETE") {
    const id = Number(url.pathname.split("/").pop());
    tareas = tareas.filter((tarea) => tarea.id !== id);
    return enviarJson(respuesta, 200, { ok: true });
  }

  let archivo = url.pathname === "/" ? "trabajo.html" : url.pathname.slice(1);
  const ruta = path.join(__dirname, archivo);

  fs.readFile(ruta, (error, contenido) => {
    if (error) {
      respuesta.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      return respuesta.end("No encontrado");
    }
    const extension = path.extname(ruta);
    const tipos = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css" };
    respuesta.writeHead(200, { "Content-Type": tipos[extension] || "application/octet-stream" });
    respuesta.end(contenido);
  });
});

servidor.listen(PORT, () => {
  console.log(`Servidor listo en http://localhost:${PORT}`);
});
