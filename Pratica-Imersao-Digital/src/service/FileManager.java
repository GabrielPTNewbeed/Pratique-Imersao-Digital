// src/main/java/br/com/yourevent/service/FileManager.java
package br.com.yourevent.service;

import br.com.yourevent.model.Evento;
import br.com.yourevent.model.CategoriaEvento;
import java.io.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

public class FileManager {
    private static final String ARQUIVO_EVENTOS = "events.data";
    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");

    public static void salvarEventos(List<Evento> eventos) {
        try (PrintWriter writer = new PrintWriter(new FileWriter(ARQUIVO_EVENTOS))) {
            for (Evento evento : eventos) {
                writer.println(serializarEvento(evento));
            }
        } catch (IOException e) {
            System.out.println("Erro ao salvar eventos: " + e.getMessage());
        }
    }
    public static void salvarUsuarios(List<Usuario> usuarios) {
    try (PrintWriter writer = new PrintWriter(new FileWriter("users.data"))) {
        for (Usuario usuario : usuarios) {
            writer.println(serializarUsuario(usuario));
        }
    } catch (IOException e) {
        System.out.println("Erro ao salvar usuários: " + e.getMessage());
    }
}
private static void salvarUltimoId() {
    try (PrintWriter writer = new PrintWriter(new FileWriter("lastid.data"))) {
        writer.println(Evento.getContadorId());
    } catch (IOException e) {
        System.out.println("Erro ao salvar último ID: " + e.getMessage());
    }
}

private static void carregarUltimoId() {
    File arquivo = new File("lastid.data");
    if (arquivo.exists()) {
        try (BufferedReader reader = new BufferedReader(new FileReader(arquivo))) {
            String linha = reader.readLine();
            if (linha != null) {
                Evento.setContadorId(Integer.parseInt(linha));
            }
        } catch (IOException e) {
            System.out.println("Erro ao carregar último ID: " + e.getMessage());
        }
    }
}

public static List<Usuario> carregarUsuarios() {
    List<Usuario> usuarios = new ArrayList<>();
    // Implementação similar à de eventos
}
    public static List<Evento> carregarEventos() {
        List<Evento> eventos = new ArrayList<>();
        File arquivo = new File(ARQUIVO_EVENTOS);
        
        if (!arquivo.exists()) {
            return eventos;
        }

        try (BufferedReader reader = new BufferedReader(new FileReader(ARQUIVO_EVENTOS))) {
            String linha;
            while ((linha = reader.readLine()) != null) {
                Evento evento = desserializarEvento(linha);
                if (evento != null) {
                    eventos.add(evento);
                }
            }
        } catch (IOException e) {
            System.out.println("Erro ao carregar eventos: " + e.getMessage());
        }
        return eventos;
    }

    private static String serializarEvento(Evento evento) {
        return String.format("%d;%s;%s;%s;%s;%s",
                evento.getId(),
                evento.getNome(),
                evento.getEndereco(),
                evento.getCategoria().name(),
                evento.getDataHora().format(formatter),
                evento.getDescricao().replace(";", ","));
    }

    private static Evento desserializarEvento(String linha) {
        try {
            String[] partes = linha.split(";", 6);
            if (partes.length < 6) return null;

            int id = Integer.parseInt(partes[0]);
            String nome = partes[1];
            String endereco = partes[2];
            CategoriaEvento categoria = CategoriaEvento.valueOf(partes[3]);
            LocalDateTime dataHora = LocalDateTime.parse(partes[4], formatter);
            String descricao = partes[5];

            Evento evento = new Evento(nome, endereco, categoria, dataHora, descricao);
            // Mantemos o ID original
            return evento;
        } catch (Exception e) {
            System.out.println("Erro ao desserializar evento: " + e.getMessage());
            return null;
        }
    }
}