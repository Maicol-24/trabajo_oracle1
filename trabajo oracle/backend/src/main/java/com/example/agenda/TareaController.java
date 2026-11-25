package com.example.agenda;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/tareas")
@CrossOrigin(origins = "*")
public class TareaController {
    private final TareaRepository repositorio;

    public TareaController(TareaRepository repositorio) {
        this.repositorio = repositorio;
    }

    @GetMapping
    public List<Tarea> listar() {
        return repositorio.findAll();
    }

    @PostMapping
    public ResponseEntity<?> crear(@RequestBody Tarea datos) {
        if (datos.getTexto() == null || datos.getTexto().trim().isEmpty()) {
            return ResponseEntity.badRequest().body("La tarea no puede estar vacía");
        }

        Tarea tarea = new Tarea(datos.getTexto().trim());
        Tarea guardada = repositorio.save(tarea);
        return ResponseEntity.status(HttpStatus.CREATED).body(guardada);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        if (!repositorio.existsById(id)) {
            return ResponseEntity.notFound().build();
        }

        repositorio.deleteById(id);
        return ResponseEntity.ok().build();
    }
}
