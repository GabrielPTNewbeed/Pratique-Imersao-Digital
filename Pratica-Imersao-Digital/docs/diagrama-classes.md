# Diagrama de Classes

## Classes Principais

### Usuario
- id: int
- nome: String
- email: String
- telefone: String
- senha: String
- eventosParticipando: List<Evento>

### Evento
- id: int
- nome: String
- endereço: String
- categoria: CategoriaEvento
- dataHora: LocalDateTime
- descricao: String
- participantes: List<Usuario>

### CategoriaEvento (Enum)
- FESTA
- ESPORTIVO
- SHOW
- CULTURAL
- GASTRONOMICO
- EDUCACIONAL

### GerenciadorEventos
- eventos: List<Evento>
- usuarios: List<Usuario>
- usuarioLogado: Usuario

### FileManager
- arquivoEventos: String = "events.data"