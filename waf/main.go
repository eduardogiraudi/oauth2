package main

import (
    "log"
    "os"
    "github.com/corazawaf/coraza/v3"
    corazahttp "github.com/corazawaf/coraza/v3/http"
    nethttp "net/http"
    "net/url"
    "io"
)

const externalServer = "http://localhost:8080"
const logFilePath = "/var/log/coraza/audit.log"

func main() {
    // Imposta il logger per scrivere nel terminale e nel file di log
    logFile, err := os.OpenFile(logFilePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
    if err != nil {
        log.Fatalf("Errore durante la creazione del file di log: %v", err)
    }
    defer logFile.Close()
    log.SetOutput(logFile)

    // Log di avvio
    log.Println("Inizializzazione del WAF e server...")

    // Crea una nuova configurazione WAF con logging
    waf, err := coraza.NewWAF(coraza.NewWAFConfig().WithDirectives(`
        SecRuleEngine On
        SecAuditEngine RelevantOnly
        SecAuditLog /var/log/coraza/audit.log
        SecDebugLog /var/log/coraza/debug.log
        SecDebugLogLevel 5

        SecAuditLogParts ABDEFHZ
        Include /rules/*.conf
    `))
    if err != nil {
        log.Fatalf("Errore durante la creazione del WAF: %v", err)
    }

    externalURL, err := url.Parse(externalServer)
    if err != nil {
        log.Fatalf("Errore nel parsing dell'URL esterno: %v", err)
    }

    handler := corazahttp.WrapHandler(waf, nethttp.HandlerFunc(func(w nethttp.ResponseWriter, r *nethttp.Request) {
        log.Printf("Forwarding request to %s\n", externalServer)

        // Modifica della richiesta per il server esterno
        r.URL.Scheme = externalURL.Scheme
        r.URL.Host = externalURL.Host
        r.Host = externalURL.Host

        // Inoltro della richiesta
        resp, err := nethttp.DefaultTransport.RoundTrip(r)
        if err != nil {
            log.Printf("Errore durante il forwarding della richiesta: %v\n", err)
            w.WriteHeader(nethttp.StatusInternalServerError)
            _, _ = w.Write([]byte("Errore interno durante il forwarding della richiesta"))
            return
        }
        defer resp.Body.Close()

        // Scrive la risposta al client
        w.WriteHeader(resp.StatusCode)
        _, err = io.Copy(w, resp.Body)
        if err != nil {
            log.Printf("Errore durante la lettura della risposta: %v\n", err)
            w.WriteHeader(nethttp.StatusInternalServerError)
            _, _ = w.Write([]byte("Errore interno durante la lettura della risposta"))
        }
    }))

    // Log di avvio del server
    log.Println("Avvio del server sulla porta 8010...")
    
    if err := nethttp.ListenAndServe(":8010", handler); err != nil {
        log.Fatalf("Errore durante l'avvio del server: %v", err)
    }

}
