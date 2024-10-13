# Usa un'immagine di base di Alpine con Git e Go installati
FROM golang:1.19-alpine3.17 AS builder

# Installa git e wget
RUN apk add --no-cache git wget

# Imposta la directory di lavoro
WORKDIR /build

# Clona il repository di coraza-spoa
RUN git clone https://github.com/corazawaf/coraza-spoa.git .

# Scarica le dipendenze
RUN go mod download

# Costruisci l'eseguibile
RUN go build -o coraza-spoa ./cmd/coraza-spoa/main.go

# Scarica e prepara le regole CRS
RUN wget -O /tmp/crs.tgz https://github.com/coreruleset/coreruleset/archive/refs/tags/v4.0.0-rc1.tar.gz && \
    mkdir crs && \
    tar --strip-components 1 -C crs -xf /tmp/crs.tgz && \
    mv crs/crs-setup.conf.example /build/crs-setup.conf && \
    mv crs/rules /build/rules && \
    rm -rf crs /tmp/crs.tgz

# Scarica il file coraza.conf dal repository GitHub
RUN wget -O /build/coraza.conf https://raw.githubusercontent.com/corazawaf/coraza-spoa/main/docker/coraza-spoa/coraza.conf

# Crea una nuova immagine per l'esecuzione
FROM alpine:3.17

# Crea un utente non privilegiato
RUN addgroup -S coraza-spoa && adduser -S coraza-spoa -G coraza-spoa

# Crea le directory necessarie
RUN mkdir -p /etc/coraza-spoa /var/log/coraza-spoa && chown -R coraza-spoa:coraza-spoa /var/log/coraza-spoa

# Copia l'eseguibile dalla fase di build
COPY --from=builder /build/coraza-spoa /usr/bin/coraza-spoa

# Copia i file di configurazione
COPY --from=builder /build/config.yaml.default /etc/coraza-spoa/config.yaml
COPY --from=builder /build/coraza.conf /etc/coraza-spoa/coraza.conf
COPY --from=builder /build/crs-setup.conf /etc/coraza-spoa/crs-setup.conf
COPY --from=builder /build/rules /etc/coraza-spoa/rules

# Espone la porta 9000
EXPOSE 9000

# Imposta l'utente non privilegiato
USER coraza-spoa

# Comando di avvio
CMD ["/usr/bin/coraza-spoa", "--config", "/etc/coraza-spoa/config.yaml"]
