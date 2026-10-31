🏋️ GymFlow
Sistema web para gerenciamento e visualização da ocupação de
academias, desenvolvido como projeto acadêmico da disciplina PJI240
-- Projeto Integrador em Computação II.

O GymFlow permite autenticar usuários, controlar permissões por perfil,
registrar entradas e saídas da academia, consultar equipamentos e
acompanhar a ocupação por meio de uma interface web integrada a uma API
REST.
Situação em 31/10/2026: funcionalidades principais implementadas e
validadas localmente. Backend com 115 testes aprovados; frontend
aprovado no ESLint e no build de produção. 

🎓 Contexto acadêmico
  Item            Informação
  Projeto         GymFlow
Disciplina      PJI240 -- Projeto Integrador em Computação II
Carga horária   80 horas
Finalidade      Projeto acadêmico

O projeto aplica conhecimentos de desenvolvimento web, APIs, banco de
dados, JavaScript, autenticação, testes automatizados, controle de
versão, organização de software e trabalho colaborativo.

🎯 Objetivo do projeto
O GymFlow foi concebido para auxiliar academias no acompanhamento da
movimentação de pessoas e da ocupação atual do estabelecimento.

Objetivos principais
- Cadastrar e gerenciar usuários conforme o perfil de acesso.
- Autenticar usuários por meio de credenciais.
- Registrar check-ins e check-outs.
- Identificar usuários com permanência ativa.
- Calcular a ocupação atual da academia.
- Consultar e gerenciar equipamentos conforme as permissões.
- Disponibilizar informações por meio de uma API REST.
- Apresentar indicadores em uma interface web.

📋 Regras de negócio
Esta seção descreve as regras implementadas no backend e refletidas,
quando aplicável, na interface. As permissões do backend são a camada
efetiva de autorização; ocultar ou bloquear uma página no frontend não
substitui essa validação.

1. Perfis de usuário
O sistema trabalha com quatro perfis:
- ADMIN: administração dos usuários e equipamentos e acesso aos
  indicadores completos.
- RECEPCAO: cadastro de alunos, consulta de equipamentos,
  acompanhamento dos check-ins e acesso aos indicadores completos.
- PROFESSOR: consulta de equipamentos, consulta do próprio
  histórico de check-ins e acesso aos indicadores completos.
- ALUNO: consulta da ocupação atual e do próprio histórico de
  check-ins.

2. Cadastro e gerenciamento de usuários
- O cadastro público cria usuários com perfil ALUNO.
- A RECEPCAO pode cadastrar alunos por meio da funcionalidade
  específica de cadastro.
- O endpoint administrativo permite ao ADMIN criar usuários com perfis
  permitidos pela validação da aplicação; a criação de outro ADMIN é
  bloqueada.
- As operações administrativas de listagem, consulta por
  identificador, atualização e exclusão de usuários são restritas ao
  ADMIN.
- O usuário autenticado pode consultar os próprios dados por meio da
  rota /users/me.

3. Controle de acesso por funcionalidade
  Funcionalidade                              ADMIN   RECEPCAO   PROFESSOR   ALUNO
Dashboard completo                            Sim      Sim         Sim       Não
Consultar ocupação atual                      Sim      Sim         Sim       Sim
Gerenciar usuários                            Sim      Não         Não       Não
Cadastrar alunos pela tela específica         Não      Sim         Não       Não
Consultar equipamentos                        Sim      Sim         Sim       Não
Criar, editar e excluir equipamentos          Sim      Não         Não       Não
Consultar histórico completo de check-ins     Sim      Sim         Não       Não
Consultar próprio histórico de check-ins      Sim      Sim         Sim       Sim
Registrar check-in próprio                    Sim      Sim         Sim       Sim

Observações:
- A tabela representa as permissões funcionais implementadas. Algumas
  operações administrativas também possuem regras específicas no
  backend.
- ADMIN e RECEPCAO podem realizar check-out de outros usuários; ALUNO
  e PROFESSOR só podem realizar check-out dos próprios registros.
- O cadastro público cria ALUNO. A tela de cadastro de alunos é
  restrita à RECEPCAO.
- A interface não oferece gerenciamento geral de usuários para
  RECEPCAO, PROFESSOR ou ALUNO.

4. Check-in e check-out
- O check-in é associado ao usuário autenticado; o cliente não escolhe
  livremente outro usuário para registrar a própria entrada.
- Um usuário não pode manter dois check-ins ativos simultaneamente.
- O check-out registra o encerramento da permanência.
- ALUNO e PROFESSOR podem encerrar somente seus próprios check-ins.
- ADMIN e RECEPCAO podem encerrar check-ins de outros usuários.
- ADMIN e RECEPCAO podem consultar o histórico completo.
- PROFESSOR e ALUNO consultam somente o próprio histórico.

5. Equipamentos
- O patrimônio/identificador do equipamento deve ser único.
- O cadastro de equipamento inicia com o status padrão ATIVO,
  conforme a implementação do serviço.
- ADMIN pode cadastrar, consultar, editar e excluir equipamentos.
- RECEPCAO e PROFESSOR podem consultar equipamentos.
- ALUNO não possui acesso à funcionalidade de equipamentos.

6. Ocupação e Dashboard
- A ocupação atual corresponde à quantidade de registros de check-in
  que ainda não possuem check-out.
- A rota /dashboard/ocupacao disponibiliza somente a quantidade de
  pessoas presentes, sem expor nomes ou histórico individual.
- O Dashboard completo apresenta ocupação atual, check-ins do dia,
  check-outs do dia, tempo médio de permanência e últimos check-ins.
- ADMIN, RECEPCAO e PROFESSOR podem consultar o Dashboard completo.
- ALUNO pode consultar somente a ocupação atual.

🏗️ Arquitetura
O GymFlow possui arquitetura separada em frontend, backend e banco de
dados.
┌────────────────────┐
│       USUÁRIO      │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│      FRONTEND      │
│    React + Vite    │
└─────────┬──────────┘
          │ HTTP / REST
          ▼
┌────────────────────┐
│      BACKEND       │
│   FastAPI + Python │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│     SQLAlchemy     │
│        ORM         │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│       SQLite       │
└────────────────────┘

Organização do backend
O backend segue uma separação por responsabilidades:
- routes: definição dos endpoints HTTP.
- schemas: validação e estrutura dos dados de entrada e saída.
- models: modelos persistidos no banco.
- crud: operações de acesso a dados.
- services: regras e operações de negócio.
- core: autenticação, configuração, dependências, segurança e
  infraestrutura.


🧰 Stack tecnológica
Backend
Tecnologia                      Versão declarada Finalidade
Python                3.14.3 (ambiente validado) Linguagem principal
FastAPI                                  0.136.3 Framework da API
Uvicorn                                   0.49.0 Servidor ASGI
SQLAlchemy                                2.0.50 ORM e acesso ao banco
python-dotenv                              1.2.2 Variáveis de ambiente
pydantic-settings                         2.12.0 Configurações
python-jose                                3.5.0 JWT
Passlib                                    1.7.4 Hash de senhas
bcrypt                                     4.0.1 Hash de senhas
pytest                                     8.4.2 Testes automatizados
pytest-cov                                 7.0.0 Cobertura de testes
httpx                                     0.28.1 Cliente HTTP para testes

As versões das dependências do backend estão registradas em
backend/requirements.txt.
Frontend
Tecnologia              Versão declarada no package.json Finalidade
React                                             ^19.2.7 Interface
React DOM                                         ^19.2.7 Renderização
Vite                                               ^8.1.1 Desenvolvimento e build
Axios                                             ^1.18.1 Comunicação HTTP
React Router DOM                                  ^7.18.1 Navegação e rotas
React Hook Form                                   ^7.84.0 Formulários
Zod                                                ^4.4.3 Validação
@hookform/resolvers                                ^5.7.1 Integração de validação
React Hot Toast                                    ^2.6.0 Notificações
React Modal                                       ^3.16.3 Modais
Lucide React                                      ^1.27.0 Ícones
Prop Types                                        ^15.8.1 Validação de propriedades

Ferramentas de desenvolvimento
Ferramenta           Finalidade
Git                  Controle de versão
GitHub               Repositório remoto e colaboração
Git Bash             Terminal utilizado no ambiente Windows
Visual Studio Code   Editor
npm                  Gerenciamento de dependências
ESLint               Análise estática do frontend
Swagger / OpenAPI    Documentação e exploração da API

🗄️ Banco de dados
O banco utilizado no desenvolvimento é o SQLite, acessado por meio
do SQLAlchemy.

Arquivos locais previstos:
backend/gymflow.db
backend/test_gymflow.db
O primeiro é utilizado pela aplicação local e o segundo pode ser
utilizado no ambiente de testes, conforme a configuração do projeto.

Bancos locais e arquivos de backup não devem ser versionados. O
.gitignore contempla extensões como *.db e *.sqlite3; confira
também as regras do repositório antes de adicionar arquivos.

🔐 Autenticação e segurança
O sistema utiliza autenticação baseada em JWT (JSON Web Token).

Tecnologias relacionadas:
python-jose
Passlib
bcrypt
Fluxo simplificado:
Usuário
   │
   ▼
Login
   │
   ▼
FastAPI valida as credenciais
   │
   ▼
Token JWT
   │
   ▼
Frontend
   │
   ▼
Requisições autenticadas

Princípios adotados:
- Senhas não devem ser armazenadas em texto puro.
- Rotas privadas exigem autenticação.
- Rotas restritas verificam também o perfil autorizado.
- Informações sensíveis devem permanecer em variáveis de ambiente.
- Arquivos .env, tokens, senhas e credenciais não devem ser enviados
  ao Git.

O controle de acesso é aplicado no backend. O frontend também protege as
rotas e a navegação, proporcionando uma experiência coerente com o
perfil autenticado.

🔌 API REST
O backend utiliza FastAPI para disponibilizar os recursos do sistema.

Durante o desenvolvimento local:
API:       http://127.0.0.1:8000
Swagger:   http://127.0.0.1:8000/docs
OpenAPI:   http://127.0.0.1:8000/openapi.json

Principais grupos de endpoints
  Recurso                 Exemplos de rotas       Finalidade
  Autenticação            /auth/login           Autenticação e emissão
de token

  Usuários                /users/, /users/me  Cadastro e consulta de
usuários

  Usuários                /users/reception,     Cadastro conforme
/users/admin          perfil autorizado

  Equipamentos            /equipments/          Consulta e
gerenciamento de
equipamentos

  Check-ins               /checkins/            Registro e consulta de
movimentações

  Check-ins               /checkins/ativos,     Consulta de registros
/checkins/me          ativos e histórico
próprio

  Dashboard               /dashboard/           Indicadores completos
Dashboard               /dashboard/ocupacao   Ocupação atual sem
dados pessoais

Os métodos HTTP e os requisitos de autenticação/perfil de cada endpoint
podem ser consultados na documentação Swagger.

⚛️ Frontend
O frontend foi desenvolvido com React e Vite.

Responsabilidades principais:
- Apresentar as telas de login e Dashboard.
- Permitir consulta e gerenciamento de usuários conforme o perfil.
- Permitir cadastro de alunos pela RECEPCAO.
- Apresentar consulta e gerenciamento de equipamentos conforme as
  permissões.
- Registrar check-ins e check-outs.
- Exibir dados retornados pela API.
- Proteger rotas e redirecionar usuários sem autorização.

Durante o desenvolvimento, a aplicação é disponibilizada normalmente em:
http://localhost:5173

O Axios realiza a comunicação HTTP com a API.
Formulários e validação

O projeto utiliza:
React Hook Form
Zod
@hookform/resolvers

Essa combinação organiza o gerenciamento dos formulários e a validação
dos dados no frontend. As validações de negócio e de autorização também
são realizadas no backend.
Rotas
O gerenciamento de navegação utiliza react-router-dom.

As rotas privadas exigem autenticação. As rotas com restrição de perfil
verificam os papéis permitidos antes de exibir a página.

🧪 Testes e qualidade
Testes automatizados do backend
O backend possui uma suíte de testes com pytest, pytest-cov e
httpx.

Arquivos de teste existentes no projeto:
backend/tests/
├── test_auth.py
├── test_checkins.py
├── test_core_auth.py
├── test_dashboard.py
├── test_database.py
├── test_dependencies.py
├── test_exception_handlers.py
├── test_exceptions.py
├── test_main.py
├── test_models_checkin.py
├── test_models_user.py
├── test_openapi.py
├── test_user_crud.py
├── test_user_service.py
└── test_users.py
Os testes abrangem autenticação, autorização, check-ins, Dashboard,
banco de dados, dependências, tratamento de exceções, modelos, OpenAPI,
CRUD, serviços e endpoints.

Resultado registrado em 31/10/2026:
115 passed
4 warnings
Os quatro avisos não impediram a aprovação da suíte. Foram identificadas
mensagens de depreciação relacionadas a bibliotecas e constantes
utilizadas no ambiente de testes.
Validação do frontend
ESLint --- 31/10/2026
npm run lint
Resultado: aprovado, sem erros ou avisos.
Build de produção --- 31/10/2026
npm run build
Resultado: build concluído com sucesso.
Validação manual dos perfis
Em 31/10/2026, foram realizados testes manuais de navegação e permissões
com os quatro perfis:

  Perfil                              Resultado
  ADMIN                               Dashboard completo e gerenciamento:
OK

  RECEPCAO                            Dashboard completo, cadastro de
alunos e consulta de equipamentos:
OK

  PROFESSOR                           Dashboard completo e consulta de
equipamentos: OK
ALUNO                               Ocupação atual e histórico
individual: OK

Também foram verificadas tentativas de acesso a páginas restritas por
meio da navegação direta.

Executando os testes
No terminal, entre na pasta do backend:
cd backend
Ative o ambiente virtual no Git Bash para Windows:
source venv/Scripts/activate
Execute a suíte:
pytest
Para executar com cobertura:
pytest --cov=app
Validando o frontend
Em outro terminal, entre na pasta do frontend:
cd frontend
Execute o ESLint:
npm run lint
Gere o build de produção:
npm run build
Para visualizar localmente o build:
npm run preview

📁 Estrutura do projeto

Estrutura principal do repositório:
gymflow/
├── .gitignore
├── README.md
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── crud/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   ├── constants/
    │   ├── contexts/
    │   ├── layouts/
    │   ├── pages/
    │   ├── routes/
    │   └── services/
    ├── index.html
    ├── package.json
    ├── package-lock.json
    ├── vite.config.js
    └── eslint.config.js

A estrutura pode evoluir conforme a manutenção e as próximas versões do
projeto.

⚙️ Requisitos para desenvolvimento
Para clonar e executar o projeto, recomenda-se ter instalado:
- Git;
- Python 3.14.3 (versão utilizada na validação registrada);
- Node.js;
- npm;
- Visual Studio Code ou outro editor de código.
A versão do Node.js utilizada pela equipe não foi fixada nesta
documentação. Para reproduzir o ambiente com maior precisão, consulte
também o package-lock.json.

📥 Clonando o projeto
Clone o repositório:
git clone <URL_DO_REPOSITORIO>
Entre na pasta:
cd gymflow
Substitua <URL_DO_REPOSITORIO> pelo endereço real do repositório
Git.

🐍 Configurando o backend
Entre na pasta:
cd backend
Crie o ambiente virtual:
python -m venv venv
Ative o ambiente no Git Bash:
source venv/Scripts/activate
Instale as dependências:
pip install -r requirements.txt

🔐 Configurando as variáveis de ambiente
O projeto possui um arquivo de referência:
backend/.env.example
Crie o arquivo local backend/.env com as configurações necessárias,
seguindo os nomes e orientações presentes no .env.example.

Não publique o .env no GitHub. O arquivo local deve permanecer
protegido pelo .gitignore.

▶️ Executando o backend
Com o ambiente virtual ativado e estando dentro de backend:
uvicorn app.main:app --reload
A API estará disponível em:
http://127.0.0.1:8000
A documentação Swagger estará em:
http://127.0.0.1:8000/docs

⚛️ Configurando o frontend
Abra outro terminal e, a partir da raiz do projeto, entre na pasta:
cd frontend
Instale as dependências:
npm install

▶️ Executando o frontend
Na pasta frontend, execute:
npm run dev
A aplicação estará disponível normalmente em:
http://localhost:5173

🚀 Executando o projeto completo
Mantenha dois terminais abertos.
Terminal 1 --- Backend
A partir da raiz do projeto:
cd gymflow/backend
source venv/Scripts/activate
uvicorn app.main:app --reload
Terminal 2 --- Frontend
A partir da raiz do projeto:
cd gymflow/frontend
npm install
npm run dev
Depois, acesse:
http://localhost:5173

🌿 Git e estratégia de branches
O projeto utiliza Git para controle de versão e GitHub como plataforma
de repositório remoto e colaboração.

Branches utilizadas durante o desenvolvimento incluem:
develop
feature/checkin
feature/frontend
O fluxo recomendado é desenvolver em branches específicas e integrar
alterações à branch develop após revisão.
develop
   │
   ├── feature/nova-funcionalidade
   │
   ├── feature/correcao
   │
   └── Pull Request
          │
          ▼
       Revisão
          │
          ▼
       develop

Cuidados ao adicionar arquivos
Antes de criar um commit:
git status --short
Adicione somente os arquivos relacionados à tarefa:
git add caminho/do/arquivo
Evite adicionar indiscriminadamente arquivos locais, bancos de dados,
backups, arquivos de ambiente ou artefatos de build.
Convenção de commits
Recomenda-se utilizar mensagens padronizadas:

  Tipo                  Exemplo
  Nova funcionalidade   feat: adiciona dashboard de ocupacao
Correção              fix: corrige validacao do login
Documentação          docs: atualiza README
Refatoração           refactor: reorganiza servico de usuarios
Testes                test: adiciona testes para check-in

🚫 Arquivos que não devem ser versionados
O .gitignore deve impedir o versionamento de arquivos gerados
localmente ou que contenham informações sensíveis.

Exemplos:
venv/
__pycache__/
.pytest_cache/
.coverage
htmlcov/
*.db
*.sqlite3
.env
node_modules/
dist/
.vscode/
.idea/
*.log

Nunca faça commit de:
- Senhas;
- Tokens;
- Chaves secretas;
- Credenciais;
- Arquivos .env;
- Dados pessoais reais;
- Banco de dados local ou backups;
- node_modules;
- Ambientes virtuais.

🔒 Segurança

Informações sensíveis devem permanecer fora do código-fonte.
- Utilize backend/.env para configurações locais.
- Utilize backend/.env.example para documentar as variáveis
  necessárias sem incluir segredos.
- O .env.example pode ser versionado.
- O .env não deve ser versionado.
- Não compartilhe tokens JWT ou credenciais em capturas de tela,
  relatórios ou commits.
- Utilize dados fictícios nos ambientes de demonstração e teste.

📋 Checklist de preparação do ambiente
- [ ] Instalar Git.
- [ ] Instalar Python.
- [ ] Instalar Node.js e npm.
- [ ] Clonar o repositório.
- [ ] Configurar o ambiente virtual do backend.
- [ ] Instalar requirements.txt.
- [ ] Configurar backend/.env.
- [ ] Instalar dependências do frontend.
- [ ] Executar o backend.
- [ ] Executar o frontend.
- [ ] Acessar a aplicação.
- [ ] Consultar a documentação /docs.
- [ ] Executar os testes automatizados.
- [ ] Executar o ESLint.
- [ ] Gerar o build do frontend.

🧪 Checklist antes de integrar alterações
Backend
- [ ] API inicia corretamente.
- [ ] Testes executados.
- [ ] Testes aprovados.
- [ ] Nenhuma credencial foi adicionada.
- [ ] Logs de debug desnecessários foram removidos.
Frontend
- [ ] Aplicação inicia.
- [ ] npm run lint executado.
- [ ] Build executado.
- [ ] Funcionalidade testada.
- [ ] Console sem erros inesperados.
Git
- [ ] Branch correta.
- [ ] Arquivos revisados com git status.
- [ ] Nenhum arquivo sensível incluído.
- [ ] Commit organizado.
- [ ] Pull Request criado quando aplicável.

📊 Fluxo de ocupação
A regra principal do GymFlow utiliza os registros de entrada e saída dos
usuários.
          CHECK-IN
              │
              ▼
      ┌─────────────────┐
      │ Check-in ativo  │
      │ sem check-out   │
      └────────┬────────┘
               │
               ▼
       Conta na ocupação
               │
               ▼
          CHECK-OUT
               │
               ▼
      ┌─────────────────┐
      │ Permanência     │
      │ encerrada       │
      └─────────────────┘

A ocupação representa a quantidade de registros de check-in sem
check-out correspondente.

📈 Possíveis evoluções
As funcionalidades abaixo são possibilidades para versões futuras e não
devem ser consideradas entregues nesta versão, salvo implementação
posterior comprovada:

- Histórico de ocupação por período.
- Gráficos de movimentação.
- Identificação de horários de maior movimento.
- Controle de capacidade máxima da academia.
- Alertas de lotação.
- Relatórios gerenciais.
- Gestão de múltiplas academias.
- Integração com outros serviços.
- Melhorias na interface administrativa para gerenciamento de perfis.
- Ampliação de recursos de auditoria e monitoramento.

Implantação em nuvem
A implantação em nuvem está prevista no escopo acadêmico e permanece sob
responsabilidade de outro integrante do grupo. O status, a URL e as
evidências de publicação devem ser adicionados a esta documentação após
a conclusão e validação do deploy.

O ambiente descrito neste README é o ambiente de desenvolvimento local
com SQLite.

🏃 Sprints e situação do projeto
O desenvolvimento foi conduzido de forma incremental, com organização de
atividades por Sprints e controle de versão com Git.
Situação em 31/10/2026
Implementação das funcionalidades
              │
              ▼
Autenticação e permissões por perfil
              │
              ▼
Testes automatizados do backend
              │
              ▼
Validação manual dos quatro perfis
              │
              ▼
ESLint e build do frontend
              │
              ▼
Documentação e evidências
              │
              ▼
Preparação da entrega acadêmica
Checkpoint
  Item                                Situação
  Projeto                             GymFlow

  Disciplina                          PJI240 -- Projeto Integrador em
Computação II

  Data de referência                  31/10/2026

  Backend                             115 testes aprovados

  Frontend                            ESLint aprovado

  Build                               Aprovado

  Perfis                              ADMIN, RECEPCAO, PROFESSOR e ALUNO
validados manualmente

  Branch de trabalho                  develop

  Último commit registrado nesta      5c92503
etapa                               

  Próxima atividade                   Finalização da documentação,
evidências e apresentação
Implantação em nuvem                Responsabilidade de outro
integrante; evidência pendente

📦 Resumo da stack
GYMFLOW
│
├── Frontend
│   ├── React
│   ├── Vite
│   ├── Axios
│   ├── React Router DOM
│   ├── React Hook Form
│   ├── Zod
│   └── Lucide React
│
├── Backend
│   ├── Python
│   ├── FastAPI
│   ├── Uvicorn
│   ├── SQLAlchemy
│   ├── Pydantic Settings
│   ├── python-jose
│   ├── Passlib
│   └── bcrypt
│
├── Banco de dados
│   └── SQLite
│
├── Testes
│   ├── pytest
│   ├── pytest-cov
│   └── httpx
│
├── Qualidade
│   └── ESLint
│
└── Controle de versão
    ├── Git
    └── GitHub
👤 Autoria
Thamyres Lima

Projeto desenvolvido para fins acadêmicos no âmbito da disciplina:

PJI240 -- Projeto Integrador em Computação II.
📄 Licença
A licença de distribuição do projeto deve ser formalizada em um arquivo
LICENSE no repositório. A versão anterior deste README mencionava MIT,
mas a existência do arquivo de licença não foi confirmada durante esta
revisão.