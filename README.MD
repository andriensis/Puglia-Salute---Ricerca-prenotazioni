# Puglia Salute - Ricerca Prenotazioni

Script in Python che permette di ricercare le prime date disponibili per prenotazione di una ricetta dematerializzata dal portale Puglia Salute.

Lo script restituisce in console i seguenti dati per la prima prenotazione disponibile a partire dal giorno successivo: struttura, data e ora prima prenotazione disponibile
## Installazione

Installa le dipendenze di Python

```sh
pip3 install -r requirements.txt
```

Modifica il file .env inserendo i dati

NB: per il valore di **TESSERA_SANITARIA** bisogna omettere il prefisso **8038000**


```sh
CODICE_FISCALE=***
TESSERA_SANITARIA=***
NUMERO_RICETTA=***
NUMERO_TELEFONO=***
EMAIL=***
```

Esegui lo script

```sh
python3 crawl.py
```

## Esempio risultato

```
Loading page
Verifying identity
Entering patient data
Looking for reservations...
Reservations loaded:

POL. BRINDISI: 29/09/2022 - 16:30
OSPEDALE "DI VENERE" BARI: 05/10/2022 - 16:00
OSPEDALE SS. ANNUNZIATA - TARANTO: 18/11/2022 - 12:30
OSP. ANDRIA "L. BONOMO": 16/03/2023 - 11:10
```