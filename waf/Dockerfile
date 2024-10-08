# Usa un'immagine base di Go per la build
FROM golang:1.23-alpine AS builder

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file del progetto nella directory di lavoro
COPY go.mod ./
COPY go.sum ./
RUN go mod download

COPY *.go ./

# Costruisci l'applicazione Go
RUN go build -o /coraza-app

# Usa un'immagine più leggera per la fase finale
FROM alpine:latest

# Imposta la directory di lavoro
WORKDIR /root/

# Copia il binario dell'app Go
COPY --from=builder /coraza-app .

# Esponi la porta 8080
EXPOSE 8080

# Esegui l'applicazione
CMD ["./coraza-app"]
