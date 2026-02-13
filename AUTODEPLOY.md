# 🚀 Auto-Deploy Configuration

Ce projet est configuré pour le **déploiement automatique** via Coolify.

## ⚙️ Configuration

### Dans Coolify UI

1. **Aller dans le service**
   ```
   Projects → monitoring → dev → grafana-monitoring-stack
   ```

2. **Activer Automatic Deployment**
   - General → **Automatic Deployment** → ✅ **Enable**
   - Branch: `master`
   - Watch Paths: `.` (tout le projet)

3. **Webhook GitHub (optionnel mais recommandé)**

   Coolify génère automatiquement un webhook URL :
   ```
   https://coolify.lesyetis.com/api/v1/deploy?uuid=t8sw48oo4wco008wc804ck8o
   ```

   Ajouter dans GitHub :
   - Repo → **Settings** → **Webhooks** → **Add webhook**
   - Payload URL : `[URL du webhook Coolify]`
   - Content type : `application/json`
   - Events : `Just the push event`
   - Active : ✅

## 🔄 Workflow de déploiement

```
git push origin master
    ↓
GitHub webhook notifie Coolify (instantané)
    ↓
Coolify détecte le nouveau commit
    ↓
Pull depuis GitHub
    ↓
Rebuild images (si nécessaire)
    ↓
Redeploy avec healthchecks
    ↓
✅ Déploiement terminé (~2-5 min)
```

## 📊 Monitoring du déploiement

Dans Coolify UI, tu peux suivre :
- **Deployment Logs** - Logs en temps réel
- **Build Status** - État du build
- **Health Status** - État des services après deploy

## 🎯 Service UUID

```
Service: grafana-monitoring-stack
UUID: t8sw48oo4wco008wc804ck8o
```

## ⚠️ Notes importantes

- **Retention des données** : Les volumes persistent entre deployments
  - `prometheus-data` - Métriques conservées
  - `loki-data` - Logs conservés
  - `grafana-data` - Dashboards & config conservés

- **Variables d'environnement** : Configurées dans Coolify UI
  - `GRAFANA_ADMIN_PASSWORD`
  - `OPENWEATHER_API_KEY`
  - `SLACK_WEBHOOK_URL`
  - `ALERT_EMAIL_TO`

- **Healthchecks** : Tous les services ont des healthchecks configurés
  - Grafana: `http://localhost:3000/api/health`
  - Prometheus: `http://localhost:9090/-/healthy`
  - Loki: `http://localhost:3100/ready`

## 🔧 Troubleshooting

**Déploiement ne se déclenche pas ?**
1. Vérifier que "Automatic Deployment" est activé
2. Vérifier que le webhook GitHub est configuré
3. Vérifier les logs Coolify : Deployments → View Logs

**Build échoue ?**
1. Vérifier les logs de build dans Coolify
2. Vérifier que les fichiers de config sont présents
3. Vérifier les permissions sur les volumes

**Services ne démarrent pas ?**
1. Vérifier les healthchecks dans `docker-compose-simple.yaml`
2. Vérifier les logs des containers
3. Vérifier que les variables `.env` sont configurées
