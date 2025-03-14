# Dine & Dash Authentication Service

## Descrição
O serviço de autenticação do Dine & Dash é responsável por gerenciar o acesso dos utilizadores à plataforma, utilizando autenticação externa através do Auth0. Este microserviço é construído com FastAPI e segue uma arquitetura modular, permitindo fácil manutenção e escalabilidade.

## Estrutura do Projeto
```
auth-service/
├── src/
│   ├── main.py          # Ponto de entrada da aplicação
│   ├── auth/            # Módulo de autenticação
│   │   ├── __init__.py  # Inicializa o módulo de autenticação
│   │   ├── routes.py    # Define as rotas de autenticação
│   │   └── utils.py     # Funções auxiliares para autenticação
│   ├── models/          # Modelos de dados
│   │   └── user.py      # Modelo de dados do usuário
│   └── config.py        # Configurações da aplicação
├── requirements.txt      # Dependências do projeto
├── Dockerfile            # Instruções para construir a imagem Docker
├── docker-compose.yml    # Configuração para orquestração do Docker
└── README.md             # Documentação do projeto
```

## Instalação
1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd auth-service
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente necessárias no arquivo `config.py`.

## Uso
Para iniciar o serviço de autenticação, execute o seguinte comando:
```
uvicorn src.main:app --reload
```

## Funcionalidades
- **Autenticação de Usuários**: Permite login e registro de usuários utilizando Auth0.
- **Verificação de Token**: Valida tokens JWT para garantir a segurança das rotas.
- **Gerenciamento de Usuários**: Armazena e gerencia informações dos usuários.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença
Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.