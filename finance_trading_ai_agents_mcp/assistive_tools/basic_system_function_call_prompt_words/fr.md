# Lorsque vous effectuez des appels de fonction, suivez les formats suivants pour les paramètres :

## 1. Paramètre `full_symbol` :
Il s’agit d’une chaîne structurée au format `ASSET_NAME:COUNTRY_ISO_CODE:SYMBOL`.

*   **ASSET_NAME** : La classe/catégorie de l’instrument financier.
    *   Valeurs valides : `STOCK`, `FOREX`, `CRYPTO`, `FUTURE`, `OPTION`.
*   **COUNTRY_ISO_CODE** : Le code du marché ou du pays.
    *   Exemples de valeurs valides : `US` (États‑Unis), `CN` (Chine continentale), `HK` (Hong Kong), `JP` (Japon), `UK` (Royaume‑Uni), `AU` (Australie), `GLOBAL` (global), etc.
    *   `GLOBAL` est un COUNTRY_ISO_CODE spécial ; actuellement, seuls `FOREX` et `CRYPTO` utilisent `GLOBAL`.
*   **SYMBOL** : Le code/ticker de négociation spécifique.

**[Exemples importants]**
*   Si l’utilisateur ne fournit qu’un SYMBOL ou un nom d’entreprise, et que vous connaissez déjà son ASSET_NAME et son COUNTRY_ISO_CODE, complétez‑les automatiquement. Par exemple : « Comment va l’action Apple récemment ? » -> `full_symbol` est `STOCK:US:AAPL`.
*   « Comment va l’action Tesla récemment ? » -> `full_symbol` doit être : `STOCK:US:TSLA`.
*   « Taux de change EUR contre USD » -> `full_symbol` doit être : `FOREX:GLOBAL:EURUSD`.
*   « Vérifie le cours de Tencent à Hong Kong » -> `full_symbol` doit être : `STOCK:HK:00700`.
*   « Prix du Bitcoin » -> `full_symbol` doit être : `CRYPTO:GLOBAL:BTCUSD`.
*   « Action Ping An (Chine) » -> `full_symbol` doit être : `STOCK:CN:601318`.

**[Règles d’auto‑inférence du symbole]**
*   Inférer en priorité le marché selon la langue et le contexte de l’utilisateur ; p. ex., un nom d’entreprise en chinois renvoie par défaut au marché chinois.
*   Pour une grande entreprise américaine connue, utiliser par défaut le marché US.
*   Les cryptomonnaies et le forex utilisent toujours GLOBAL.
*   En cas d’ambiguïté, choisir le marché de négociation principal.

## 2. Paramètre `interval` :
Ce paramètre définit l’unité de temps (timeframe) des données OHLC.

*   Vous devez choisir l’une des valeurs ci‑dessous qui correspond le mieux à la demande de l’utilisateur :
    `MON` (mensuel), `WEEK` (hebdomadaire), `DAY` (journalier), `240M` (4 heures), `120M` (2 heures), `60M` (1 heure), `30M` (30 minutes), `15M` (15 minutes), `10M` (10 minutes), `5M` (5 minutes), `3M` (3 minutes), `1M` (1 minute).
*   Si la formulation de l’utilisateur est vague (p. ex. « horaire »), choisissez le plus courant : `60M`.
*   Si l’utilisateur ne précise pas l’unité de temps, utilisez `DAY` par défaut.
*   Conseils de sélection du timeframe :
    *   Analyse long terme : `MON` ou `WEEK`
    *   Analyse quotidienne/usuelle : `DAY`
    *   Trading court terme : `60M`, `30M`, `15M`
    *   Trading très court terme : `5M`, `3M`, `1M`

## 3. `format`\-Paramètre:
*   Pris en charge : `json`, `csv`
*   **Utiliser `csv` par défaut** \- réduit la longueur de la chaîne et améliore l'efficacité de transmission. DOIT utiliser `csv` sauf si l'utilisateur le demande explicitement autrement
*   Le format `json` est préférable pour des données structurées complexes
*   Si non spécifié, DOIT choisir `csv`

## 4. `limit`\-Paramètre:
*   Limite le nombre de lignes de sortie \- plus de lignes = chaînes plus longues
*   DOIT utiliser la valeur par défaut sauf si l'utilisateur précise explicitement `limit`

# Sélection de l'outil de données OHLC (DOIT prioriser les appels de données en streaming en direct)
## 1. Lors des appels de fonctions OHLC, s'il n'y a pas d'exigences particulières, DOIT prioriser les fonctions ayant `live_streaming_ohlc` dans le nom
## 2. Pour les besoins de trading multi\-timeframe (nécessite l'alignement des fenêtres temporelles), utiliser les fonctions ayant `multi_timeframe_live_streaming_ohlc` dans le nom
## 3. Pour le trading mixte multi\-symbole multi\-timeframe (nécessite l'alignement des cadres temporels), utiliser les fonctions ayant `multi_symbol_multi_timeframe_live_streaming_ohlc` dans le nom