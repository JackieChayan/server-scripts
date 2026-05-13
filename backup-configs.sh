#!/bin/bash
# Скрипт бэкапа важных конфигов
BACKUP_DIR=~/backups/configs-$(date +%Y-%m-%d)
mkdir -p "$BACKUP_DIR"

echo "Бэкаплю конфиги в $BACKUP_DIR ..."

# Копируем конфиги
sudo cp /etc/nginx/sites-available/default "$BACKUP_DIR/nginx-default"
sudo cp /etc/ssh/sshd_config "$BACKUP_DIR/sshd_config"
sudo cp /etc/ufw/user.rules "$BACKUP_DIR/ufw-user.rules"
cp ~/docker-demo/docker-compose.yml "$BACKUP_DIR/docker-compose.yml" 2>/dev/null || echo "  docker-compose.yml не найден, пропускаю"

# Создаём архив
tar -czf "$BACKUP_DIR.tar.gz" -C ~/backups "configs-$(date +%Y-%m-%d)" && rm -rf "$BACKUP_DIR"

echo "Готово! Архив: $BACKUP_DIR.tar.gz"
