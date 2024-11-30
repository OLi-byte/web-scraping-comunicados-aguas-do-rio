# Comunicados Águas do Rio

Um projeto para coletar, filtrar e enviar comunicados sobre abastecimento de água da Águas do Rio.

Este é um projeto automatizado que coleta e envia por e-mail os comunicados de uma página específica da Águas do Rio. O script utiliza Selenium para realizar o scraping da página, filtra comunicados com base em palavras-chave e envia esses comunicados para um e-mail configurado. Além disso, ele armazena os resultados em um arquivo JSON e garante que comunicados com mais de 10 dias sejam removidos.

## Funcionalidades

- Coleta comunicados de um site específico da Águas do Rio.
- Filtra os comunicados com base em palavras-chave configuráveis.
- Verifica se o comunicado já foi enviado anteriormente para evitar repetições.
- Salva os resultados em um arquivo JSON.
- Envia os comunicados por e-mail.
- Remove comunicados com mais de 10 dias do arquivo JSON.

## Finalidade

Este projeto visa ajudar pessoas que têm dificuldade em acompanhar as últimas notícias sobre o abastecimento de água na região onde moram, na cidade do Rio de Janeiro. Em 30/11/2024, uma falta de água generalizada afeta diversas áreas da cidade, e, infelizmente, não é a primeira vez nos últimos meses. Ser notificado rapidamente é essencial para que a população possa economizar água.

## Requisitos

Antes de executar o projeto, você precisa garantir que as seguintes dependências estão instaladas:

1. Python 3.x
2. pip

### Dependências

Este projeto usa as seguintes bibliotecas:

- selenium
- webdriver-manager

Você pode instalar todas as dependências executando o seguinte comando:

`pip install -r requirements.txt`

## Criando o arquivo `.env`

O arquivo `.env` deve ser criado na raiz do seu projeto. Nele, você deve adicionar as variáveis de ambiente necessárias para a execução do script.

Exemplo de conteúdo para o arquivo `.env`:

```env
KEYWORDS="Grande Tijuca,Tijuca,Vila Isabel,Capital"
EMAIL_RECEIVER=seuemail@example.com
EMAIL_USER=seuemail@example.com
EMAIL_PASSWORD=sua_senha
```

## E-mail para envio dos comunicados

O e-mail usado para enviar os comunicados precisa ser configurado. Para usar o Gmail, é necessário gerar uma senha de app nas configurações de segurança da sua conta Google.

Para gerar a senha de app:

1. Acesse [Gerenciar sua Conta Google](https://myaccount.google.com/).
2. No menu "Segurança", ative a verificação em 2 etapas (se ainda não estiver ativada).
3. Em "Senhas de app", gere uma nova senha de app para o seu projeto.
4. Use essa senha no campo `EMAIL_PASSWORD`.

## Como executar o projeto

Após configurar o arquivo `.env` com suas variáveis, execute o script com o seguinte comando:

```bash
python main.py
```

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
