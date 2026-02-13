# Coolify Monitoring Stack - Setup Guide

## 📊 Stack créé

**Projet**: `monitoring` (dev environment)
**Service UUID**: `t8sw48oo4wco008wc804ck8o`

### Services déployés
- **Grafana** (port 3000) - Dashboards & visualisation
- **Prometheus** (port 9090) - Collecte de métriques
- **cAdvisor** (port 8080) - Métriques containers Docker
- **Node Exporter** (port 9100) - Métriques système (CPU, RAM, disk)

---

## 🚀 Étapes de configuration

### 1. Uploader la configuration Prometheus dans Coolify

Le fichier `prometheus.yml` doit être monté dans le container Prometheus.

**Via l'interface Coolify:**
1. Accéder au service → Storage → File Storage
2. Upload `prometheus.yml` → monter à `/etc/prometheus/prometheus.yml`

**OU via SSH sur le serveur:**
```bash
# Trouver le chemin du service
cd /var/lib/docker/volumes/coolify-monitoring-*
# Copier prometheus.yml
cp prometheus.yml /path/to/coolify/service/
```

### 2. Déployer le stack

**Via Coolify UI:**
```
Services → grafana-monitoring-stack → Deploy
```

**Via MCP/API:**
```bash
# Déployer le service
coolify deploy t8sw48oo4wco008wc804ck8o
```

### 3. Accéder à Grafana

**URL**: `http://localhost:3000` (ou votre domaine configuré)

**Credentials:**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT**: Changer le mot de passe après première connexion!

---

## 📈 Configuration des dashboards

### Ajouter Prometheus comme datasource

1. Grafana → Configuration → Data Sources → Add data source
2. Sélectionner **Prometheus**
3. URL: `http://prometheus:9090`
4. Save & Test

### Importer les dashboards recommandés

**Dashboard 1: Docker Containers (cAdvisor)**
- Dashboard ID: `14282` (official Docker cAdvisor)
- URL: https://grafana.com/grafana/dashboards/14282
- Metrics: CPU, RAM, Network par container

**Dashboard 2: Node Exporter Full**
- Dashboard ID: `1860` (Node Exporter Full)
- URL: https://grafana.com/grafana/dashboards/1860
- Metrics: CPU, Load, RAM, Disk, Network système

**Dashboard 3: Prometheus Stats**
- Dashboard ID: `3662` (Prometheus 2.0 Stats)
- Metrics: Performance Prometheus lui-même

**Import:**
```
Dashboards → Import → Enter ID → Load → Select Prometheus datasource → Import
```

---

## 🔍 Vérifier que ça marche

### Test Prometheus scraping
```bash
# Vérifier les targets
curl http://localhost:9090/api/v1/targets

# Vérifier les métriques container
curl http://localhost:8080/metrics

# Vérifier les métriques système
curl http://localhost:9100/metrics
```

### Test dans Grafana
```
Explore → Select Prometheus datasource → Query:
- container_memory_usage_bytes
- node_cpu_seconds_total
- up{job="cadvisor"}
```

---

## 🎯 Dashboards personnalisés pour vos services

### Requêtes utiles

**Services unhealthy:**
```promql
container_last_seen{name=~".*unhealthy.*"}
```

**Top 5 containers par CPU:**
```promql
topk(5, rate(container_cpu_usage_seconds_total[5m]))
```

**Top 5 containers par RAM:**
```promql
topk(5, container_memory_usage_bytes)
```

**Containers crashés (restart count):**
```promql
sum by (name) (container_restart_count)
```

**Disk usage par container:**
```promql
container_fs_usage_bytes / container_fs_limit_bytes * 100
```

---

## ⚠️ Alerting (optionnel)

### Créer des alertes dans Grafana

**Exemple: Container down**
```
Metric: up{job="cadvisor"}
Condition: WHEN last() OF query() IS BELOW 1
Alert: Container is down!
```

**Exemple: High CPU**
```
Metric: rate(container_cpu_usage_seconds_total[5m])
Condition: WHEN avg() OF query() IS ABOVE 0.8
Alert: Container using >80% CPU
```

**Notification channels:**
- Email
- Slack webhook
- Discord webhook
- Webhook custom

---

## 🔧 Troubleshooting

### Prometheus ne scrape pas cAdvisor
```bash
# Vérifier que cAdvisor tourne
docker ps | grep cadvisor

# Vérifier les logs
docker logs cadvisor

# Test manuel
curl http://cadvisor:8080/metrics
```

### Grafana ne se connecte pas à Prometheus
```bash
# Vérifier le réseau Docker
docker network inspect monitoring

# Vérifier que Prometheus tourne
docker logs prometheus
```

### Métriques manquantes
```bash
# Vérifier les targets Prometheus
http://localhost:9090/targets

# All targets doivent être UP (green)
```

---

## 📊 Ressources utilisées

**Estimations:**
- Prometheus: ~200-300MB RAM
- Grafana: ~200-400MB RAM
- cAdvisor: ~100-150MB RAM
- Node Exporter: ~20-30MB RAM

**Total: ~500-900MB RAM** (dépend du nombre de containers monitorés)

---

## 🎨 Prochaines étapes

1. ✅ Déployer le stack
2. ✅ Configurer datasource Prometheus
3. ✅ Importer dashboards (14282, 1860, 3662)
4. 🔄 Créer dashboard personnalisé pour vos services critiques
5. 🔄 Configurer alerting (email/Slack)
6. 🔄 Ajouter Loki pour logs centralisés (optionnel)
7. 🔄 Configurer domaine public (monitoring.lesyetis.com)

---

## 🔐 Sécurité

**Production checklist:**
- [ ] Changer password Grafana admin
- [ ] Activer HTTPS (via Coolify reverse proxy)
- [ ] Limiter accès réseau (firewall/VPN)
- [ ] Backup volumes prometheus-data & grafana-data
- [ ] Activer authentication Grafana (OAuth/LDAP)
- [ ] Configurer retention Prometheus (actuellement 30 jours)
