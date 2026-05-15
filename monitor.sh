#!/bin/bash

EMAIL="JackieChayan@yandex.ru"
HOSTNAME=$(hostname)

send_alert() {
    SUBJECT="$1"
    MESSAGE="$2"
    echo "$MESSAGE" | mail -s "$SUBJECT" "$EMAIL"
}

MEM_AVAILABLE=$(free -m | awk '/^Mem:/ {print $7}')
MEM_THRESHOLD=100

DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
DISK_THRESHOLD=80

LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $2}' | sed 's/,//')
LOAD_THRESHOLD=2.0

if (( $(echo "$LOAD > $LOAD_THRESHOLD" | bc -l) )); then
    send_alert "HIGH LOAD: $HOSTNAME" "Load (5 min): $LOAD
Threshold: $LOAD_THRESHOLD"
fi

if [ "$MEM_AVAILABLE" -lt "$MEM_THRESHOLD" ]; then
    send_alert "LOW MEMORY: $HOSTNAME" "Available RAM: ${MEM_AVAILABLE} MB
Threshold: ${MEM_THRESHOLD} MB"
fi

if [ "$DISK_USAGE" -gt "$DISK_THRESHOLD" ]; then
    send_alert "DISK ALMOST FULL: $HOSTNAME" "Disk usage: ${DISK_USAGE}%
Threshold: ${DISK_THRESHOLD}%"
fi
