# Executive Summary: Monte-Carlo-Simulation für Ölindustrie-Investitionen

## Kernbefund

Dieses Projekt entwickelt ein stochastisches ROI-Modell, das die Unsicherheit ölindustrieller Investitionen quantifiziert. Anstatt eines einzigen ROI-Wertes liefert die Monte-Carlo-Simulation eine vollständige Risikoverteilung.

## Die 4 Input-Variablen

| Variable | Verteilung | Grund |
|----------|-----------|-------|
| CAPEX | Dreieck/PERT | Expertenschätzung (Min, Modus, Max) |
| OPEX | Dreieck/PERT | Expertenschätzung (Min, Modus, Max) |
| Fördervolumen | Dreieck/PERT | Geologische Unsicherheit |
| Ölpreis | Lognormal | Finanzmathematischer Standard |

## Wichtigste Ergebnisse (Beispielrechnung)

- **Mean ROI**: ~45% — aber mit breiter Streuung
- **Value at Risk (5%)**: ~-15% — im Worst-5%-Szenario droht Verlust
- **Verlustwahrscheinlichkeit**: ~12% — ca. jedes 8. Szenario ist negativ
- **Haupt-Risikotreiber**: Ölpreis (~55% der ROI-Varianz)

## Warum MCS statt deterministisch?

1. Deterministische Modelle vermitteln Scheingenauigkeit (ein ROI-Wert suggeriert Sicherheit, die nicht existiert)
2. Die ROI-Verteilung zeigt die wahre Risikobandbreite
3. P(ROI < 0) ist entscheidungsrelevanter als ein Punkt-ROI
4. Sensitivitätsanalyse identifiziert den Ölpreis als Hauptrisiko

## Nächste Schritte

1. Korrelationsmodellierung zwischen Variablen
2. Realoptionsansatz (Abbruch-, Erweiterungsoptionen)
3. Validierung mit historischen Projektdaten
4. Portfolio-Simulationen

---

*Elias Corp — April 2026*