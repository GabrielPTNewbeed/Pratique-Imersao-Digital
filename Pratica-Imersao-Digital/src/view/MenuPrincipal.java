// src/main/java/br/com/yourevent/view/MenuPrincipal.java
package br.com.yourevent.view;

import br.com.yourevent.service.GerenciadorEventos;
import br.com.yourevent.model.Evento;
import br.com.yourevent.model.Usuario;
import br.com.yourevent.model.CategoriaEvento;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.List;
import java.util.Scanner;

public class MenuPrincipal {
    private GerenciadorEventos gerenciador;
    private Scanner scanner;

    public MenuPrincipal() {
        this.gerenciador = new GerenciadorEventos();
        this.scanner = new Scanner(System.in);
    }

    public void executar() {
        while (true) {
            if (!gerenciador.isUsuarioLogado()) {
                exibirMenuLogin();
            } else {
                exibirMenuPrincipal();
            }
        }
    }

    private void exibirMenuLogin() {
        System.out.println("\n=== SISTEMA DE EVENTOS DA CIDADE ===");
        System.out.println("1. Fazer Login");
        System.out.println("2. Cadastrar Usuário");
        System.out.println("3. Sair");
        System.out.print("Escolha uma opção: ");

        int opcao = scanner.nextInt();
        scanner.nextLine(); // Limpar buffer

        switch (opcao) {
            case 1:
                fazerLogin();
                break;
            case 2:
                cadastrarUsuario();
                break;
            case 3:
                System.out.println("Saindo do sistema...");
                System.exit(0);
                break;
            default:
                System.out.println("Opção inválida!");
        }
    }

    private void fazerLogin() {
        System.out.print("Email: ");
        String email = scanner.nextLine();
        System.out.print("Senha: ");
        String senha = scanner.nextLine();

        if (gerenciador.fazerLogin(email, senha)) {
            System.out.println("Login realizado com sucesso!");
        } else {
            System.out.println("Email ou senha incorretos!");
        }
    }

    private void cadastrarUsuario() {
        System.out.println("\n=== CADASTRO DE USUÁRIO ===");
        System.out.print("Nome: ");
        String nome = scanner.nextLine();
        System.out.print("Email: ");
        String email = scanner.nextLine();
        System.out.print("Telefone: ");
        String telefone = scanner.nextLine();
        System.out.print("Senha: ");
        String senha = scanner.nextLine();

        Usuario usuario = new Usuario(nome, email, telefone, senha);
        gerenciador.cadastrarUsuario(usuario);
        System.out.println("Usuário cadastrado com sucesso!");
    }

    private void exibirMenuPrincipal() {
        System.out.println("\n=== MENU PRINCIPAL ===");
        System.out.println("1. Visualizar Eventos");
        System.out.println("2. Cadastrar Evento");
        System.out.println("3. Meus Eventos");
        System.out.println("4. Eventos Ocorrendo Agora");
        System.out.println("5. Sair");
        System.out.print("Escolha uma opção: ");

        int opcao = scanner.nextInt();
        scanner.nextLine(); // Limpar buffer

        switch (opcao) {
            case 1:
                visualizarEventos();
                break;
            case 2:
                cadastrarEvento();
                break;
            case 3:
                visualizarMeusEventos();
                break;
            case 4:
                visualizarEventosOcorrendoAgora();
                break;
            case 5:
                gerenciador.fazerLogout();
                System.out.println("Logout realizado!");
                break;
            default:
                System.out.println("Opção inválida!");
        }
    }

    private void visualizarEventos() {
        System.out.println("\n=== EVENTOS DISPONÍVEIS ===");
        
        List<Evento> eventosFuturos = gerenciador.getEventosFuturos();
        if (eventosFuturos.isEmpty()) {
            System.out.println("Nenhum evento futuro encontrado.");
        } else {
            System.out.println("--- Eventos Futuros ---");
            for (Evento evento : eventosFuturos) {
                System.out.println(evento);
            }
        }

        List<Evento> eventosPassados = gerenciador.getEventosPassados();
        if (!eventosPassados.isEmpty()) {
            System.out.println("\n--- Eventos Passados ---");
            for (Evento evento : eventosPassados) {
                System.out.println(evento);
            }
        }

        System.out.println("\n1. Participar de Evento");
        System.out.println("2. Voltar");
        System.out.print("Escolha uma opção: ");

        int opcao = scanner.nextInt();
        scanner.nextLine();

        if (opcao == 1) {
            participarEvento();
        }
    }

    private void participarEvento() {
        System.out.print("Digite o ID do evento que deseja participar: ");
        int eventoId = scanner.nextInt();
        scanner.nextLine();

        gerenciador.participarEvento(eventoId);
        System.out.println("Participação confirmada!");
    }

    private void cadastrarEvento() {
        System.out.println("\n=== CADASTRAR EVENTO ===");
        
        System.out.print("Nome do evento: ");
        String nome = scanner.nextLine();
        
        System.out.print("Endereço: ");
        String endereco = scanner.nextLine();
        
        System.out.println("Categorias disponíveis:");
        for (CategoriaEvento categoria : CategoriaEvento.values()) {
            System.out.println("- " + categoria.name() + " (" + categoria.getDescricao() + ")");
        }
        System.out.print("Categoria: ");
        String categoriaStr = scanner.nextLine().toUpperCase();
        
        CategoriaEvento categoria;
        try {
            categoria = CategoriaEvento.valueOf(categoriaStr);
        } catch (IllegalArgumentException e) {
            System.out.println("Categoria inválida!");
            return;
        }
        
        System.out.print("Data e Hora (dd/MM/yyyy HH:mm): ");
        String dataHoraStr = scanner.nextLine();
        
        LocalDateTime dataHora;
        try {
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");
            dataHora = LocalDateTime.parse(dataHoraStr, formatter);
        } catch (DateTimeParseException e) {
            System.out.println("Formato de data/hora inválido!");
            return;
        }
        
        System.out.print("Descrição: ");
        String descricao = scanner.nextLine();

        Evento evento = new Evento(nome, endereco, categoria, dataHora, descricao);
        gerenciador.cadastrarEvento(evento);
        System.out.println("Evento cadastrado com sucesso!");
    }

    private void visualizarMeusEventos() {
        System.out.println("\n=== MEUS EVENTOS ===");
        
        List<Evento> meusEventos = gerenciador.getEventosUsuario();
        if (meusEventos.isEmpty()) {
            System.out.println("Você não está participando de nenhum evento.");
        } else {
            for (Evento evento : meusEventos) {
                System.out.println(evento);
            }
            
            System.out.println("\n1. Cancelar Participação");
            System.out.println("2. Voltar");
            System.out.print("Escolha uma opção: ");

            int opcao = scanner.nextInt();
            scanner.nextLine();

            if (opcao == 1) {
                cancelarParticipacao();
            }
        }
    }

    private void cancelarParticipacao() {
        System.out.print("Digite o ID do evento que deseja cancelar: ");
        int eventoId = scanner.nextInt();
        scanner.nextLine();

        gerenciador.cancelarParticipacao(eventoId);
        System.out.println("Participação cancelada!");
    }

    private void visualizarEventosOcorrendoAgora() {
        System.out.println("\n=== EVENTOS OCORRENDO AGORA ===");
        
        List<Evento> eventosAgora = gerenciador.getEventosOcorrendoAgora();
        if (eventosAgora.isEmpty()) {
            System.out.println("Nenhum evento ocorrendo no momento.");
        } else {
            for (Evento evento : eventosAgora) {
                System.out.println(evento);
                System.out.println("Descrição: " + evento.getDescricao());
                System.out.println("---");
            }
        }
    }

private boolean validarEmail(String email) {
    return email.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");
}

private boolean validarTelefone(String telefone) {
    return telefone.matches("^[0-9]{10,11}$");
}
}
