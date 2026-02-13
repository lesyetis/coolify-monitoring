#!/usr/bin/env python3
"""Generate individual Grafana dashboards for each Coolify project"""

import json
import os

# Coolify projects and their services
PROJECTS = {
    "plane": ["web", "api", "admin", "worker", "beat-worker", "live", "space", "proxy", "plane-db", "plane-redis", "plane-minio", "plane-mq"],
    "twentycrm": ["app", "server", "worker", "browser", "db", "postgres", "postgresql", "redis", "n8n", "n8n-worker", "nocodb", "vexa"],
    "glitchtip": ["web", "worker", "postgres", "redis"],
    "questionnaire": ["heyform", "backend", "frontend", "workers", "redis", "keydb", "mongo", "queue-dashboard"],
    "websitemanager": ["admin", "backend", "worker", "chrome", "redis", "weaviate"],
    "seobrrief": ["backend", "frontend", "redis", "bullmq-board"],
    "wp-translator": ["api", "postgres", "redis", "bull-board"],
    "projetx": ["payload", "mongo"],
    "pj-crawler": ["pagesjaunes-api"],
    "cvme": ["reactive-resume", "chrome", "minio", "postgres", "redis"],
    "design": ["excalidraw"],
    "civico": ["weaviate"],
    "gatsia-review": ["ig0g480oc08gos040sgc8ck0-102259054833", "iw4g4ow00040c88wws408kwc"],
}

def create_service_row(service, project, y_pos):
    """Create a row of panels for a service"""
    return [
        # Status
        {
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {
                "defaults": {
                    "color": {"mode": "thresholds"},
                    "mappings": [
                        {"options": {"0": {"color": "red", "index": 0, "text": "DOWN"}, "1": {"color": "green", "index": 1, "text": "UP"}}, "type": "value"}
                    ],
                    "thresholds": {"mode": "absolute", "steps": [{"color": "red", "value": None}, {"color": "green", "value": 1}]}
                },
                "overrides": []
            },
            "gridPos": {"h": 4, "w": 3, "x": 0, "y": y_pos},
            "id": y_pos * 10 + 1,
            "options": {"colorMode": "background", "graphMode": "none", "justifyMode": "center", "orientation": "auto", "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "textMode": "auto"},
            "pluginVersion": "12.3.3",
            "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "expr": f"up{{container_label_coolify_projectName=\"{project}\", container_label_com_docker_compose_service=\"{service}\"}}", "refId": "A"}],
            "title": f"{service} - Status",
            "type": "stat"
        },
        # CPU
        {
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {
                "defaults": {
                    "color": {"mode": "palette-classic"},
                    "custom": {"axisBorderShow": False, "axisCenteredZero": False, "axisColorMode": "text", "axisLabel": "", "axisPlacement": "auto", "barAlignment": 0, "drawStyle": "line", "fillOpacity": 10, "gradientMode": "none", "hideFrom": {"tooltip": False, "viz": False, "legend": False}, "insertNulls": False, "lineInterpolation": "linear", "lineWidth": 1, "pointSize": 5, "scaleDistribution": {"type": "linear"}, "showPoints": "never", "spanNulls": False, "stacking": {"group": "A", "mode": "none"}, "thresholdsStyle": {"mode": "off"}},
                    "mappings": [],
                    "thresholds": {"mode": "absolute", "steps": [{"color": "green", "value": None}]},
                    "unit": "percent"
                },
                "overrides": []
            },
            "gridPos": {"h": 4, "w": 7, "x": 3, "y": y_pos},
            "id": y_pos * 10 + 2,
            "options": {"legend": {"calcs": ["last"], "displayMode": "list", "placement": "bottom", "showLegend": False}, "tooltip": {"mode": "single", "sort": "none"}},
            "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "expr": f"rate(container_cpu_usage_seconds_total{{container_label_coolify_projectName=\"{project}\", container_label_com_docker_compose_service=\"{service}\"}}[5m]) * 100", "legendFormat": "CPU", "refId": "A"}],
            "title": f"{service} - CPU",
            "type": "timeseries"
        },
        # Memory
        {
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {
                "defaults": {
                    "color": {"mode": "palette-classic"},
                    "custom": {"axisBorderShow": False, "axisCenteredZero": False, "axisColorMode": "text", "axisLabel": "", "axisPlacement": "auto", "barAlignment": 0, "drawStyle": "line", "fillOpacity": 10, "gradientMode": "none", "hideFrom": {"tooltip": False, "viz": False, "legend": False}, "insertNulls": False, "lineInterpolation": "linear", "lineWidth": 1, "pointSize": 5, "scaleDistribution": {"type": "linear"}, "showPoints": "never", "spanNulls": False, "stacking": {"group": "A", "mode": "none"}, "thresholdsStyle": {"mode": "off"}},
                    "mappings": [],
                    "thresholds": {"mode": "absolute", "steps": [{"color": "green", "value": None}]},
                    "unit": "bytes"
                },
                "overrides": []
            },
            "gridPos": {"h": 4, "w": 7, "x": 10, "y": y_pos},
            "id": y_pos * 10 + 3,
            "options": {"legend": {"calcs": ["last"], "displayMode": "list", "placement": "bottom", "showLegend": False}, "tooltip": {"mode": "single", "sort": "none"}},
            "targets": [{"datasource": {"type": "prometheus", "uid": "prometheus"}, "expr": f"container_memory_usage_bytes{{container_label_coolify_projectName=\"{project}\", container_label_com_docker_compose_service=\"{service}\"}}", "legendFormat": "Memory", "refId": "A"}],
            "title": f"{service} - Memory",
            "type": "timeseries"
        },
        # Network
        {
            "datasource": {"type": "prometheus", "uid": "prometheus"},
            "fieldConfig": {
                "defaults": {
                    "color": {"mode": "palette-classic"},
                    "custom": {"axisBorderShow": False, "axisCenteredZero": False, "axisColorMode": "text", "axisLabel": "", "axisPlacement": "auto", "barAlignment": 0, "drawStyle": "line", "fillOpacity": 10, "gradientMode": "none", "hideFrom": {"tooltip": False, "viz": False, "legend": False}, "insertNulls": False, "lineInterpolation": "linear", "lineWidth": 1, "pointSize": 5, "scaleDistribution": {"type": "linear"}, "showPoints": "never", "spanNulls": False, "stacking": {"group": "A", "mode": "none"}, "thresholdsStyle": {"mode": "off"}},
                    "mappings": [],
                    "thresholds": {"mode": "absolute", "steps": [{"color": "green", "value": None}]},
                    "unit": "Bps"
                },
                "overrides": []
            },
            "gridPos": {"h": 4, "w": 7, "x": 17, "y": y_pos},
            "id": y_pos * 10 + 4,
            "options": {"legend": {"calcs": [], "displayMode": "list", "placement": "bottom", "showLegend": True}, "tooltip": {"mode": "multi", "sort": "none"}},
            "targets": [
                {"datasource": {"type": "prometheus", "uid": "prometheus"}, "expr": f"rate(container_network_receive_bytes_total{{container_label_coolify_projectName=\"{project}\", container_label_com_docker_compose_service=\"{service}\"}}[5m])", "legendFormat": "RX", "refId": "A"},
                {"datasource": {"type": "prometheus", "uid": "prometheus"}, "expr": f"rate(container_network_transmit_bytes_total{{container_label_coolify_projectName=\"{project}\", container_label_com_docker_compose_service=\"{service}\"}}[5m])", "legendFormat": "TX", "refId": "B"}
            ],
            "title": f"{service} - Network",
            "type": "timeseries"
        }
    ]

def create_dashboard(project, services):
    """Create a dashboard for a Coolify project"""
    panels = []
    y_pos = 0

    for service in services:
        panels.extend(create_service_row(service, project, y_pos))
        y_pos += 4

    # Add logs panel at the bottom
    panels.append({
        "datasource": {"type": "loki", "uid": "loki"},
        "gridPos": {"h": 12, "w": 24, "x": 0, "y": y_pos},
        "id": y_pos * 10 + 5,
        "options": {"dedupStrategy": "none", "enableLogDetails": True, "prettifyLogMessage": False, "showCommonLabels": False, "showLabels": True, "showTime": True, "sortOrder": "Descending", "wrapLogMessage": False},
        "targets": [{"datasource": {"type": "loki", "uid": "loki"}, "expr": f"{{coolify_project=\"{project}\"}}", "refId": "A"}],
        "title": f"{project.upper()} - All Logs",
        "type": "logs"
    })

    return {
        "annotations": {"list": []},
        "editable": True,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 1,
        "id": None,
        "links": [],
        "panels": panels,
        "schemaVersion": 39,
        "tags": ["coolify", project],
        "templating": {"list": []},
        "time": {"from": "now-1h", "to": "now"},
        "timepicker": {},
        "timezone": "browser",
        "title": f"Coolify - {project.upper()}",
        "uid": f"coolify-{project}",
        "version": 1
    }

def main():
    output_dir = "grafana/provisioning/dashboard-files"
    os.makedirs(output_dir, exist_ok=True)

    for project, services in PROJECTS.items():
        dashboard = create_dashboard(project, services)
        filename = f"{output_dir}/coolify-{project}.json"

        with open(filename, 'w') as f:
            json.dump(dashboard, f, indent=2)

        print(f"✅ Created: {filename} ({len(services)} services)")

    print(f"\n🎉 Generated {len(PROJECTS)} dashboards!")

if __name__ == "__main__":
    main()
