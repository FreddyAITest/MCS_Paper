# MCS_Paper — Monte-Carlo-Simulation zur ROI-Bewertung in der Ölindustrie

Ein wissenschaftliches Projekt zur stochastischen Modellierung von Investitionsrenditen (ROI) in der Öl- und Gasindustrie mittels Monte-Carlo-Simulation.

## Projektübersicht

Dieses Projekt entwickelt ein stochastisches ROI-Modell, das die inhärenten Unsicherheiten ölindustrieller Investitionsentscheidungen quantifiziert. Anstatt klassischer deterministischer Single-Point-Schätzungen verwendet das Modell Wahrscheinlichkeitsverteilungen für die vier zentralen Inputgrößen und aggregiert diese über 10.000+ Simulationen zu einer Gesamtrisikoverteilung.

## Repository-Struktur

```
MCS_Paper/
├── README.md                    # Projektübersicht (diese Datei)
├── docs/
│   ├── paper/                    # Wissenschaftliches Paper
│   │   ├── MCS_Paper_Main.md     # Hauptdokument (~15 Seiten)
│   │   └── figures/              # Abbildungen und Diagramme
│   ├── summary/                  # Zusammenfassungen und Notizen
│   │   └── executive_summary.md # Management Summary
│   └── methodology/              # Methodische Grundlagen
│       ├── distributions.md      # Verteilungsannahmen und Begründung
│       └── roi_model.md          # 数学公式 des ROI-Modells
├── src/
│   ├── simulation/
│   │   ├── mcs_engine.py         # Kern-Simulations-Engine
│   │   ├── distributions.py     # Verteilungsdefinitionen
│   │   └── roi_calculator.py    # ROI-Berechnungslogik
│   ├── visualization/
│   │   ├── histogram.py         # ROI-Histogramm-Erstellung
│   │   └── sensitivity.py       # Sensitivitätsanalysen
│   └── data/
│       ├── sample_data.py       # Fiktive/anonymisierte Antragsdaten
│       └── config.py            # Simulationsparameter
├── interactive/                  # Interaktiver Simulator
│   └── simulator.html           # Browser-basierter Prototyp
├── tests/
│   ├── test_distributions.py
│   ├── test_roi_calculator.py
│   └── test_mcs_engine.py
├── requirements.txt             # Python-Abhängigkeiten
└── .github/
    └── workflows/
        └── ci.yml               # Automatisierte Tests
```

## Die 4 stochastischen Inputgrößen

| Variable             | Verteilung          | Begründung                                    |
|----------------------|---------------------|-----------------------------------------------|
| CAPEX (Investition)  | Dreieck / PERT      | Experten-Schätzung (Min, Max, Modus)         |
| OPEX (Betriebskosten)| Dreieck / PERT      | Experten-Schätzung (Min, Max, Modus)         |
| Fördervolumen        | Dreieck / PERT      | Geologisches Risiko, Expertenschätzung        |
| Ölpreis              | Lognormal           | Finanzmathematischer Standard (Rechtsschiefe) |

## ROI-Berechnung

Für jeden Simulationsschritt *i*:

```
ROI_i = (Ölpreis_i × Fördervolumen_i - CAPEX_i - OPEX_i) / CAPEX_i
```

Die Aggregation aller Iterationen ergibt die ROI-Verteilung mit:
- **Erwartungswert (Mean)**: Mittlere Rendite
- **Standardabweichung**: Volatilität/Risiko
- **Value at Risk (VaR)**: Wahrscheinlichkeit eines negativen ROI

## Schnellstart

```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Simulation ausführen (10.000 Iterationen)
python src/simulation/mcs_engine.py --iterations 10000

# Ergebnisse visualisieren
python src/visualization/histogram.py
```

## Team

| Rolle        | Verantwortung                              |
|-------------|--------------------------------------------|
| CEO         | Strategische Ausrichtung, Koordination     |
| CTO         | Technische Architektur, Simulations-Engine |
| CMO         | Kommunikation, Präsentation               |
| Researcher  | Wissenschaftliche Grundlagen, Literatur    |

## Lizenz

Internes Forschungsprojekt — Elias Corp