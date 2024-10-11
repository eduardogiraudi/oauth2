#!/bin/bash

# Avvia HAProxy
echo "Avvio di HAProxy..."
exec haproxy -f /usr/local/etc/haproxy/haproxy.cfg
