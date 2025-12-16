import csv
import requests
import time
import os
from datetime import datetime

# Configurações de Caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, 'data', 'input_isbns.txt')
DATABASE_FILE = os.path.join(BASE_DIR, 'data', 'library.csv')
API_URL = "https://openlibrary.org/isbn/{}.json"

# Mapa Simplificado de CDD (Centenas)
CDD_MAP = {
    '0': 'Generalidades/Ciência da Computação',
    '1': 'Filosofia e Psicologia',
    '2': 'Religião',
    '3': 'Ciências Sociais',
    '4': 'Linguagem',
    '5': 'Ciências Naturais e Matemática',
    '6': 'Tecnologia e Ciências Aplicadas',
    '7': 'Artes',
    '8': 'Literatura e Retórica',
    '9': 'Geografia e História'
}

def resolve_cdd_category(cdd_code):
    """Traduz o código numérico para categoria macro."""
    if not cdd_code or cdd_code == 'N/A':
        return 'Indefinido'
    major_class = str(cdd_code)[0]
    return CDD_MAP.get(major_class, 'Outros')

def fetch_metadata(isbn):
    """Busca metadados na Open Library API."""
    print(f"[*] Consultando ISBN: {isbn}...")
    try:
        response = requests.get(API_URL.format(isbn), timeout=10)
        if response.status_code == 200:
            data = response.json()

            title = data.get('title', 'Desconhecido')
            cdd = data.get('dewey_decimal_class', ['N/A'])[0]

            # Formatação de Autores (Simplificada)
            # Para produção, idealmente buscaria os nomes via chave do autor
            has_authors = 'authors' in data
            author_key = 'Sim' if has_authors else 'Nao'

            return {
                'isbn': isbn,
                'titulo': title,
                'autor_ref': author_key, # Placeholder para refinamento futuro
                'cdd': cdd,
                'categoria': resolve_cdd_category(cdd),
                'tipo': 'FISICO',
                'data_registro': datetime.now().strftime('%Y-%m-%d')
            }
    except Exception as e:
        print(f"[!] Erro de conexão: {e}")
    return None

def update_csv(new_entries):
    """Atualiza o CSV principal mantendo histórico."""
    file_exists = os.path.isfile(DATABASE_FILE)
    existing_isbns = set()

    if file_exists:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_isbns.add(row['isbn'])

    keys = ['isbn', 'titulo', 'autor_ref', 'cdd', 'categoria', 'tipo', 'data_registro']

    with open(DATABASE_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if not file_exists:
            writer.writeheader()

        count = 0
        for entry in new_entries:
            if entry['isbn'] not in existing_isbns:
                writer.writerow(entry)
                count += 1
                print(f"[+] Registrado: {entry['titulo']}")
            else:
                print(f"[-] Ignorado (Duplicado): {entry['isbn']}")

        print(f"\nResumo: {count} novos livros adicionados ao catálogo.")

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Arquivo de entrada não encontrado: {INPUT_FILE}")
        # Cria arquivo vazio para facilitar
        open(INPUT_FILE, 'w').close()
        print("Arquivo criado. Insira os ISBNs e rode novamente.")
        return

    with open(INPUT_FILE, 'r') as f:
        # Filtra linhas vazias e espaços
        isbns = [line.strip() for line in f if line.strip()]

    if not isbns:
        print("Nenhum ISBN encontrado para processar.")
        return

    processed_data = []
    for isbn in isbns:
        meta = fetch_metadata(isbn)
        if meta:
            processed_data.append(meta)
        time.sleep(1) # Rate limit gentil

    update_csv(processed_data)

    # Limpa arquivo de entrada após sucesso
    open(INPUT_FILE, 'w').close()

if __name__ == "__main__":
    main()
