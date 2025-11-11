# UE1_Projet
Analyse des actes médicaux prénataux en France (CCAM) : fusion des données hospitalières et libérales, traitement par acte et par année, avec visualisation et export CSV/Excel.

# Analyse des actes médicaux prénataux en France

## Description
Ce projet analyse les actes médicaux prénataux (CCAM) en France, en combinant les données hospitalières et libérales.  
Il permet de :  
- Nettoyer et fusionner les données provenant de différentes sources (CSV et Excel).  
- Filtrer les actes spécifiques (ex. `JPHJ0010`, `JPHJ0020`, `JPHB0010`, `JPHB0020`).  
- Agréger les nombres d’actes par année, par type d’acte et par origine (hospitalier/libéral).  
- Exporter des tableaux résumés au format CSV ou Excel pour analyses ultérieures.  
- Visualiser les totaux par année et par acte (graphiques matplotlib).

---

## Installation

1. Cloner le dépôt :  
```bash
git clone <url-du-repo>
cd <nom-du-repo>
```

## Créer l'env virtuel

### Windows
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancer

```bash
python main.py
```