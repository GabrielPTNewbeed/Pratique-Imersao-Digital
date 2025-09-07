// src/main/java/br/com/yourevent/model/Usuario.java
package br.com.yourevent.model;

import java.util.ArrayList;
import java.util.List;

public class Usuario {
    private static int contadorId = 1;
    
    private int id;
    private String nome;
    private String email;
    private String telefone;
    private String senha;
    private List<Evento> eventosParticipando;

    public Usuario(String nome, String email, String telefone, String senha) {
        this.id = contadorId++;
        this.nome = nome;
        this.email = email;
        this.telefone = telefone;
        this.senha = senha;
        this.eventosParticipando = new ArrayList<>();
    }

    // Getters e Setters
    public int getId() { return id; }
    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getTelefone() { return telefone; }
    public void setTelefone(String telefone) { this.telefone = telefone; }
    public String getSenha() { return senha; }
    public void setSenha(String senha) { this.senha = senha; }
    public List<Evento> getEventosParticipando() { return eventosParticipando; }

    public void participarEvento(Evento evento) {
        if (!eventosParticipando.contains(evento)) {
            eventosParticipando.add(evento);
            evento.adicionarParticipante(this);
        }
    }

    public void cancelarParticipacao(Evento evento) {
        if (eventosParticipando.contains(evento)) {
            eventosParticipando.remove(evento);
            evento.removerParticipante(this);
        }
    }

    @Override
    public String toString() {
        return String.format("ID: %d | Nome: %s | Email: %s | Telefone: %s", 
                id, nome, email, telefone);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Usuario usuario = (Usuario) obj;
        return email.equals(usuario.email);
    }
}
