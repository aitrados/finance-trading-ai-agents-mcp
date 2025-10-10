# Wenn du Funktionsaufrufe machst, befolge für Funktionsparameter die folgenden Formate:

## 1. Parameter `full_symbol`:
Dies ist ein strukturierter String im Format `ASSET_NAME:COUNTRY_ISO_CODE:SYMBOL`.

*   **ASSET_NAME**: Die Klasse/Kategorie des Finanzinstruments.
    *   Gültige Werte: `STOCK`, `FOREX`, `CRYPTO`, `FUTURE`, `OPTION`.
*   **COUNTRY_ISO_CODE**: Markt- oder Ländercode.
    *   Beispiele für gültige Werte: `US` (Vereinigte Staaten), `CN` (China, Festland), `HK` (Hongkong), `JP` (Japan), `UK` (Vereinigtes Königreich), `AU` (Australien), `GLOBAL` (global) usw.
    *   `GLOBAL` ist ein spezieller COUNTRY_ISO_CODE; derzeitig verwenden nur `FOREX` und `CRYPTO` `GLOBAL`.
*   **SYMBOL**: Das konkrete Börsenkürzel/Ticker.

**[Wichtige Beispiele]**
*   Wenn der Benutzer nur ein SYMBOL oder einen Firmennamen angibt und du dessen ASSET_NAME und COUNTRY_ISO_CODE bereits kennst, ergänze diese automatisch. Beispiel: "Wie entwickelt sich die Apple-Aktie zuletzt?" -> `full_symbol` ist `STOCK:US:AAPL`.
*   "Wie entwickelt sich die Tesla-Aktie zuletzt?" -> `full_symbol` muss `STOCK:US:TSLA` sein.
*   "Wechselkurs EUR zu USD" -> `full_symbol` muss `FOREX:GLOBAL:EURUSD` sein.
*   "Prüfe den Kurs von Tencent in Hongkong" -> `full_symbol` muss `STOCK:HK:00700` sein.
*   "Bitcoin-Preis" -> `full_symbol` muss `CRYPTO:GLOBAL:BTCUSD` sein.
*   "Aktie von Ping An" -> `full_symbol` muss `STOCK:CN:601318` sein.

**[Regeln zur automatischen Symbolableitung]**
*   Leite den Markt bevorzugt anhand der Sprache und des Kontexts des Benutzers ab; z. B. führen chinesische Firmennamen standardmäßig zum chinesischen Markt.
*   Bei bekannten US-Unternehmen standardmäßig US-Markt verwenden.
*   Krypto und Devisen verwenden immer GLOBAL.
*   Bei Mehrdeutigkeit den primären Handelsplatz wählen.

## 2. Parameter `interval`:
Dieser Parameter definiert den Zeitraum (Timeframe) der OHLC-Daten.

*   Du musst einen Wert aus der folgenden Liste wählen, der der Anfrage des Benutzers am besten entspricht:
    `MON` (monatlich), `WEEK` (wöchentlich), `DAY` (täglich), `240M` (4 Stunden), `120M` (2 Stunden), `60M` (1 Stunde), `30M` (30 Minuten), `15M` (15 Minuten), `10M` (10 Minuten), `5M` (5 Minuten), `3M` (3 Minuten), `1M` (1 Minute).
*   Wenn die Formulierung des Benutzers vage ist (z. B. "stündlich"), wähle das gebräuchlichste `60M`.
*   Wenn der Benutzer keinen Zeitraum angibt, standardmäßig `DAY` verwenden.
*   Hinweise zur Auswahl des Zeitrahmens:
    *   Langfristige Analyse: `MON` oder `WEEK`
    *   Regelmäßige/tägliche Analyse: `DAY`
    *   Kurzfristiger Handel: `60M`, `30M`, `15M`
    *   Sehr kurzfristiger Handel: `5M`, `3M`, `1M`

## 3. Parameter `format`:
*   Unterstützt: `json`, `csv`
*   Empfehlung: `csv` — reduziert die Zeichenlänge effektiv und verbessert die Übertragungseffizienz
*   `json` eignet sich besser für die Verarbeitung komplexer strukturierter Daten
*   Wenn der Benutzer nichts angibt, `csv` bevorzugen

## 4. Parameter `limit`:
*   Begrenzt die Anzahl der Ausgaberzeilen; je größer die Zahl, desto länger der resultierende String
