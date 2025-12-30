#!/usr/bin/env bash

# Calibre instalado via flatpak

# O Calibre precisa estar fechado para executar esse comandos

# Listando todos os campos
flatpak run --command=calibredb com.calibre_ebook.calibre list --fields all

# Exportando o json
flatpak run --command=calibredb com.calibre_ebook.calibre list \
  --for-machine \
  --sort-by "*cdd" \
  --fields "title,authors,publisher,tags,isbn,*cdd,*cdd_class,*read" > biblioteca.json

# Exportando csv
flatpak run --command=calibredb com.calibre_ebook.calibre list \
  --fields "title,authors,publisher,tags,isbn,*cdd,*cdd_class" \
  --sort-by "*cdd" \
  --separator ';' > biblioteca.csv
