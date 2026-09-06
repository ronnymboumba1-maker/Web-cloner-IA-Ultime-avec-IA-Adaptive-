🌐 Web Cloner Ultime - JATHNIEL EDITION

Version 3.1 - 100% Fonctionnel

---

📋 DESCRIPTION

Web Cloner Ultime est un outil de clonage de sites web avec interface graphique. Il permet de télécharger des sites web entiers, d'extraire les fichiers sensibles, de détecter les technologies utilisées et les secrets exposés.

---

✅ FONCTIONNALITÉS (100% RÉELLES)

Fonctionnalité Description Statut
GUI Interface graphique moderne ✅
Crawl Exploration récursive des pages ✅
Téléchargement HTML Sauvegarde des pages ✅
Téléchargement Assets CSS, JS, images ✅
Fichiers sensibles .env, config, .git, etc. ✅
Détection technologies WordPress, Laravel, React, etc. ✅
Détection secrets API keys, tokens, mots de passe ✅
Base de données SQLite ✅
Multi-threading 5 threads simultanés ✅
Logs en temps réel Affichage GUI ✅
Rapport HTML Génération automatique ✅
Arrêt contrôlé Bouton Stop ✅

---

🚀 INSTALLATION

Prérequis

```bash
# Python 3.8+
python3 --version

# Dépendances
pip install requests beautifulsoup4
```

Téléchargement

```bash
# Cloner le dépôt
git clone https://github.com/JATHNIEL/web-cloner-ultime.git
cd web-cloner-ultime

# Lancer
python3 web_cloner.py
```

---

🎮 UTILISATION

Interface

```
┌─────────────────────────────────────────────────────────────────────┐
│  🌐 WEB CLONER ULTIME - JATHNIEL EDITION                           │
│  v3.1                                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  URL: [https://example.com________________________] Dossier: [./cloned_site] │
│                                                                      │
│  [🚀 Démarrer]  [⏹️ Arrêter]  [🗑️ Effacer]                       │
│                                                                      │
│  Pages: 0  Fichiers sensibles: 0  Secrets: 0  Technologies: 0      │
│                                                                      │
│  📋 LOGS                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ [14:30:25] 🔍 Prêt - Entrez une URL et cliquez sur Démarrer │   │
│  │ [14:30:30] 🚀 Démarrage du clonage...                      │   │
│  │ [14:30:30] 📄 1: https://example.com                       │   │
│  │ [14:30:31] ⚙️ Technologie: Nginx                           │   │
│  │ [14:30:31] ⚙️ Technologie: PHP                            │   │
│  │ [14:30:32] 📄 2: https://example.com/page1                │   │
│  │ [14:30:33] 🔴 Fichier sensible: .env (245 octets)         │   │
│  │ [14:30:33] 🔑 SECRET: API Key (32 chars)                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

Étapes

1. Entrer l'URL du site à cloner
2. Choisir le dossier de destination (par défaut: ./cloned_site)
3. Cliquer sur "Démarrer"
4. Surveiller les logs en temps réel
5. Cliquer sur "Arrêter" pour stopper (si nécessaire)
6. Consulter le rapport généré automatiquement

---

📂 STRUCTURE DE SORTIE

```
cloned_site/
├── pages/              # Pages HTML téléchargées
│   ├── abc123def456.html
│   └── ...
├── assets/             # CSS, JS, images
│   ├── style.css
│   ├── script.js
│   └── ...
├── sensitive/          # Fichiers sensibles (.env, config, etc.)
│   ├── .env
│   ├── wp-config.php
│   └── ...
├── clone_data.db       # Base de données SQLite
└── report.html         # Rapport d'audit
```

---

📊 BASE DE DONNÉES

Tables

Table Description
pages Pages HTML téléchargées
sensitive_files Fichiers sensibles trouvés
secrets Secrets détectés (API keys, etc.)
technologies Technologies identifiées

Exemple de requête

```sql
-- Voir toutes les pages
SELECT url, title, size FROM pages;

-- Voir les fichiers sensibles
SELECT filename, path, size FROM sensitive_files;

-- Voir les secrets critiques
SELECT type, value, source FROM secrets WHERE severity = 'critical';

-- Voir les technologies
SELECT name FROM technologies;
```

---

🔍 DÉTECTION DES TECHNOLOGIES

Technologie Patterns
WordPress wp-content, wp-includes
Laravel laravel, csrf-token
Django django, csrfmiddlewaretoken
Rails rails, authenticity_token
React react, react-dom
Vue vue.js, v-bind
Angular angular, ng-app
jQuery jquery, $(
Bootstrap bootstrap, navbar
Nginx nginx
Apache apache
PHP .php, ?php
Cloudflare cf-ray, __cfduid

---

🔑 DÉTECTION DES SECRETS

Type Pattern Severity
API Key (32 chars) [A-Z0-9]{32} High
AWS Access Key AKIA[0-9A-Z]{16} Critical
Stripe Secret Key sk_live_[a-zA-Z0-9]{24} Critical
Stripe Publishable Key pk_live_[a-zA-Z0-9]{24} High
RSA Private Key -----BEGIN RSA PRIVATE KEY----- Critical
Password in JSON \"password\"\s*:\s*\"[^\"]+\" High
API Key in JSON \"api_key\"\s*:\s*\"[^\"]+\" High
JWT Secret JWT_SECRET\s*=\s*[\'"]?([^\'"]+)[\'"]? Critical
Database Password DB_PASS[D]?[A-Z]?\s*=\s*[\'"]?([^\'"]+)[\'"]? Critical

---

📁 FICHIERS SENSIBLES RECHERCHÉS

Fichier Description
.env Variables d'environnement
.env.local Variables d'environnement (local)
wp-config.php Configuration WordPress
config.php Configuration PHP
settings.py Configuration Django
appsettings.json Configuration ASP.NET
web.config Configuration IIS
.htaccess Configuration Apache
robots.txt Instructions robots
composer.json Dépendances PHP
package.json Dépendances Node.js
.git Dépôt Git
access.log Logs d'accès
error.log Logs d'erreurs
.sql / .db Bases de données
.pem / .crt / .key Certificats
id_rsa Clé SSH
authorized_keys Clés SSH autorisées

---

⚙️ CONFIGURATION

Paramètres modifiables

```python
CONFIG = {
    'max_depth': 3,        # Profondeur de crawl
    'max_pages': 500,      # Nombre max de pages
    'threads': 5,          # Threads simultanés
    'timeout': 10,         # Timeout des requêtes
    'output_dir': './cloned_site',  # Dossier de sortie
    'download_assets': True,        # Télécharger assets
    'save_headers': True,           # Sauvegarder headers
}
```

Modification

```python
# Dans web_cloner.py
CONFIG['max_depth'] = 5
CONFIG['max_pages'] = 1000
CONFIG['threads'] = 10
```

---

📄 RAPPORT HTML

Un rapport est généré automatiquement à la fin du clonage :

```html
<!DOCTYPE html>
<html>
<head>
    <title>Web Cloner Ultime - Rapport</title>
</head>
<body>
    <div class="header">
        <h1>🌐 Web Cloner Ultime</h1>
        <p>Cible: https://example.com</p>
        <p>Date: 2026-09-06 14:30:45</p>
        <p>JATHNIEL EDITION</p>
    </div>
    <div class="stats">
        <div class="stat">
            <div class="number">45</div>
            <div>Pages</div>
        </div>
        <div class="stat">
            <div class="number">12</div>
            <div>Fichiers sensibles</div>
        </div>
        <div class="stat">
            <div class="number">3</div>
            <div>Secrets</div>
        </div>
        <div class="stat">
            <div class="number">5</div>
            <div>Technologies</div>
        </div>
    </div>
</body>
</html>
```

---

🔧 DÉPANNAGE

Problème Solution
"Module not found" pip install requests beautifulsoup4
"Permission denied" Vérifier les droits du dossier de sortie
"Connection timeout" Vérifier l'URL ou augmenter le timeout
"No pages found" Vérifier que le site est accessible

Vérification

```bash
# Vérifier les dépendances
python3 -c "import requests, bs4; print('OK')"

# Vérifier la version Python
python3 --version  # > 3.8
```

---

🛡️ AVERTISSEMENT

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ⚠️  USAGE STRICTEMENT ÉDUCATIF ET ACADÉMIQUE                     ║
║                                                                      ║
║   Cet outil est conçu pour des tests de sécurité dans le cadre      ║
║   d'un laboratoire isolé et autorisé.                               ║
║                                                                      ║
║   L'utilisation de cet outil sur des sites sans autorisation       ║
║   est ILLÉGALE et peut entraîner des poursuites judiciaires.        ║
║                                                                      ║
║   L'utilisateur est SEUL RESPONSABLE de l'usage de cet outil.      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

📞 INFORMATIONS

Élément Détail
Nom Web Cloner Ultime
Version 3.1
Auteur JATHNIEL
Année 2026
Langage Python 3
Interface Tkinter
Licence Usage éducatif

---

📦 EXEMPLE D'UTILISATION

```bash
# Installation
pip install requests beautifulsoup4

# Lancement
python3 web_cloner.py

# Entrer une URL
🌐 URL cible: https://example.com

# Résultat
🚀 Démarrage du clonage...
📄 1: https://example.com
⚙️ Technologie: Nginx
⚙️ Technologie: PHP
📄 2: https://example.com/page1
🔴 Fichier sensible: .env (245 octets)
🔑 SECRET: API Key (32 chars)
✅ Clonage terminé!
📄 Rapport généré: ./cloned_site/report.html
```

---

🔧 Web Cloner Ultime - L'outil de clonage complet ! 🚀