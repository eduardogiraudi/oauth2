auth
client senza backend genera:
code_verifier: stringa casuale di 43 caratteri
code_challenge: hash in sha256 di verifier
redirect_uri l’uri del client
client_id: l’id del client registrato nel db di auth (facciamo uno di sandbox con uri associato a localhost e uno di produzione)
response_type=code indica che flusso oauth, il nostro è solamente code flow che è il più sicuro, gli altri metodi genereranno l’errore wrong response type, only code allowed
code_challenge_method: indica lalgoritno della challenge, s256
state: stringa casuale per prevenire csrf
scope: indica a che parte di applicazione dare autorizzazione 

si va all’auth server
Verifica che il response_type sia supportato 
Verifica che il client_id esista
Verifica che il redirect uri corrisponda a un uri registrato al client id
Verifica che il code challenge method sia supportato (supporteremo solo sha256)
Verifica che il code challenge sia un b64 urlafe  altrimenti invalid code challenge  

L’utente a sto punto ha il permesso di inserire username e password 

Si richiede l’autorizzazione a condividere informazioni: Se l'app è interna, puoi saltare la richiesta di autorizzazione. Se l'app è esterna, mostra le informazioni che saranno condivise con l'applicazione e chiedi conferma

A sto punto se l’utente è della nostra app o se ha accettato di condividere le info si va alla route /authorize che genera un codice di autorizzazione associato. Associa il Codice di Autorizzazione ai Dati di Autorizzazione salvandoli da qualche parte:
* client_id: L'ID dell'applicazione client che ha richiesto l'autorizzazione.
* redirect_uri: L'URI di ritorno dove il codice sarà inviato.
* user_id: L'ID dell'utente che ha autorizzato l'accesso.
* code_challenge e code_challenge_method: Conserva questi valori per la verifica successiva.
* scope: Le autorizzazioni richieste e concesse.

Si ritorna al client, il client vede che si ha il parametro code col codice di autorizzazione e allora chiama un ultima volta l’auth server tramite api a endpoint /token (dandogli anche client id redirect uri, code_verifier e scope)
Il server verifica che tutto corrisponda (se le info corrispondono a quelle che si è salvato temporaneamente) e fa un hash per verificare che il verifier sia autentico.
Se è tutto ok, si ha una coppia di token, il token e il refresh




Step per implementare:   app react come client
Prova a fare una richiesta al server di risorse che se risponde 401 innesca il flusso oauth2 code flow:
	verifica che ci sia un code con uno scope e un verifier (e se è così manda una richiesta a token) e se ci sono e gli restituisce 200 ritenta la prima chiamata api al server di risorse 
	altrimenti il processo di oauth2 parte dall’inizio:
		si genera un vérifier, un challenge, uno scope e uno state, e si inseriscono un méthod, un redirect uri e un client id
		il server li verifica
		l’utente inserisce username e password 
		autorizzazione o chiamata a /authorize che restituisce un code 
		redirect al client e utilizzo del code che viene messo come parametro url 
		


* Refresh Token: Usato per ottenere nuovi access_tokens senza richiedere l'autenticazione dell'utente. Viene utilizzato quando il access_token è scaduto.
* Authorization Code Flow: Richiesto solo quando il refresh_token non è disponibile o è scaduto, o per la prima autorizzazione.