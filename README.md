# 🍲 Django Recipes

Este projeto foi criado durante o curso de Django Web Framework e Django Rest Framework de Luiz Otávio Miranda, adquirido na Udemy.
O Projeto Fullstack consiste em uma plataforma que exibe receitas cadastradas pelos usuários registrados na API.


## ✅ Ajustes e melhorias

Apesar de seguir a ideia básica do projeto proposto no curso, algumas features foram criadas para melhoria do projeto e novas atualizações estão em andamento. 
Veja abaixo o que foi adicionado e as próximas alterações que estão em desenvolvimento:


 - [X] Criar banco de dados no Postgres - substituir SQLite
 - [X] Makefile com snippets de comandos mais usados
 - [X] Poetry para gerenciamento de dependências
 - [X] Alteração no Design do Dashboard
 - [ ] Docker
 - [ ] CI/CD Pipeline Github Actions


## 📝 Pré-requisitos

Para que possa gerenciar as dependências adequadamente, recomenda-se a instalação do Poetry:



## 🛠️ Rodando o projeto localmente

1. Clone o repositório:


```
https://github.com/deb-gama/django_recipes.git
```
2. Ative o ambiente virtual do Poetry:

```shell
make poetry
```

3. Instale as dependências:

```
make install
```

4. Rode um servidor de desenvolvimentoz  local:

```
make run
```

> ### ⚠️ Importante
> 
> Django Recipes deve está agora rodando e pode ser acessado em http://localhost:8000/