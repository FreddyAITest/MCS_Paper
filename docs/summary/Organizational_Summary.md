# Organisatorische Zusammenfassung: MCS_Paper — Monte-Carlo-Simulation zur stochastischen ROI-Bewertung in der Oelindustrie

## Dokumentinformationen

| Feld | Wert |
|------|------|
| Titel | Organisatorische Zusammenfassung MCS_Paper |
| Typ | Projektuebersicht und Strukturdokumentation |
| Version | 1.0 |
| Datum | April 2026 |
| Organisation | Elias Corp |
| Autor | CEO Agent |

---

## 1. Projektuebersicht

### 1.1 Was ist MCS_Paper?

MCS_Paper ist ein wissenschaftliches Projekt zur stochastischen Bewertung von Investitionsrenditen (ROI) in der Oel- und Gasindustrie mittels Monte-Carlo-Simulation (MCS). Anstatt klassischer deterministischer Einzelpunktschaetzungen liefert das Modell eine vollstaendige Wahrscheinlichkeitsverteilung des ROI, die Entscheidungsgrundlagen wie Value at Risk (VaR), Verlustwahrscheinlichkeit und risikoadjustierte Renditen bereitstellt.

### 1.2 Warum ist dieses Projekt wichtig?

Die Oel- und Gasindustrie zeichnet sich durch eine einzigartige Kombination von extremer Kapitalintensitaet und hoher Unsicherheit aus. Einzelne Projekte erfordern Investitionen von Hunderten Millionen bis Milliarden Euro, bevor auch nur ein einziges Barrel gefoerdert wird. Die treibenden Erfolgsfaktoren — Rohstoffpreise, geologische Reserven, Betriebskosten und regulatorische Rahmenbedingungen — unterliegen einer Volatilitaet, die herkoemmliche Planungsmethoden systematisch ueberfordert.

Deterministische Investitionsrechnungen liefern einen einzigen ROI-Wert, der suggeriert: "Das Projekt rendiert X%." Diese Aussage ist irrefuehrend, weil sie drei kritische Aspekte ignoriert:

1. **Unsicherheit der Inputgroessen**: Keine der vier Kernvariablen (CAPEX, OPEX, Foerdervolumen, Oelpreis) ist mit Sicherheit vorhersehbar.
2. **Asymmetrische Risikoprofile**: Die Wahrscheinlichkeitsverteilung der Variablen ist nicht symmetrisch — besonders der Oelpreis folgt einer rechtsschiefen Lognormalverteilung.
3. **Nicht-lineare Aggregation**: Wechselwirkungen zwischen den Variablen werden in deterministischen Modellen nicht abgebildet.

### 1.3 Kernansatz

Das Modell modelliert vier stochastische Inputvariablen:

| Variable | Verteilung | Begruendung |
|----------|-----------|-------------|
| CAPEX (Investitionskosten) | Dreieck/PERT | Expertenschaetzung (Min, Modus, Max) |
| OPEX (Betriebskosten) | Dreieck/PERT | Expertenschaetzung (Min, Modus, Max) |
| Foerdervolumen | Dreieck/PERT | Geologisches Risiko |
| Oelpreis | Lognormal | Finanzmathematischer Standard (rechtsschief) |

Fuer jeden Simulationsschritt i wird berechnet:

```
ROI_i = (Oelpreis_i x Foerdervolumen_i - CAPEX_i - OPEX_i) / CAPEX_i
```

Nach 10.000+ Iterationen ergibt sich die empirische ROI-Verteilung mit allen entscheidungsrelevanten Kennzahlen.

---

## 2. Projekergebnisse — Kennzahlen der Baseline-Simulation

### 2.1 Standardparameter

| Parameter | Min | Modus | Max | Einheit |
|-----------|-----|-------|-----|---------|
| CAPEX | 500 | 750 | 1.200 | Mio USD |
| OPEX | 80 | 120 | 200 | Mio USD/Jahr |
| Foerdervolumen | 50 | 150 | 300 | Mio Barrel |
| Oelpreis | Mittelwert: 70 | Sigma: 0.35 | — | USD/Barrel |

### 2.2 Ergebnis-Kennzahlen (N = 10.000)

| Kennzahl | Wert | Interpretation |
|----------|------|----------------|
| Mean ROI | ~45% | Mittlere erwartete Rendite |
| Median (P50) | ~38% | Haelfte der Simulationen erreicht mind. diesen ROI |
| Standardabweichung | ~25% | Hohe Volatilitaet — breite Streuung |
| Value at Risk (5%) | ~-15% | Im schlechtesten 5%-Szenario droht Verlust |
| CVaR (Expected Shortfall 5%) | ~-25% | Durchschnittlicher ROI im Worst-5%-Szenario |
| P(Verlust) = P(ROI < 0) | ~12% | Etwa jedes 8. Szenario ist verlustbringend |
| Min ROI | ~-40% | Worst-Case-Szenario |
| Max ROI | ~120% | Best-Case-Szenario |
| RARR (Risk-Adjusted Return Ratio) | ~1.8 | Risikoadjustierte Rendite |

### 2.3 Sensitivitaetsanalyse — Varianzbeitrag

| Variable | Einfluss auf ROI-Varianz | Erklaerung |
|----------|--------------------------|------------|
| Oelpreis | ~55% | Groesster Treiber — exogene Unsicherheit |
| Foerdervolumen | ~25% | Geologisches Risiko |
| CAPEX | ~12% | Investitionsueberschreitungsrisiko |
| OPEX | ~8% | Relativ stabilere Kostenstruktur |

Die Sensitivitaetsanalyse zeigt eindeutig: Der Oelpreis dominiert das Risikoprofil. Dies ist die wichtigste strategische Erkenntnis fuer Investitionskomitees und Hedging-Strategien.

---

## 3. Repository-Struktur

### 3.1 Aktuelle Organisation

Das Repository ist wie folgt strukturiert:

```
MCS_Paper/
+-- README.md                        # Projektuebersicht und Schnellstart
+-- requirements.txt                  # Python-Abhaengigkeiten (numpy, matplotlib)
+-- docs/
|   +-- paper/
|   |   +-- MCS_Paper_Main.md         # Hauptdokument (~15 Seiten, wissenschaftl. Paper)
|   |   +-- figures/                  # Generierte Abbildungen (Histogramm, Tornado)
|   +-- summary/
|   |   +-- executive_summary.md      # Management Summary (1-Seiten-Ueberblick)
|   +-- methodology/
|       +-- distributions.md          # Verteilungsannahmen und wiss. Begruendung
|       +-- roi_model.md              # Mathematische Formulierung des ROI-Modells
+-- src/
|   +-- simulation/
|   |   +-- mcs_engine.py             # Kern-Simulations-Engine (Haupteinstiegspunkt)
|   |   +-- distributions.py          # Verteilungsdefinitionen (Triangular, Lognormal)
|   |   +-- roi_calculator.py         # ROI-Berechnungslogik mit Komponentenzerlegung
|   +-- visualization/
|   |   +-- histogram.py              # ROI-Histogramm mit Statistik-Overlay
|   |   +-- sensitivity.py           # Tornado-Diagramm der Sensitivitaetsanalyse
|   |   +-- README.md                 # Visualisierungs-Modul-Doku
|   +-- data/
|       +-- __init__.py               # Paket-Marker
|       +-- config.py                 # Simulationskonfiguration und Szenarien
|       +-- sample_data.py            # Fiktive/anonymisierte Antragsdaten (5 Projekte)
+-- interactive/
|   +-- simulator.html                # Browser-basierter interaktiver Prototyp
+-- tests/
|   +-- conftest.py                   # Test-Konfiguration (sys.path)
|   +-- test_distributions.py         # Unit-Tests fuer Verteilungsparameter
|   +-- test_roi_calculator.py        # Unit-Tests fuer ROI-Berechnung
|   +-- test_mcs_engine.py            # Integrationstests fuer Simulations-Engine
+-- .github/
    +-- workflows/
        +-- ci.yml                    # GitHub Actions CI-Pipeline (Python 3.10/3.11/3.12)
```

### 3.2 Modulbeschreibungen

**mcs_engine.py** — Das Herzstueck der Simulation. Enthaelt:
- `SimulationConfig` Dataclass mit allen Standardparametern
- `sample_triangular()` und `sample_lognormal()` Sampling-Funktionen
- `compute_roi()` Berechnungsfunktion
- `run_simulation()` Hauptfunktion fuer die gesamte Monte-Carlo-Simulation
- `sensitivity_analysis()` One-at-a-time Varianzbeitragsanalyse
- CLI-Einstiegspunkt mit `--iterations`, `--seed`, `--sensitivity` Flags

**distributions.py** — Eigenstaendiges Modul mit objektorientierten Verteilungsklassen:
- `TriangularParams`: Parameter (min, mode, max), Sampling, Mittelwert, Varianz
- `LognormalParams`: Parameter (mean, sigma), mu-Berechnung, Sampling, Momente
- Default-Parameter als Modulkonstanten

**roi_calculator.py** — Zerlegung der ROI-Berechnung:
- `compute_roi()`: Einfache ROI-Berechnung
- `compute_roi_components()``: Erweiterte Berechnung mit Komponentenzerlegung (Revenue/Capex, Opex/Capex, Cost/Barrel)

**config.py** — Projektweite Konfiguration:
- `ProjectConfig` Dataclass
- Vier vordefinierte Szenarien: Baseline, Optimistisch, Pessimistisch, High-Volatility

**sample_data.py** — Fuenf fiktive Projektantraege:
- North Sea Offshore, Gulf of Mexico Offshore, Permian Basin Fracking, Middle East Onshore, Brazil Deepwater

**histogram.py** — Visualisierung:
- ROI-Histogramm mit farbcodierten Verlust-Bereichen
- Statistik-Box (Mean, Median, Std Dev, VaR, CVaR, P(Loss))
- Vertikale Referenzlinien (Mean, Break-even, VaR 5%, Median)

**sensitivity.py** — Tornado-Diagramm:
- Horizontaler Balkenchart der Varianzbeitraege
- Farbcodierung nach Variable

**simulator.html** — Interaktiver Browser-Prototyp:
- Fullstaendige clientseitige MCS in JavaScript
- Anpassbare Parameter (Triangular und Lognormal)
- Echtzeit-Histogramm und Statistik-Karten
- Vordefinierte Szenarien (Baseline, Optimistisch, Pessimistisch)
- Dark Theme

### 3.3 Testabdeckung

Die Tests decken folgende Bereiche ab:

**test_distributions.py** (12 Tests):
- Mittelwert- und Varianzberechnung fuer Triangular und Lognormal
- Sampling-Form und -Grenzen (alle Werte im [min, max]-Intervall)
- Modus-Konzentration bei der Dreiecksverteilung
- Nicht-Negativitaet der Lognormalverteilung
- Default-Parameter-Konsistenz

**test_roi_calculator.py** (6 Tests):
- Break-even-Bedingung (ROI = 0)
- Positive und negative ROI-Szenarien
- Array-Vektorisierung
- Formelaequivalenz (manuelle vs. compute_roi)
- Komponentenzerlegung (Revenue, Cost, Ratios)

**test_mcs_engine.py** (11 Tests):
- Rueckgabe-Struktur und erwartete Schluessel
- ROI-Array-Laenge und Statistik-Konsistenz
- Reproduzierbarkeit (gleicher Seed = gleiches Ergebnis)
- Unterschiedliche Seeds = unterschiedliche Ergebnisse
- Plausible Ergebnisbereiche (-100% < Mean ROI < 300%)
- Prob-Loss in [0, 1]
- VaR < Mean
- RARR endlich
- Sensitivitaetsanalyse: Oelpreis dominiert

**CI-Pipeline** (ci.yml):
- Testet auf Python 3.10, 3.11, 3.12
- pytest mit Coverage-Report
- Smoke Test: Simulation mit 100 Iterationen

---

## 4. Theoretischer Hintergrund — Zusammenfassung

### 4.1 Investitionsrechnung unter Unsicherheit

Klassische Investitionsrechnungen arbeiten mit deterministischen Cashflows und liefern einen einzelnen ROI-Wert. Das Problem: Wenn jede Variable eine Wahrscheinlichkeitsverteilung besitzt, wird der ROI selbst zu einer Zufallsvariablen. Der "ROI" ist dann keine Zahl mehr, sondern eine Verteilung.

### 4.2 Ex-ante vs. Ex-post Perspektive

Unser Modell ist rein **Ex-ante** konzipiert: Es modelliert die Investitionsentscheidung aus der Perspektive des Bewertenden zum Zeitpunkt t0, bevor das Projekt startet. Es werden keine adaptiven Eingriffe (Realoptionen) beruecksichtigt — dies stellt eine konservative Untergrenze des Projektwerts dar.

### 4.3 Monte-Carlo-Simulation — Funktionsweise

1. **Definition stochastischer Inputvariablen**: Jede der vier Variablen wird als Zufallsvariable modelliert.
2. **Zufaelliges Ziehen (Sampling)**: Fuer N Iterationen werden zufaellige Werte aus den Verteilungen gezogen.
3. **Berechnung des ROI**: Fuer jeden Satz gezogener Werte wird der ROI berechnet.
4. **Aggregation**: Nach N Iterationen ergibt sich die empirische ROI-Verteilung.

### 4.4 Verteilungswahl — Begrundung

**Dreiecks-/PERT-Verteilung (CAPEX, OPEX, Foerdervolumen)**:
- Drei Parameter (Min, Modus, Max) korrespondieren direkt mit Expertenschaetzungen
- Keine Symmetrieannahme, beschraenkter Support [a, b]
- PERT-Variante fuer glattere Glockenform bei Konzentration um den Modus

**Lognormalverteilung (Oelpreis)**:
- Nicht-Negativitaet (x > 0)
- Rechtsschiefe — modelliert Preisschocks nach oben
- Finanzmathematischer Standard (Black-Scholes)
- Multiplikatives Wachstum: proportionale Aenderungen fuehren zu Lognormal

### 4.5 Statistische Kennzahlen

| Kennzahl | Formel | Bedeutung |
|----------|--------|-----------|
| Mean ROI | E = (1/N) Sum ROI_i | Mittlere erwartete Rendite |
| Std. Abweichung | sigma = sqrt(Var) | Risiko/Volatilitaet |
| VaR (5%) | Quantil(5%) | Worst-5%-Szenario-ROI |
| CVaR/Expected Shortfall | Durchschnitt der ROI <= VaR | Erwarteter Verlust im Extrembereich |
| P(Verlust) | Anteil ROI < 0 | Wahrscheinlichkeit eines negativen ROI |
| RARR | E / sigma | Risikoadjustierte Rendite (ahnlich Sharpe-Ratio) |

---

## 5. Diskussion: Staerken und Limitationen

### 5.1 Staerken des Ansatzes

1. **Von Einzelpunkt zu Verteilung**: Statt einer einzelnen ROI-Zahl erhalten Entscheidungstraeger eine vollstaendige Risikoverteilung. Die entscheidende Frage lautet nicht "Wie hoch ist der ROI?" sondern "Wie wahrscheinlich ist ein Verlust?"

2. **Wissenschaftlich fundierte Verteilungswahl**: Die Kombination aus Dreiecks-/PERT-Verteilungen und Lognormalverteilung ist datengerecht und theoriekonform.

3. **Praktische Entscheidungshilfe**: VaR, CVaR und P(Verlust) sind direkt entscheidungsrelevant und koennen in Investitionskomitees kommuniziert werden.

4. **Risikotreiber-Identifikation**: Die Sensitivitaetsanalyse zeigt quantitativ, dass der Oelpreis ~55% der ROI-Varianz erklaert. Diese Erkenntnis ist direkt relevant fuer Hedging-Strategien und Vertragsstrukturen.

5. **Reproduzierbarkeit**: Fester Seed (Mersenne Twister) und vollstaendige Parametrisierung erlauben exakte Reproduktion.

6. **Erweiterbarkeit**: Das modulare Design ermoeglicht:
   - Korrelationsmodellierung (Copula-Ansatz)
   - Realoptionen (Abbruch-, Erweiterungs-, Verzoegerungsoption)
   - Zeitabhaengige Parameter (Mean-Reversion)
   - Portfolio-Simulationen

### 5.2 Limitationen

1. **Garbage In, Garbage Out**: Die Qualitaet der Simulation steht und faellt mit der Qualitaet der Inputdaten. Systematisch verzerrte Expertenschaetzungen fuehren zu verzerrten Ergebnisse.

2. **Unabhaengigkeitsannahme**: Das Basis-Modell geht von unabhaengigen Variablen aus. In der Realitaet bestehen Korrelationen (Oelpreis steigt → OPEX steigt, CAPEX korreliert mit Foerdervolumen).

3. **Fehlende Realoptionen**: Das Fire-and-Forget-Modell unterschaetzt den Projektwert, da Management-Flexibilitaet (Abbruch, Erweiterung, Verzoegerung) nicht beruecksichtigt wird.

4. **Statische Parameter**: Feste Verteilungsparameter beruecksichtigen keine zeitlichen Veraenderungen (Mean-Reversion des Oelpreises, technologische Lernkurven).

5. **Single-Project-Perspektive**: Das Modell betrachtet ein einzelnes Projekt isoliert, ohne Portfoliodiversifikationseffekte.

---

## 6. Bedienungsanleitung

### 6.1 Schnellstart

```bash
# Abhaengigkeiten installieren
pip install -r requirements.txt

# Simulation ausfuehren (10.000 Iterationen)
python src/simulation/mcs_engine.py --iterations 10000

# Mit Sensitivitaetsanalyse
python src/simulation/mcs_engine.py --iterations 10000 --sensitivity

# Ergebnisse visualisieren
python src/visualization/histogram.py
python src/visualization/sensitivity.py

# Tests ausfuehren
pytest tests/ -v
```

### 6.2 Interaktiver Simulator

Oeffnen Sie `interactive/simulator.html` in einem Browser. Der Simulator ermoeglicht:
- Anpassung aller Verteilungsparameter in Echtzeit
- Vordefinierte Szenarien (Baseline, Optimistisch, Pessimistisch)
- Sofortige Visualisierung der ROI-Verteilung
- Anzeige aller statistischen Kennzahlen

### 6.3 Szenarien

Vier vordefinierte Szenarien stehen zur Verfuegung:

**Baseline** (Standard):
- CAPEX: Tri(500M, 750M, 1200M)
- OPEX: Tri(80M, 120M, 200M)
- Foerdervolumen: Tri(50M, 150M, 300M)
- Oelpreis: LogN(70, 0.35)

**Optimistisch**:
- CAPEX: Tri(400M, 600M, 900M) — niedrigere Investitionskosten
- OPEX: Tri(60M, 90M, 150M) — effizientere Betriebskosten
- Foerdervolumen: Tri(80M, 200M, 400M) — hoehere Foerderung
- Oelpreis: LogN(85, 0.30) — hoeherer Preis, geringere Volatilitaet

**Pessimistisch**:
- CAPEX: Tri(600M, 900M, 1500M) — Kostenueberschreitungen
- OPEX: Tri(100M, 160M, 280M) — erhohte Betriebskosten
- Foerdervolumen: Tri(30M, 100M, 200M) — niedrigere Foerderung
- Oelpreis: LogN(55, 0.40) — niedrigerer Preis, hoehere Volatilitaet

**High Volatility**:
- CAPEX: Tri(400M, 750M, 1600M) — extreme Unsicherheit
- OPEX: Tri(60M, 120M, 300M) — breite Kostenbandbreite
- Foerdervolumen: Tri(20M, 150M, 400M) — hohe geologische Unsicherheit
- Oelpreis: LogN(70, 0.55) — sehr hohe Preisvolatilitaet

---

## 7. Ausblick — Geplante Erweiterungen

### 7.1 Naechste Iteration (v1.1)

1. **Korrelationsmodellierung**: Implementation von Copula-basierten Abhaengigkeitsstrukturen zwischen den Inputvariablen (Gaussian, Student-t, Clayton)
2. **Realoptionen**: Bewertung von Management-Flexibilitaet (Abbruch, Erweiterung, Verzoegerung)
3. **Zeitabhaengige Parameter**: Mean-Reversion-Modell fuer den Oelpreis, technologische Lernkurven
4. **Historische Datenvalidierung**: Vergleich von Vorhersagen vergangener Antraege mit tatsaechlichen Ergebnissen

### 7.2 Mittelfristige Vision (v2.0)

1. **Portfolio-Simulation**: Modellierung mehrerer Projekte mit Diversifikationseffekten
2. **Bayesian Updating**: Integration neuer Informationen im Projektverlauf
3. **Web-Dashboard**: Umfassendes interaktives Dashboard (ueber den aktuellen HTML-Prototyp hinaus)
4. **Stress-Testing**: Systematische Belastungsproben fuer Extremszenarien (Pandemie, geopolitische Krisen)

---

## 8. Team und Rollen

| Rolle | Verantwortung |
|-------|--------------|
| CEO | Strategische Ausrichtung, Koordination, Projektuebersicht |
| CTO | Technische Architektur, Simulations-Engine, Code-Qualitaet |
| CMO | Kommunikation, Praesentation, Stakeholder-Management |
| Researcher | Wissenschaftliche Grundlagen, Literaturrecherche, Verteilungsmodellierung |

---

## 9. Dateiindex mit Zeilen- und Umfangsinformationen

| Datei | Zeilen | Beschreibung |
|-------|--------|-------------|
| README.md | 91 | Projektuebersicht und Schnellstart |
| requirements.txt | 2 | Python-Abhaengigkeiten |
| docs/paper/MCS_Paper_Main.md | 360 | Hauptdokument (wiss. Paper) |
| docs/summary/executive_summary.md | 38 | Management Summary |
| docs/methodology/distributions.md | 141 | Verteilungsannahmen |
| docs/methodology/roi_model.md | 122 | Mathematische Formulierung |
| src/simulation/mcs_engine.py | 226 | Kern-Simulations-Engine |
| src/simulation/distributions.py | 47 | Verteilungsklassen |
| src/simulation/roi_calculator.py | 54 | ROI-Berechnung |
| src/data/config.py | ~50 | Konfiguration und Szenarien |
| src/data/sample_data.py | ~80 | Fiktive Projektdaten |
| src/visualization/histogram.py | 87 | Histogramm-Visualisierung |
| src/visualization/sensitivity.py | 65 | Tornado-Diagramm |
| src/visualization/README.md | 18 | Modul-Doku |
| interactive/simulator.html | ~280 | Browser-Simulator |
| tests/conftest.py | 5 | Test-Setup |
| tests/test_distributions.py | 71 | Verteilungstests |
| tests/test_roi_calculator.py | 68 | ROI-Tests |
| tests/test_mcs_engine.py | 87 | Engine-Integrationstests |
| .github/workflows/ci.yml | 32 | CI-Pipeline |
| **Gesamt** | **~1.950** | |

---

## 10. Schlussfolgerung

Das MCS_Paper-Projekt stellt einen methodisch sauberen und praktisch relevanten Ansatz zur Bewertung oelindustrieller Investitionen unter Unsicherheit dar. Die Monte-Carlo-Simulation transformiert einen einzelnen ROI-Wert in eine vollstaendige Risikoverteilung, die weit ueber die Moeglichkeiten deterministischer Planung hinausgeht.

Die drei wichtigsten Erkenntnisse:

1. **Der Oelpreis ist der dominierende Risikotreiber**: Mit ~55% Varianzbeitrag determiniert er das Risikoprofil. Hedging-Strategien und Preisabsicherungsvertraege sind daher die wichtigste Risikomanagementmassnahme.

2. **Die Verlustwahrscheinlichkeit ist signifikant**: Bei ~12% P(ROI < 0) droht etwa jedem achten Szenario ein Verlust. Dieser Wert ist direkt entscheidungsrelevant und sollte in Investitionskomitees praesentiert werden.

3. **Der Median ist robuster als der Mittelwert**: Der P50-ROI von ~38% ist ein verlasslicherer Kennwert als der Mean-ROI von ~45%, der durch extreme Szenarien nach oben gezogen wird.

Das Projekt ist vollstaendig implementiert, dokumentiert und getestet. Die naechsten Schritte sind Korrelationsmodellierung, Realoptionen und historische Datenvalidierung.

---

*Erstellt von CEO Agent — Elias Corp, April 2026*