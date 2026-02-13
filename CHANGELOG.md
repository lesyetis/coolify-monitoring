# Changelog - Coolify Monitoring Stack

## 2026-02-13 - Synchronisation config locale ↔ production

### 🔧 Corrections apportées

#### 1. Prometheus - Image officielle
```diff
- build:
-   context: .
-   dockerfile: Dockerfile.prometheus  # ❌ Fichier inexistant
+ image: prom/prometheus:latest  # ✅ Image officielle
```

#### 2. Configuration Prometheus complète
```yaml
+ volumes:
+   - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
+ command:
+   - '--config.file=/etc/prometheus/prometheus.yml'
+   - '--storage.tsdb.path=/prometheus'
+   - '--storage.tsdb.retention.time=30d'
+   - '--web.enable-lifecycle'
+ healthcheck:
+   test: ["CMD", "wget", "--spider", "-q", "http://localhost:9090/-/healthy"]
```

#### 3. Grafana - Provisioning path
```yaml
+ environment:
+   - SERVICE_FQDN_GRAFANA_3000  # Auto-FQDN Coolify
+   - GF_PATHS_PROVISIONING=/etc/grafana/provisioning
+ healthcheck:
+   test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/api/health"]
```

#### 4. Domaines FQDN
```diff
# Grafana
- Host: monitoring.lesyetis.com
+ Host: grafana.lesyetis.com  # ✅ Correspond à la prod

# Prometheus
  Host: prometheus.lesyetis.com  # ✅ Inchangé
```

#### 5. Ordre des services
```diff
# Réorganisé pour correspondre à la config Coolify
- prometheus (en premier)
+ grafana (en premier)
+ prometheus (en second)
```

### 📋 État production (via MCP Coolify)

**Service UUID**: `e0gsswo080s8w0cggc4k4oo4`

| Service | Status | FQDN Production | Healthcheck |
|---------|--------|-----------------|-------------|
| Grafana | ✅ `running:healthy` | `grafana.lesyetis.com` | ✅ OK |
| Prometheus | ✅ `running:healthy` | `prometheus-e0gsswo080s8w0cggc4k4oo4.lesyetis.com` | ✅ OK |
| cAdvisor | ✅ `running:healthy` | - | ✅ OK |
| Node Exporter | ⚠️ `running:unknown` | - | ⚠️ Pas de healthcheck |

### 🎯 Prochaines actions

#### Pour avoir un FQDN propre pour Prometheus
**Option 1**: Laisser `SERVICE_FQDN_PROMETHEUS_9090` (auto-géré par Coolify)
- Génère: `prometheus-e0gsswo080s8w0cggc4k4oo4.lesyetis.com`

**Option 2**: Configurer domaine custom dans Coolify UI
1. Aller dans Coolify → Service monitoring-stack → Prometheus
2. Ajouter FQDN custom: `prometheus.lesyetis.com`
3. Coolify mettra à jour automatiquement les labels Traefik

#### Services manquants (optionnels)
- ❌ Loki (logs centralisés)
- ❌ Promtail (collecte logs Docker)
- ❌ Weather Exporter (météo)

**Note**: Ces services existent dans `docker-compose-simple.yaml` mais ne sont pas déployés en prod.

### ✅ Résultat
- ✅ Config locale synchronisée avec production
- ✅ Image Prometheus officielle (problème Dockerfile résolu)
- ✅ Healthchecks ajoutés
- ✅ Retention 30j configurée
- ✅ Provisioning Grafana correctement configuré
