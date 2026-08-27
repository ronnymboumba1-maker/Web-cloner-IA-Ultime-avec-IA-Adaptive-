```markdown
# 🤖 WEB CLONER ULTIME AVEC IA ADAPTATIVE

## Cloneur intelligent avec détection automatique des vulnérabilités

### 📌 Description

WEB CLONER ULTIME est un cloneur de site intelligent qui utilise une IA adaptative pour détecter automatiquement les vulnérabilités, extraire les fichiers sensibles et exploiter les failles découvertes.

### ✨ Fonctionnalités

#### 🧠 IA Adaptative
- Détection automatique des APIs (GraphQL, REST, WebSocket)
- Détection des secrets (clés AWS, Stripe, JWT, mots de passe)
- Détection des vulnérabilités (XSS, SQLi, LFI, RFI)
- Détection des technologies utilisées
- Adaptation de la stratégie d'exploitation

#### 📡 Exploitation
- GraphQL : Introspection + vol de données
- Stripe : Vol de cartes bancaires
- AWS : Listage de buckets
- Admin : Brute force des identifiants

#### 📁 Téléchargement
- Fichiers sensibles (.env, config.php, etc.)
- Assets (CSS, JS, images)
- Pages HTML avec rendu JavaScript

#### 💾 Sauvegarde
- Base de données SQLite
- Export JSON
- Rapport complet
- Fichiers séparés par type

#### 📊 Consultation
- Menu interactif
- Affichage des données volées
- Export des données

### 🚀 Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-compte/web-cloner-ultime.git
cd web-cloner-ultime

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/WSL
# ou
venv\Scripts\activate     # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Installer Playwright
playwright install chromium
```

🎯 Utilisation

```bash
# Lancer le cloneur
python3 ultimate_cloner.py

# Entrer l'URL cible
URL cible: https://example.com
```

📋 Menu de consultation

```
📋 MENU DE CONSULTATION
==================================================
1. 💳 Voir les cartes Stripe volées
2. ☁️ Voir les buckets AWS
3. 🔐 Voir les identifiants admin
4. 🔑 Voir tous les secrets
5. 📁 Voir les fichiers sensibles
6. 🚨 Voir les vulnérabilités
7. 📊 Voir le rapport complet
8. 💾 Exporter toutes les données
0. Quitter
==================================================
```

📁 Structure de sortie

```
cloned_site/
├── pages/              # Pages HTML
├── assets/             # CSS, JS, images
├── sensitive/          # Fichiers sensibles téléchargés
├── screenshots/        # Captures d'écran
├── clone_data.db       # Base de données SQLite
├── clone_results.json  # Résultats structurés
├── clone_report.txt    # Rapport complet
├── stripe_data.json    # Cartes Stripe volées
├── aws_buckets.json    # Buckets AWS trouvés
├── admin_credentials.txt # Identifiants admin
└── export/             # Export des données
```