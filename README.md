# 📊 Coolify Monitoring Stack

Stack complet de monitoring pour infrastructure Coolify avec Grafana, Prometheus, cAdvisor et Node Exporter.

---

## 🎯 Créé avec succès

✅ **Projet**: `monitoring` (UUID: `d0ws4k44ok8088swwws40ccg`)
✅ **Environment**: `dev` (UUID: `ywo4g48wko000c0gsk8gw04c`)
✅ **Service**: `grafana-monitoring-stack` (UUID: `t8sw48oo4wco008wc804ck8o`)
✅ **Serveur**: `localhost` (UUID: `as8kggoogkkgoc88o4ookgos`)

---

## 📦 Contenu du stack

### Services déployés

| Service | Port | Description |
|---------|------|-------------|
| **Grafana** | 3000 | Dashboards & visualisation |
| **Prometheus** | 9090 | Collecte & stockage métriques |
| **cAdvisor** | 8080 | Métriques containers Docker |
| **Node Exporter** | 9100 | Métriques système (CPU, RAM, disk) |

### Volumes persistants
- `prometheus-data` - Stockage métriques (30 jours retention)
- `grafana-data` - Configuration & dashboards Grafana

---

## 🚀 Quick Start

### 1. Uploader la configuration Prometheus

**Le fichier `prometheus.yml` doit être monté dans Coolify:**

Via Coolify UI:
```
Services → grafana-monitoring-stack → Storage → File Storage
→ Upload prometheus.yml
→ Mount path: /etc/prometheus/prometheus.yml
```

### 2. Déployer le stack

**Via Coolify UI:**
```
Services → grafana-monitoring-stack → Deploy
```

**Via API:**
```bash
curl -X POST https://your-coolify.com/api/v1/deploy/t8sw48oo4wco008wc804ck8o \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Accéder à Grafana

**URL**: `http://localhost:3000`

**Credentials:**
- Username: `admin`
- Password: `admin123`

⚠️ **Changer le mot de passe immédiatement!**

### 4. Configurer la datasource Prometheus

```
Grafana → Configuration → Data Sources → Add data source
→ Prometheus
→ URL: http://prometheus:9090
→ Save & Test
```

### 5. Importer les dashboards

**Dashboards recommandés:**
- **14282** - Docker Containers (cAdvisor)
- **1860** - Node Exporter Full
- **3662** - Prometheus Stats

**OU utiliser le dashboard custom:**
```
Dashboards → Import → Upload JSON
→ Sélectionner dashboard-coolify-services.json
```

---

## 📁 Fichiers fournis

```
coolify-monitoring/
├── README.md                         ← Ce fichier
├── SETUP.md                          ← Guide détaillé setup & configuration
├── prometheus.yml                    ← Configuration Prometheus
├── prometheus-queries.md             ← Requêtes Prometheus utiles
└── dashboard-coolify-services.json   ← Dashboard Grafana custom
```

---

## 🎨 Dashboards & métriques disponibles

### Vue d'ensemble
- Total containers running
- Services status (up/down)
- CPU usage par container
- Memory usage par container
- Network I/O par container
- Container restarts
- Unhealthy services

### Métriques système
- CPU usage global
- Memory usage global
- Disk usage
- Network I/O

### Services spécifiques monitorés
- plane (project management)
- glitchtip (error tracking)
- n8n (automation)
- twenty-crm
- weaviate (vector DB)
- nocodb
- Tous vos autres services Coolify

---

## 🚨 Alerting

### Alertes recommandées à configurer

**Container down:**
```promql
up{job="cadvisor"} == 0
```

**High CPU (>80% for 5min):**
```promql
rate(container_cpu_usage_seconds_total{name!=""}[5m]) * 100 > 80
```

**High Memory (>90%):**
```promql
(container_memory_usage_bytes / container_spec_memory_limit_bytes) * 100 > 90
```

**Container restart:**
```promql
delta(container_restart_count{name!=""}[5m]) > 0
```

**Disk full (>85%):**
```promql
(node_filesystem_size_bytes{mountpoint="/"} - node_filesystem_avail_bytes) / node_filesystem_size_bytes * 100 > 85
```

---

## 📊 Ressources utilisées

| Service | RAM | CPU | Notes |
|---------|-----|-----|-------|
| Prometheus | 200-300MB | Low | Dépend du nombre de containers |
| Grafana | 200-400MB | Low | Augmente avec dashboards actifs |
| cAdvisor | 100-150MB | Medium | Monitoring constant |
| Node Exporter | 20-30MB | Very Low | Lightweight |
| **Total** | **~500-900MB** | **Low-Medium** | Pour ~25 containers |

---

## 🔧 Troubleshooting

### Prometheus ne collecte pas de métriques

```bash
# Vérifier les targets
curl http://localhost:9090/api/v1/targets

# Vérifier les logs
docker logs prometheus
```

### cAdvisor ne démarre pas

```bash
# Vérifier les permissions
# cAdvisor a besoin d'accès privilégié au host

docker logs cadvisor
```

### Grafana ne se connecte pas à Prometheus

```bash
# Vérifier le réseau Docker
docker network inspect monitoring

# Les containers doivent être sur le même réseau
```

---

## 📈 Prochaines étapes

### Immédiat
- [ ] Déployer le stack
- [ ] Configurer datasource Prometheus
- [ ] Importer dashboards
- [ ] Changer password Grafana

### Court terme
- [ ] Configurer alerting (Slack/Email)
- [ ] Créer dashboard personnalisé pour services critiques
- [ ] Backup volumes Grafana/Prometheus

### Long terme
- [ ] Ajouter Loki pour logs centralisés
- [ ] Configurer domaine public (monitoring.lesyetis.com)
- [ ] Activer HTTPS via Coolify reverse proxy
- [ ] Alertmanager pour gestion avancée alertes

---

## 🔐 Sécurité Production

**Checklist avant prod:**
- [ ] Mot de passe admin Grafana fort
- [ ] HTTPS activé
- [ ] Accès réseau limité (VPN/firewall)
- [ ] Backups automatiques configurés
- [ ] Retention Prometheus adaptée (actuellement 30j)
- [ ] Authentication Grafana (OAuth/LDAP)

---

## 📚 Documentation

- **SETUP.md** - Guide complet configuration
- **prometheus-queries.md** - Requêtes Prometheus prêtes à l'emploi
- **dashboard-coolify-services.json** - Dashboard pré-configuré

---

## 🆘 Support

**Vérifier les services unhealthy actuels:**
```bash
# Via API Coolify
curl https://your-coolify.com/api/v1/services
```

**Diagnostiquer un service:**
```
Coolify MCP: mcp__coolify__diagnose_app("service-name")
```

---

## ✅ Validation finale

**Checklist post-déploiement:**

```bash
# 1. Vérifier que tous les containers tournent
docker ps | grep -E "(prometheus|grafana|cadvisor|node-exporter)"

# 2. Vérifier Prometheus collecte les métriques
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job, health}'

# 3. Vérifier cAdvisor expose les métriques
curl http://localhost:8080/metrics | head -20

# 4. Vérifier Node Exporter
curl http://localhost:9100/metrics | head -20

# 5. Tester Grafana datasource
# Via UI: Data Sources → Prometheus → Test
```

**Tous doivent retourner status: UP** ✅

---

**Stack créé le**: 2026-02-13
**Coolify version**: 4.0.0-beta.462
