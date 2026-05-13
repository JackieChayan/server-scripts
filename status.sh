#!/bin/bash
# Мой первый скрипт — информация о сервере
echo "===== СЕРВЕР: $(hostname) ====="
echo "Время: $(date)"
echo "Аптайм: $(uptime -p)"
echo "Память:"
free -h | grep "Mem"
echo "Диск:"
df -h / | tail -1
echo "Docker-контейнеры:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "  Docker не запущен или нет контейнеров"
# Версия 1.1
