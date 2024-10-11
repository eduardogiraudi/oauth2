package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/corazawaf/coraza/v3"
	corazahttp "github.com/corazawaf/coraza/v3/http"
)

func main() {
	// Creazione del WAF e caricamento delle Core Rule Set
	waf, err := coraza.NewWAF(coraza.NewWAFConfig().
		WithDirectives(`
			Include coreruleset/crs-setup.conf.example
			Include coreruleset/rules/*.conf
		`),
	)
	if err != nil {
		log.Fatalf("Errore durante la creazione del WAF: %v", err)
	}

	// Creazione di un handler HTTP e wrappato con Coraza
	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Richiesta accettata. Nessuna violazione rilevata.")
	})

	// Uso corretto del WrapHandler: mux come gestore HTTP, WAF per la protezione
	handler := corazahttp.WrapHandler(waf, mux)

	// Avvio del server
	log.Println("Server in ascolto sulla porta 8080...")
	if err := http.ListenAndServe(":8080", handler); err != nil {
		log.Fatalf("Errore durante l'avvio del server: %v", err)
	}
}
