package main

import (
    "fmt"
    "github.com/corazawaf/coraza/v3"
    corazahttp "github.com/corazawaf/coraza/v3/http"
    nethttp "net/http"
    "net/url"
    "io"
)

// Imposta l'URL del server esterno
const externalServer = "http://localhost:5173"

func main() {
    // Configurazione del WAF con una semplice regola
    waf, err := coraza.NewWAF(coraza.NewWAFConfig().
        WithDirectives(`
        SecRuleEngine On
        SecRequestBodyAccess On
        SecRule REQUEST_URI "@rx ^/protected" "id:1,phase:1,deny,status:403"
    `))
    if err != nil {
        panic(err)
    }

    // Crea un nuovo URL per il server esterno
    externalURL, err := url.Parse(externalServer)
    if err != nil {
        panic(err)
    }

    // Wrappare l'handler HTTP con Coraza WAF e inoltrare le richieste al server esterno
    handler := corazahttp.WrapHandler(waf, nethttp.HandlerFunc(func(w nethttp.ResponseWriter, r *nethttp.Request) {
        // Log di debug per vedere cosa viene inoltrato
        fmt.Printf("Forwarding request to %s\n", externalServer)

        // Modifica la richiesta per inoltrarla al server esterno
        r.URL.Scheme = externalURL.Scheme
        r.URL.Host = externalURL.Host
        r.Host = externalURL.Host

        // Inoltra la richiesta al server esterno
        resp, err := nethttp.DefaultTransport.RoundTrip(r)
        if err != nil {
            fmt.Printf("Error forwarding request: %v\n", err) // Log dell'errore
            nethttp.Error(w, "Error forwarding request", nethttp.StatusInternalServerError)
            return
        }
        defer resp.Body.Close()

        // Copia i dati di risposta nel response writer
        w.WriteHeader(resp.StatusCode)
        _, err = io.Copy(w, resp.Body)
        if err != nil {
            fmt.Printf("Error reading response: %v\n", err) // Log dell'errore
            nethttp.Error(w, "Error reading response", nethttp.StatusInternalServerError)
        }
    }))

    // Avviare il server sulla porta 8080
    nethttp.ListenAndServe(":8080", handler)
}
