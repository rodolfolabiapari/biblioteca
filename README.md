# Personal Library Manager (CDD Based)

Sistema de gestão de acervo bibliográfico pessoal utilizando Python para catalogação via ISBN e Docker (Kavita) para consumo de Ebooks.

## Estrutura de Dados

A fonte da verdade é o arquivo `data/library.csv`.

## Fluxo de Trabalho

### 1. Adicionar Livros Físicos

1. Usando um scanner ou app, popule o arquivo `data/input_isbns.txt` com os códigos de barra (um por linha).
2. Execute o script de processamento:
   ```bash
   python3 scripts/manager.py
   ```
3. O script irá:
   - Consultar a Open Library API.
   - Resolver a categoria CDD (Dewey Decimal).
   - Atualizar `data/library.csv`.
   - Limpar o arquivo de input.

### 2. Adicionar Ebooks
1. Coloque os arquivos `.pdf` ou `.epub` na pasta `library/ebooks/`.
2. Adicione manualmente a entrada correspondente no `data/library.csv` mudando o tipo para `DIGITAL`.

### 3. Visualização (Raspberry/Orange Pi)
Inicie o servidor de leitura:
```bash
docker-compose up -d
```
Acesse: `http://localhost:5000`

### 4. Versionamento
Após alterações, registre no Git:
```bash
git add data/library.csv
git commit -m "update: novos livros registrados"
git push origin main
```
