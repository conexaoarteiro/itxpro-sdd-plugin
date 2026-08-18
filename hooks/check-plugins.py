#!/usr/bin/env python3
"""check-plugins.py — confere os plugins recomendados pelo framework SDD.

O que faz: lê a tabela "Plugins de terceiros: instalação" de
base/skills-padrao.md do plugin (cabeçalho fixo
"| Plugin | Fonte oficial | Instalação | Sem ele |") e o registro local de
plugins instalados do Claude Code
(${CLAUDE_CONFIG_DIR:-~/.claude}/plugins/installed_plugins.json). Imprime,
para cada plugin ausente, o comando de instalação, a fonte oficial e o que
degrada sem ele. Instalado = existe alguma chave "nome@<marketplace>" em
"plugins", qualquer escopo.

O que nunca faz: instalar, executar comando, acessar rede, escrever em
disco. Somente leitura de dois arquivos locais. Exit 0 sempre: é aviso,
não gate.

Onde para: registro ausente, ilegível ou fora do formato esperado vira
"não verificado" para a lista inteira (fail-open declarado); "não
verificado" nunca vira "presente". Quem lê a saída trata como pendência.

Uso: python3 check-plugins.py [--skills-padrao <caminho>] [--registro <caminho>]
Somente stdlib do Python 3.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

CABECALHO = "| Plugin | Fonte oficial | Instalação | Sem ele |"
RE_NOME = re.compile(r"`([^`]+)`")


def caminho_skills_padrao_default():
    aqui = Path(__file__).resolve().parent
    for cand in (aqui.parent / "base" / "skills-padrao.md", aqui.parent / "skills-padrao.md"):
        if cand.is_file():
            return cand
    return aqui.parent / "base" / "skills-padrao.md"


def caminho_registro_default():
    base = os.environ.get("CLAUDE_CONFIG_DIR") or str(Path.home() / ".claude")
    return Path(base) / "plugins" / "installed_plugins.json"


def le_tabela(caminho):
    """Devolve lista de dicts {nome, fonte, instalacao, sem_ele}; [] se não achar."""
    try:
        linhas = Path(caminho).read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    try:
        inicio = linhas.index(CABECALHO)
    except ValueError:
        return []
    plugins = []
    for linha in linhas[inicio + 2:]:
        if not linha.startswith("|"):
            break
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(celulas) < 4:
            continue
        m = RE_NOME.search(celulas[0])
        if not m:
            continue
        plugins.append({
            "nome": m.group(1),
            "fonte": celulas[1],
            "instalacao": celulas[2].strip("`"),
            "sem_ele": celulas[3],
        })
    return plugins


def le_registro(caminho):
    """Devolve o conjunto de nomes instalados, ou None se não verificável."""
    try:
        dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    chaves = dados.get("plugins") if isinstance(dados, dict) else None
    if not isinstance(chaves, dict):
        return None
    return {chave.split("@", 1)[0] for chave in chaves}


def main():
    ap = argparse.ArgumentParser(description="Confere plugins recomendados; nunca instala.")
    ap.add_argument("--skills-padrao", default=None)
    ap.add_argument("--registro", default=None)
    args = ap.parse_args()
    skills = Path(args.skills_padrao) if args.skills_padrao else caminho_skills_padrao_default()
    registro = Path(args.registro) if args.registro else caminho_registro_default()

    tabela = le_tabela(skills)
    if not tabela:
        print("não verificado: tabela 'Plugins de terceiros: instalação' não encontrada em "
              f"{skills.name}; confira com /plugin")
        return 0

    instalados = le_registro(registro)
    if instalados is None:
        print("não verificado: registro local de plugins ilegível; confira com /plugin")
        for p in tabela:
            print(f"- não verificado: {p['nome']}")
            print(f"  instalar: {p['instalacao']}")
            print(f"  fonte: {p['fonte']}")
            print(f"  sem ele: {p['sem_ele']}")
        return 0

    presentes = [p for p in tabela if p["nome"] in instalados]
    ausentes = [p for p in tabela if p["nome"] not in instalados]
    print(f"Plugins recomendados: {len(presentes)} presentes, {len(ausentes)} ausentes")
    for p in ausentes:
        print(f"- ausente: {p['nome']}")
        print(f"  instalar: {p['instalacao']}")
        print(f"  fonte: {p['fonte']}")
        print(f"  sem ele: {p['sem_ele']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
