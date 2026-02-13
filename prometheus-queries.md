# Prometheus Queries Utiles pour Coolify

## 🎯 Services Status & Health

### Services actuellement en cours d'exécution
```promql
count(container_last_seen{name!=""})
```

### Services unhealthy
```promql
container_last_seen{name=~".*unhealthy.*"}
```

### Services qui ont crash dans la dernière heure
```promql
changes(container_last_seen{name!=""}[1h]) > 0
```

### Uptime par service (en secondes)
```promql
time() - container_start_time_seconds{name!=""}
```

---

## 💻 CPU & Performance

### CPU usage par container (%)
```promql
rate(container_cpu_usage_seconds_total{name!=""}[5m]) * 100
```

### Top 5 containers par CPU
```promql
topk(5, rate(container_cpu_usage_seconds_total{name!=""}[5m]) * 100)
```

### Containers utilisant >80% CPU
```promql
rate(container_cpu_usage_seconds_total{name!=""}[5m]) * 100 > 80
```

### CPU usage système global
```promql
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

---

## 🧠 Memory

### Memory usage par container (MB)
```promql
container_memory_usage_bytes{name!=""} / 1024 / 1024
```

### Top 5 containers par RAM
```promql
topk(5, container_memory_usage_bytes{name!=""} / 1024 / 1024)
```

### Memory usage ratio (utilisé/limite)
```promql
container_memory_usage_bytes{name!=""} / container_spec_memory_limit_bytes{name!=""} * 100
```

### Containers proche de la limite RAM (>90%)
```promql
(container_memory_usage_bytes{name!=""} / container_spec_memory_limit_bytes{name!=""}) * 100 > 90
```

### RAM système disponible (%)
```promql
(node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
```

---

## 🌐 Network

### Network RX (received) par container (bytes/sec)
```promql
rate(container_network_receive_bytes_total{name!=""}[5m])
```

### Network TX (transmitted) par container (bytes/sec)
```promql
rate(container_network_transmit_bytes_total{name!=""}[5m])
```

### Total bandwidth par container (MB/sec)
```promql
(rate(container_network_receive_bytes_total{name!=""}[5m]) + rate(container_network_transmit_bytes_total{name!=""}[5m])) / 1024 / 1024
```

### Top 5 containers par network I/O
```promql
topk(5, rate(container_network_receive_bytes_total{name!=""}[5m]) + rate(container_network_transmit_bytes_total{name!=""}[5m]))
```

---

## 💾 Disk & Storage

### Disk usage par container (bytes)
```promql
container_fs_usage_bytes{name!=""}
```

### Disk usage ratio (%)
```promql
container_fs_usage_bytes{name!=""} / container_fs_limit_bytes{name!=""} * 100
```

### Containers avec >90% disk usage
```promql
(container_fs_usage_bytes{name!=""} / container_fs_limit_bytes{name!=""}) * 100 > 90
```

### Disk I/O reads (bytes/sec)
```promql
rate(container_fs_reads_bytes_total{name!=""}[5m])
```

### Disk I/O writes (bytes/sec)
```promql
rate(container_fs_writes_bytes_total{name!=""}[5m])
```

### Système: Disk usage root partition (%)
```promql
(node_filesystem_size_bytes{mountpoint="/"} - node_filesystem_avail_bytes{mountpoint="/"}) / node_filesystem_size_bytes{mountpoint="/"} * 100
```

---

## 🔄 Restarts & Availability

### Nombre de restarts par container
```promql
sum by (name) (container_restart_count{name!=""})
```

### Containers redémarrés dans les 5 dernières minutes
```promql
delta(container_restart_count{name!=""}[5m]) > 0
```

### Container uptime (jours)
```promql
(time() - container_start_time_seconds{name!=""}) / 86400
```

---

## 📊 Services spécifiques Coolify

### Plane (project management)
```promql
# CPU
rate(container_cpu_usage_seconds_total{name=~".*plane.*"}[5m]) * 100

# Memory
container_memory_usage_bytes{name=~".*plane.*"} / 1024 / 1024

# Network
rate(container_network_receive_bytes_total{name=~".*plane.*"}[5m])
```

### GlitchTip (error tracking)
```promql
# CPU
rate(container_cpu_usage_seconds_total{name=~".*glitchtip.*"}[5m]) * 100

# Memory
container_memory_usage_bytes{name=~".*glitchtip.*"} / 1024 / 1024
```

### n8n (automation)
```promql
# CPU
rate(container_cpu_usage_seconds_total{name=~".*n8n.*"}[5m]) * 100

# Memory
container_memory_usage_bytes{name=~".*n8n.*"} / 1024 / 1024
```

### Twenty CRM
```promql
# Status
up{name=~".*twenty.*"}

# CPU
rate(container_cpu_usage_seconds_total{name=~".*twenty.*"}[5m]) * 100
```

### Databases (MySQL/PostgreSQL)
```promql
# Memory usage
container_memory_usage_bytes{name=~".*(mysql|postgres|db).*"} / 1024 / 1024

# CPU
rate(container_cpu_usage_seconds_total{name=~".*(mysql|postgres|db).*"}[5m]) * 100
```

---

## 🚨 Alerting Queries

### Container down
```promql
up{job="cadvisor"} == 0
```

### High CPU usage (>80% for 5min)
```promql
rate(container_cpu_usage_seconds_total{name!=""}[5m]) * 100 > 80
```

### High memory usage (>90% for 5min)
```promql
(container_memory_usage_bytes{name!=""} / container_spec_memory_limit_bytes{name!=""}) * 100 > 90
```

### Container restart
```promql
delta(container_restart_count{name!=""}[5m]) > 0
```

### System disk full (>85%)
```promql
(node_filesystem_size_bytes{mountpoint="/"} - node_filesystem_avail_bytes{mountpoint="/"}) / node_filesystem_size_bytes{mountpoint="/"} * 100 > 85
```

### System RAM low (<10% available)
```promql
(node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 < 10
```

---

## 📈 Aggregations utiles

### Total CPU usage tous containers
```promql
sum(rate(container_cpu_usage_seconds_total{name!=""}[5m])) * 100
```

### Total memory usage tous containers (GB)
```promql
sum(container_memory_usage_bytes{name!=""}) / 1024 / 1024 / 1024
```

### Total network bandwidth (MB/sec)
```promql
sum(rate(container_network_receive_bytes_total{name!=""}[5m]) + rate(container_network_transmit_bytes_total{name!=""}[5m])) / 1024 / 1024
```

---

## 🎨 Variables pour dashboards dynamiques

### Liste de tous les containers
```promql
label_values(container_last_seen{name!=""}, name)
```

### Liste des services unhealthy uniquement
```promql
label_values(container_last_seen{name=~".*unhealthy.*"}, name)
```

### Liste des services par projet
```promql
label_values(container_last_seen{name=~".*$project.*"}, name)
```

---

## 💡 Tips

**Utiliser `[5m]` vs `[1m]`:**
- `[1m]` = plus réactif mais plus de bruit
- `[5m]` = moyenne plus stable, recommandé pour alerting

**Rate vs irate:**
- `rate()` = moyenne sur la période
- `irate()` = instantané basé sur les 2 derniers points
- Utiliser `rate()` pour alerting, `irate()` pour graphes temps réel

**Label matching:**
- `name="exact"` = match exact
- `name=~".*pattern.*"` = regex match
- `name!~".*pattern.*"` = regex exclude

**Aggregations:**
- `sum()` = total
- `avg()` = moyenne
- `max()` = maximum
- `min()` = minimum
- `topk(n, ...)` = top N valeurs
- `bottomk(n, ...)` = bottom N valeurs
