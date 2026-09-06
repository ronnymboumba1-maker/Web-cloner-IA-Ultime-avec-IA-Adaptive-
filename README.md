# 🌐 Web Cloner Ultime - JATHNIEL EDITION

> **Version :** 3.1  
> **Statut :** 100% Fonctionnel

---

# 📋 Description

**Web Cloner Ultime** est un outil de clonage de sites web disposant d'une interface graphique moderne.

Il permet notamment de :

- Télécharger un site web complet
- Explorer automatiquement les pages
- Télécharger les ressources (CSS, JavaScript, images...)
- Identifier certaines technologies utilisées
- Générer un rapport HTML
- Sauvegarder les résultats dans une base SQLite

---

# ✅ Fonctionnalités

| Fonctionnalité | Description | Statut |
|---------------|------------|:------:|
| GUI | Interface graphique moderne | ✅ |
| Crawl | Exploration récursive des pages | ✅ |
| Téléchargement HTML | Sauvegarde des pages | ✅ |
| Téléchargement Assets | CSS, JS, images | ✅ |
| Détection technologies | WordPress, Laravel, React, etc. | ✅ |
| Base de données | SQLite | ✅ |
| Multi-threading | 5 threads simultanés | ✅ |
| Logs temps réel | Affichage dans la GUI | ✅ |
| Rapport HTML | Génération automatique | ✅ |
| Arrêt contrôlé | Bouton Stop | ✅ |

---

# 🚀 Installation

## Prérequis

```bash
# Python 3.8+
python3 --version

# Dépendances
pip install requests beautifulsoup4
```

## Téléchargement

```bash
git clone https://github.com/JATHNIEL/web-cloner-ultime.git

cd web-cloner-ultime

python3 web_cloner.py
```

---

# 🎮 Utilisation

## Interface

```text
┌─────────────────────────────────────────────────────────────────────┐
│  🌐 WEB CLONER ULTIME - JATHNIEL EDITION                           │
│  Version 3.1                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ URL : [https://example.com________________________]                 │
│ Dossier : [./cloned_site__________________________]                 │
│                                                                     │
│ [🚀 Démarrer] [⏹ Arrêter] [🗑 Effacer]                              │
│                                                                     │
│ Pages : 0   Technologies : 0                                        │
│                                                                     │
│ 📋 LOGS                                                             │
│ ┌───────────────────────────────────────────────────────────────┐   │
│ │ [14:30:25] Prêt                                               │   │
│ │ [14:30:30] Démarrage...                                       │   │
│ │ [14:30:31] https://example.com                                │   │
│ └───────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Étapes

1. Entrer l'URL du site.
2. Choisir le dossier de destination.
3. Cliquer sur **Démarrer**.
4. Suivre la progression dans les logs.
5. Arrêter le processus si nécessaire.
6. Consulter le rapport HTML généré.

---

# 📂 Structure du projet

```text
cloned_site/
│
├── pages/
│   ├── abc123.html
│   └── ...
│
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
│
├── clone_data.db
│
└── report.html
```

---

# 📊 Base de données SQLite

## Tables

| Table | Description |
|--------|-------------|
| pages | Pages HTML téléchargées |
| technologies | Technologies détectées |

### Exemples SQL

```sql
SELECT url, title, size
FROM pages;

SELECT name
FROM technologies;
```

---

# 🔍 Détection des technologies

| Technologie | Pattern |
|-------------|---------|
| WordPress | wp-content |
| Laravel | laravel |
| Django | django |
| Rails | rails |
| React | react |
| Vue | vue.js |
| Angular | angular |
| jQuery | jquery |
| Bootstrap | bootstrap |
| Nginx | nginx |
| Apache | apache |
| PHP | .php |

---

# 📁 Ressources téléchargées

Le programme télécharge automatiquement :

- Pages HTML
- CSS
- JavaScript
- Images
- Polices
- Icônes

---

# ⚙️ Configuration

```python
CONFIG = {
    "max_depth": 3,
    "max_pages": 500,
    "threads": 5,
    "timeout": 10,
    "output_dir": "./cloned_site",
    "download_assets": True,
    "save_headers": True,
}
```

## Exemple

```python
CONFIG["max_depth"] = 5
CONFIG["max_pages"] = 1000
CONFIG["threads"] = 10
```

---

# 📄 Rapport HTML

À la fin de chaque clonage, un rapport est généré automatiquement.

Le rapport contient notamment :

- URL analysée
- Date du scan
- Nombre de pages
- Nombre de fichiers téléchargés
- Technologies détectées
- Statistiques générales

---

# 🔧 Dépannage

| Problème | Solution |
|----------|----------|
| Module not found | `pip install requests beautifulsoup4` |
| Permission denied | Vérifier les droits du dossier |
| Connection timeout | Vérifier l'URL ou augmenter le timeout |
| No pages found | Vérifier que le site est accessible |

## Vérification

```bash
python3 -c "import requests, bs4; print('OK')"

python3 --version
```

---

# 🛡️ Avertissement

> **Usage strictement éducatif et académique.**
>
> Cet outil est destiné à l'apprentissage, aux laboratoires de sécurité et aux audits réalisés avec l'autorisation explicite du propriétaire du site.
>
> L'utilisation contre des systèmes sans autorisation peut être illégale selon la législation en vigueur.
>
> L'utilisateur est responsable du respect des lois applicables.

---

# 📞 Informations

| Élément | Valeur |
|----------|--------|
| Nom | Web Cloner Ultime |
| Version | 3.1 |
| Auteur | JATHNIEL |
| Année | 2026 |
| Langage | Python 3 |
| Interface | Tkinter |
| Base de données | SQLite |

---

# 📦 Exemple

```bash
# Installation

pip install requests beautifulsoup4

# Lancement

python3 web_cloner.py

# Exemple

URL cible :
https://example.com

Démarrage...

✓ Page téléchargée
✓ CSS téléchargé
✓ Images téléchargées
✓ Technologies détectées

Rapport généré :
./cloned_site/report.html
```

---

# 📜 Licence

Usage éducatif et académique uniquement.

---

<div align="center">

## 🌐 Web Cloner Ultime

**JATHNIEL EDITION**

*Version 3.1*

🚀

</div>