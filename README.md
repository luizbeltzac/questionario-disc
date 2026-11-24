# Questionário DISC – versão online

Questionário de perfil comportamental (DISC) do time de Projetos Estratégicos.
Roda na Vercel como aplicação Python (WSGI): `app.py` é o ponto de entrada; páginas em `public/` e regras em `disc/`.
**Nada é gravado na plataforma**: o resultado vai por e-mail.

| Quem | Recebe |
|---|---|
| Participante | PDF do resultado (e pode baixar na tela final) |
| Líder (`LEADER_EMAIL`) | PDF + `.json` para importar no programa Gestão do Time |

## Como usar
1. Abra `https://<seu-endereco>/admin.html`, informe a senha de administrador,
   o nome e o e-mail do liderado e clique em **Gerar link**.
2. Envie o link para a pessoa. O nome e o e-mail vêm travados; o link expira
   no prazo escolhido.

## Publicar na Vercel (uma vez)
1. Crie a conta em vercel.com entrando com o GitHub.
2. **Add New → Project →** importe o repositório `questionario-disc`
   (a Vercel detecta Python sozinha; não precisa mudar build nem output).
3. Em **Settings → Environment Variables** cadastre as variáveis do
   `.env.example` (APP_SECRET, ADMIN_PASSWORD, LEADER_EMAIL, SMTP_*).
   Use uma **senha de aplicativo** da Zoho em SMTP_PASSWORD.
4. **Deployments → Redeploy** para aplicar as variáveis.
5. Teste: gere um convite para você mesmo em `/admin.html` e responda.

Cada alteração enviada ao GitHub (branch `main`) publica uma nova versão
automaticamente.

## Teste local
```
pip install reportlab
copy .env.example .env   (preencha; use DRY_RUN=1 para não enviar e-mail)
python dev_local.py      ->  http://127.0.0.1:8000/admin.html
```

## Estrutura
- `app.py` – ponto de entrada e rotas
- `disc/_questionario.py` – frases e pontuação
- `disc/_perfis.py` – textos de cada perfil
- `disc/_pdf_relatorio.py` – relatório em PDF
- `disc/_email_envio.py` – envio SMTP (mesma lógica do relatório do Portfólio)
- `disc/_servico.py` – convites assinados, montagem do questionário e envio
- `public/index.html` – questionário · `public/admin.html` – convites

## Segurança
- Senhas e segredos só nas variáveis de ambiente da Vercel, nunca no código.
- Links de convite assinados com `APP_SECRET`: trocar o APP_SECRET invalida
  todos os links já enviados.
- Só e-mails do domínio `ALLOWED_EMAIL_DOMAIN` recebem convite.
