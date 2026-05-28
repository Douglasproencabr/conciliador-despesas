# 🚀 Como publicar o Conciliador online (grátis)

Este guia leva **menos de 15 minutos** e não exige conhecimento técnico avançado.

---

## O que você vai precisar

- Conta no **GitHub** (gratuita) → https://github.com
- Conta no **Streamlit Cloud** (gratuita) → https://streamlit.io/cloud

---

## PASSO 1 — Criar conta no GitHub

1. Acesse https://github.com e clique em **Sign up**
2. Preencha e-mail, senha e username
3. Confirme o e-mail recebido
4. Pronto, conta criada ✅

---

## PASSO 2 — Criar o repositório no GitHub

1. Clique no botão **"+"** no canto superior direito → **New repository**
2. Preencha:
   - **Repository name:** `conciliador-despesas`
   - **Visibility:** ✅ Public *(necessário para o plano gratuito)*
   - Deixe as demais opções como estão
3. Clique em **Create repository**

---

## PASSO 3 — Enviar os arquivos para o GitHub

### Opção A — Pelo site (mais fácil)

1. Na página do repositório recém-criado, clique em **"uploading an existing file"**
2. Arraste **todos** os arquivos e pastas desta pasta para a área de upload:
   ```
   app.py
   requirements.txt
   logo_ciss.png
   services/
     __init__.py
     conciliador.py
     leitor_excel.py
     leitor_pdf.py
     leitor_pdf.py
     exportador_excel.py
   .streamlit/
     config.toml
   ```
3. Clique em **Commit changes**

> ⚠️ Atenção: a pasta `.streamlit` pode ficar oculta no Windows.
> Para vê-la: no Explorer → Exibir → marcar "Itens ocultos".

### Opção B — Pelo Git (para quem já usa)

```bash
git init
git add .
git commit -m "Conciliador CISS v2.0"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/conciliador-despesas.git
git push -u origin main
```

---

## PASSO 4 — Criar conta no Streamlit Cloud

1. Acesse https://streamlit.io/cloud
2. Clique em **Sign up** → escolha **Continue with GitHub**
3. Autorize o acesso ao GitHub
4. Pronto, já está logado ✅

---

## PASSO 5 — Publicar o app

1. No Streamlit Cloud, clique em **"New app"**
2. Preencha:
   - **Repository:** `SEU_USUARIO/conciliador-despesas`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Clique em **Deploy!**
4. Aguarde ~2 minutos enquanto o Streamlit instala as dependências
5. Seu app estará disponível em uma URL do tipo:
   ```
   https://conciliador-despesas-XXXXXX.streamlit.app
   ```

---

## PASSO 6 — Compartilhar o link

Copie a URL gerada e compartilhe com qualquer pessoa da equipe.
**Não precisa instalar nada** — funciona direto no navegador, em qualquer dispositivo.

---

## Atualizando o app no futuro

Sempre que quiser atualizar o sistema:
1. Edite os arquivos localmente
2. Suba novamente para o GitHub (substitua os arquivos pelo site ou use git)
3. O Streamlit atualiza **automaticamente** em ~1 minuto

---

## Perguntas frequentes

**O app fica disponível 24h?**
Sim. O Streamlit Cloud mantém o app online. Após 7 dias sem uso, ele "dorme"
e acorda automaticamente no próximo acesso (demora ~30 segundos).

**Meus arquivos ficam salvos na nuvem?**
Não. Os arquivos carregados (Excel e PDF) são processados na memória e
descartados. Nada fica armazenado — segurança total dos dados.

**Posso deixar o app privado?**
O plano gratuito exige repositório público, mas o **app em si** não fica
indexado em buscadores. Só quem tiver o link consegue acessar.
Para repositório privado, o plano Community Pro do Streamlit é gratuito
para estudantes/professores ou $25/mês para empresas.

---

*CISS Consultoria em Informática, Serviços e Software S/A*
