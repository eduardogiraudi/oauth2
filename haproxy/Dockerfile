
FROM haproxy:2.4-alpine


COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY entrypoint.sh .
EXPOSE 80

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
