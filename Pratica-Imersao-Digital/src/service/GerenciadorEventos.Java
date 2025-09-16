// src/main/java/br/com/yourevent/service/GerenciadorEventos.java
package br.com.yourevent.service;

import br.com.yourevent.model.Evento;
import br.com.yourevent.model.Usuario;
import br.com.yourevent.model.CategoriaEvento;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

public class GerenciadorEventos {
    private List<Evento> eventos;
    private List<Usuario> usuarios;
    private Usuario usuarioLogado;

    public GerenciadorEventos() {
        this.eventos = FileManager.carregarEventos();
        this.usuarios = new ArrayList<>();
        this.usuarioLogado = null;
    }

    public void cadastrarUsuario(Usuario usuario) {
        if (!usuarios.contains(usuario)) {
            usuarios.add(usuario);
        }
    }

    public boolean fazerLogin(String email, String senha) {
        for (Usuario usuario : usuarios) {
            if (usuario.getEmail().equals(email) && usuario.getSenha().equals(senha)) {
                usuarioLogado = usuario;
                return true;
            }
        }
        return false;
    }

    public void fazerLogout() {
        usuarioLogado = null;
    }

    public void cadastrarEvento(Evento evento) {
        eventos.add(evento);
        FileManager.salvarEventos(eventos);
    }

    public List<Evento> getEventos() {
        return new ArrayList<>(eventos);
    }

    public List<Evento> getEventosOrdenadosPorData() {
        return eventos.stream()
                .sorted(Comparator.comparing(Evento::getDataHora))
                .collect(Collectors.toList());
    }

    public List<Evento> getEventosFuturos() {
        return eventos.stream()
                .filter(Evento::isFuturo)
                .sorted(Comparator.comparing(Evento::getDataHora))
                .collect(Collectors.toList());
    }

    public List<Evento> getEventosPassados() {
        return eventos.stream()
                .filter(Evento::isPassado)
                .sorted(Comparator.comparing(Evento::getDataHora))
                .collect(Collectors.toList());
    }

    public List<Evento> getEventosOcorrendoAgora() {
        return eventos.stream()
                .filter(Evento::isOcorrendoAgora)
                .collect(Collectors.toList());
    }

    public Evento buscarEventoPorId(int id) {
        return eventos.stream()
                .filter(e -> e.getId() == id)
                .findFirst()
                .orElse(null);
    }

    public void participarEvento(int eventoId) {
        if (usuarioLogado == null) return;

        Evento evento = buscarEventoPorId(eventoId);
        if (evento != null) {
            usuarioLogado.participarEvento(evento);
        }
    }

    public void cancelarParticipacao(int eventoId) {
        if (usuarioLogado == null) return;

        Evento evento = buscarEventoPorId(eventoId);
        if (evento != null) {
            usuarioLogado.cancelarParticipacao(evento);
        }
    }

    public List<Evento> getEventosUsuario() {
        if (usuarioLogado == null) return new ArrayList<>();
        return new ArrayList<>(usuarioLogado.getEventosParticipando());
    }

    public Usuario getUsuarioLogado() {
        return usuarioLogado;
    }

    public boolean isUsuarioLogado() {
        return usuarioLogado != null;
    }
}
