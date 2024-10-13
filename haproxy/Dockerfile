# Usa l'immagine ufficiale di HAProxy
FROM haproxy:2.7

# Copia la configurazione di HAProxy
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY coraza.cfg /etc/haproxy/coraza.cfg

# Espone la porta 80 per il traffico HTTP
EXPOSE 80

# Comando di avvio predefinito
CMD ["haproxy", "-f", "/usr/local/etc/haproxy/haproxy.cfg"]
