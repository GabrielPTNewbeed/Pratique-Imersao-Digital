// src/main/java/br/com/yourevent/model/Evento.java
package br.com.yourevent.model;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

public class Evento {
    private static int contadorId = 1;
    
    private int id;
    private String nome;
    private String endereco;
    private CategoriaEvento categoria;
    private LocalDateTime dataHora;
    private String descricao;
    private List<Usuario> participantes;

    public Evento(String nome, String endereco, CategoriaEvento categoria, 
                 LocalDateTime dataHora, String descricao) {
        this.id = contadorId++;
        this.nome = nome;
        this.endereco = endereco;
        this.categoria = categoria;
        this.dataHora = dataHora;
        this.descricao = descricao;
        this.participantes = new ArrayList<>();
    }

    // Getters e Setters
    public int getId() { return id; }
    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }
    public String getEndereco() { return endereco; }
    public void setEndereco(String endereco) { this.endereco = endereco; }
    public CategoriaEvento getCategoria() { return categoria; }
    public void setCategoria(CategoriaEvento categoria) { this.categoria = categoria; }
    public LocalDateTime getDataHora() { return dataHora; }
    public void setDataHora(LocalDateTime dataHora) { this.dataHora = dataHora; }
    public String getDescricao() { return descricao; }
    public void setDescricao(String descricao) { this.descricao = descricao; }
    public List<Usuario> getParticipantes() { return participantes; }

    public void adicionarParticipante(Usuario usuario) {
        if (!participantes.contains(usuario)) {
            participantes.add(usuario);
        }
    }

    public void removerParticipante(Usuario usuario) {
        participantes.remove(usuario);
    }

    public boolean isOcorrendoAgora() {
        LocalDateTime agora = LocalDateTime.now();
        return !dataHora.isBefore(agora) && !dataHora.isAfter(agora.plusHours(3));
    }

    public boolean isPassado() {
        return dataHora.isBefore(LocalDateTime.now());
    }

    public boolean isFuturo() {
        return dataHora.isAfter(LocalDateTime.now());
    }

    @Override
    public String toString() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");
        return String.format("ID: %d | %s - %s | %s | %s", 
                id, nome, categoria.getDescricao(), dataHora.format(formatter), endereco);
    }
}
