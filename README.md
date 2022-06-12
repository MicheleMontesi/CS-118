# Elaborato di Programmazione di Reti A.A. 2022
## Traccia #2
Realizzazione di un applicativo client-server per il trasferimento di file che impieghi il servizio di rete senza connessione (UDP).
**Obiettivi del Software**:
- Connessione client-server senza autenticazione.
- Visualizzazione sul client dei file disponibili sul server.
- *Download* di un file dal server.
- *Upload* di file su server.

##### Specifiche del Protocollo di comunicazione
Il protocollo deve prevedere lo scambio di due tipi di messaggi:
- **Messaggi di comando**:
  - Inviati dal client al server
  - richiesta di esecuzione delle diverse operazioni
- **Messaggi di risposta**:
  - Inviati dal server al client
  - Risposta ad un comando con l'esito dell'operazione

### Funzionalità del Server
- Invio del messaggio di risposta al comando **list** ali client richiedente (+client contemporaneamente).
-Messaggio di risposta contente la *file list*.
- Invio del messaggio di risposta al comando **get** contente il file richiesto, se presente, od un opportuno messaggio di errore.
- Ricezione di un messaggio **put** contenente il file da caricare sul server e l'invio del relativo messaggio di risposta (esito).
  
### Funzionalità del Client
- Invio del messaggio **list** per richiedere la lista dei nomi dei file disponibili.
- Invio del messaggio **get** per ottenere un file
- Ricezione di un file richiesta tramite il mssaggio di get o la gestione dell'eventuale errore.
- invio del messaggio **put** per effettuare l'*upload* di un file sul server.