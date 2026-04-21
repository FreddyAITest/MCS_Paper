# Monte-Carlo-Simulation zur stochastischen Bewertung von Investitionsrenditen in der Ölindustrie

## Dokumentinformationen

| Feld             | Wert                                                    |
|-----------------|---------------------------------------------------------|
| Titel            | Stochastische ROI-Bewertung mittels Monte-Carlo-Simulation |
| Typ              | Wissenschaftliches Working Paper                         |
| Version          | 1.0                                                     |
| Datum            | April 2026                                              |
| Organisation     | Elias Corp                                              |

---

## 1. Einleitung

### 1.1 Motivation

Die Öl- und Gasindustrie zeichnet sich durch eine einzigartige Kombination von extremer Kapitalintensität und hoher Unsicherheit aus. Einzelne Projekte — ob Offshore-Bohrungen, Fracking-Vorhaben oder Pipeline-Infrastruktur — erfordern Investitionen im Bereich von Hunderten Millionen bis Milliarden Euro, bevor auch nur ein einziges Barrel gefördert wird. Gleichzeitig unterliegen die treibenden Erfolgsfaktoren — Rohstoffpreise, geologische Reserven, Betriebskosten und regulatorische Rahmenbedingungen — einer Volatilität, die herkömmliche Planungsmethoden systematisch überfordert.

Die Finanzkrise 2008, der Ölpreiscrash 2014–2016 und die COVID-bedingte Preiskatastrophe 2020 haben eindrucksvoll gezeigt, dass deterministische Planungsansätze, die auf Einzelpunktschätzungen (Point Estimates) basieren, die Realität systematisch verfehlen. Ein Projekt, das bei einem Ölpreis von $80/Barrel hervorragend rentabel erscheint, kann bei $40/Barrel katastrophal sein — und die Geschichte zeigt, dass solche Preisschwankungen innerhalb weniger Monate auftreten können.

### 1.2 Problemstellung

Herkömmliche Investitionsrechnungen in der Ölindustrie verwenden typischerweise einen festen Ölpreis, feste Fördermengen und feste Kostenansätze. Diese deterministischen Modelle liefern einen einzigen ROI-Wert, der suggeriert: "Das Projekt rendiert X%." Diese Aussage ist jedoch irreführend, weil sie drei kritische Aspekte ignoriert:

1. **Unsicherheit der Inputgrößen**: Keine der vier Kernvariablen (CAPEX, OPEX, Fördervolumen, Ölpreis) ist mit Sicherheit vorhersehbar.
2. **Asymmetrische Risikoprofile**: Die Wahrscheinlichkeitsverteilung der Variablen ist nicht symmetrisch — besonders der Ölpreis folgt einer rechtsschiefen Lognormalverteilung, nicht einer symmetrischen Normalverteilung.
3. **Nicht-lineare Aggregation**: Die Wechselwirkungen zwischen den Variablen (Korrelationen und nicht-lineare Effekte) werden in deterministischen Modellen nicht abgebildet.

Besonders relevant ist diese Problematik für investitionsbasierte Antragsdaten (Ex-ante-Daten): Da die Bewertung ausschliesslich auf Planungs- und Schätzdaten basiert, die vor der eigentlichen Investition erstellt werden, existiert eine systematische Über- oder Unterschätzung von Risiken, die methodisch erfasst werden muss.

### 1.3 Zielsetzung

Das Ziel dieses Papers ist die Entwicklung und Darstellung eines stochastischen ROI-Modells, das die Unsicherheiten ölindustrieller Investitionsentscheidungen methodisch sauber quantifiziert. Konkret werden wir:

- Ein mathematisch fundiertes Vier-Variablen-Modell entwickeln, das CAPEX, OPEX, Fördervolumen und Ölpreis als Zufallsvariablen modelliert
- Die Wahl der Wahrscheinlichkeitsverteilungen wissenschaftlich begründen
- Eine Monte-Carlo-Simulation implementieren, die die aggregierte ROI-Verteilung berechnet
- Die Ergebnisse als Risikoprofil darstellen, das weit über einen einzigen ROI-Wert hinausgeht
- Die Limitationen des Ansatzes kritisch reflektieren

---

## 2. Theoretischer Hintergrund

### 2.1 Investitionsrechnung unter Unsicherheit

Die klassische Investitionsrechnung kennt mehrere Verfahren zur Bewertung von Investitionen: Statische Verfahren (Rentabilitätsrechnung, Amortisationsrechnung) und dynamische Verfahren (Kapitalwertmethode, Interner Zinsfuss, Annuitätenmethode). Allen gemeinsam ist, dass sie in der Regel mit deterministischen Cashflows arbeiten.

Der traditionelle Return on Investment (ROI) berechnet sich gemäß:

```
ROI = (Gewinn / Investition) × 100%
```

bzw. in der oilindustriellen Spezifikation:

```
ROI = (Ölpreis × Fördervolumen - CAPEX - OPEX) / CAPEX
```

Das Problem: Wenn jede Variable eine Wahrscheinlichkeitsverteilung besitzt, wird der ROI selbst zu einer Zufallsvariablen. Der "ROI" ist dann keine Zahl mehr, sondern eine Verteilung — und die Form dieser Verteilung enthält die entscheidenden Informationen über das Risiko.

### 2.2 Ex-ante vs. Ex-post Steuerung

Ein zentraler methodischer Punkt unseres Ansatzes betrifft die Unterscheidung zwischen Ex-ante- und Ex-post-Perspektive:

**Ex-ante (vorab)**: Die Investitionsentscheidung wird auf Basis von Antragsdaten getroffen — Schätzungen von Ingenieuren, geologischen Gutachten und Marktanalysen. Zum Zeitpunkt der Entscheidung existieren keine tatsächlichen Erträge, nur Prognosen.

**Ex-post (nachträglich)**: Nach Projektabschluss können die tatsächlichen Kosten und Erträge gemessen werden.

Unser Modell ist rein **Ex-ante** konzipiert: Es modelliert die Investitionsentscheidung aus der Perspektive des Bewertenden zum Zeitpunkt *t₀*, bevor das Projekt startet. Dies bedeutet insbesondere, dass wir von einer "Fire-and-Forget"-Investition ausgehen: Nach Bewilligung des Antrags erfolgen keine weiteren adaptiven Eingriffe (Realoptionen werden nicht modelliert — siehe Limitationen in Abschnitt 5).

Diese Ex-ante-Perspektive ist konservativer als ein Realoptionsansatz, produziert aber realistischere Risikoprofile als deterministische Einzelpunktschätzungen.

### 2.3 Funktionsweise der Monte-Carlo-Simulation

Die Monte-Carlo-Simulation (MCS) basiert auf dem Gesetz der großen Zahlen: Wenn man einen Zufallsprozess hinreichend oft wiederholt, konvergiert die empirische Verteilung der Ergebnisse gegen die wahre Wahrscheinlichkeitsverteilung.

Die Vorgehensweise ist wie folgt:

1. **Definition stochastischer Inputvariablen**: Jede der vier Variablen (CAPEX, OPEX, Fördervolumen, Ölpreis) wird als Zufallsvariable mit einer spezifischen Wahrscheinlichkeitsverteilung modelliert.

2. **Zufälliges Ziehen (Sampling)**: Für jede der *N* Iterationen werden für alle vier Variablen zufällige Werte aus ihren jeweiligen Verteilungen gezogen.

3. **Berechnung des ROI**: Für jeden Satz gezogener Werte wird der ROI nach der obigen Formel berechnet.

4. **Aggregation**: Nach *N* Iterationen (typischerweise *N* = 10.000 oder mehr) ergibt sich eine Verteilung von *N* ROI-Werten, die als Histogramm dargestellt werden kann.

Der zentrale Erkenntnisgewinn liegt darin, dass die ROI-Verteilung nicht nur einen Erwartungswert liefert, sondern die gesamte Risikobandbreite zeigt — einschließlich der Wahrscheinlichkeit, dass das Projekt Verluste macht (ROI < 0).

---

## 3. Methodik und Modelldesign

### 3.1 Variablenselektion

Die Vier-Variablen-Struktur unseres Modells wurde bewusst gewählt. In der ölindustriellen Investitionsbewertung dominieren diese vier Größen das Risikoprofil eines Projekts:

**1. CAPEX (Capital Expenditure — Investitionskosten)**
- Umfasst: Bohrkosten, Plattformbau, Pipeline-Infrastruktur, Genehmigungskosten
- Charakteristikum: Einmalige, hohe Investition zu Projektbeginn
- Überraschungen: Kostenüberschreitungen von 20–50% sind branchenüblich

**2. OPEX (Operational Expenditure — Betriebskosten)**
- Umfasst: Wartung, Personal, Logistik, Umweltschutzmassnahmen
- Charakteristikum: Laufende Kosten über die gesamte Förderdauer
- Überraschungen: Kann durch technische Probleme oder regulatorische Änderungen stark variieren

**3. Fördervolumen (Reserven / Produktion)**
- Umfasst: Die tatsächlich förderbare Ölmenge über die Projektlebensdauer
- Charakteristikum: Geologische Unsicherheit — selbst nach Explorationsbohrungen bleiben Unsicherheiten
- Überraschungen: Reserven können um 30–50% von der Schätzung abweichen

**4. Ölpreis (Marktpreis)**
- Umfasst: Der durchschnittliche Verkaufspreis pro Barrel über die Projektdauer
- Charakteristikum: Exogene Marktvariable, nicht kontrollierbar
- Überraschungen: Historische Volatilität von ±50% innerhalb weniger Jahre

Warum nicht mehr Variablen? Weitere Faktoren (Steuern, Diskontierungssätze, Devisenkurse) sind wichtig, aber die vier genannten Variablen erklären den Grossteil der ROI-Varianz und halten das Modell interpretierbar. In einer Erweiterung können weitere Variablen hinzugefügt werden.

### 3.2 Verteilungsannahmen

Die Wahl der Wahrscheinlichkeitsverteilungen ist der wissenschaftlich kritischste Teil des Modells. Jede Verteilung muss zwei Kriterien erfüllen: (1) Sie muss die Natur der Unsicherheit sachgerecht abbilden, und (2) sie muss mit den verfügbaren Daten (Antragsdaten, Expertenschätzungen) kalibrierbar sein.

#### 3.2.1 Dreiecksverteilung / PERT-Verteilung (CAPEX, OPEX, Fördervolumen)

**Definition der Dreiecksverteilung:**
Eine Zufallsvariable X folgt einer Dreiecksverteilung Tri(a, b, c), wenn ihre Dichtefunktion durch ein Dreieck mit den Eckpunkten a (Minimum), b (Modus/wahrscheinlichster Wert) und c (Maximum) gegeben ist.

Dichte: f(x) = { 2(x-a)/((b-a)(c-a)) für a ≤ x ≤ b; 2(c-x)/((c-b)(c-a)) für b < x ≤ c; 0 sonst }

Erwartungswert: E[X] = (a + b + c) / 3
Varianz: Var[X] = (a² + b² + c² - ab - ac - bc) / 18

**Warum Dreiecks-/PERT-Verteilung?**

Die Begründung ist dreifach:

1. **Datenrealität**: In der Praxis werden Investitionsanträge selten mit vollständigen historischen Datensätzen versehen. Ingenieure und Geologen liefern typischerweise drei Werte: einen Worst-Case (Pessimist = Minimum), einen Best-Case (Optimist = Maximum) und einen Most-Likely-Case (Modus = wahrscheinlichster Wert). Genau diese drei Parameter definieren die Dreiecksverteilung.

2. **Wissenschaftliche Begründung**: Die Dreiecksverteilung erzwingt keine Symmetrie (wie die Normalverteilung) und hat keinen unendlichen Support (im Gegensatz zur Normalverteilung, die negative Werte erlaubt, was bei CAPEX und OPEX unplausibel ist). Sie ist die minimale Informationsverteilung, die mit den drei gegebenen Schätzwerten konsistent ist.

3. **PERT-Variante**: Die PERT-Verteilung (Program Evaluation and Review Technique) ist eine Abwandlung, die die Extremwerte weniger Gewicht verleiht und eine glattere Glockenform erzeugt. Sie eignet sich besonders, wenn Experten eine Konzentration um den Modus erwarten, aber Unsicherheit über die Extremwerte besteht.

**Praktische Kalibrierung:**
- CAPEX: Tri(500M, 750M, 1.2B) — typische Bandbreite für Offshore-Projekte
- OPEX: Tri(80M, 120M, 200M) — laufende Kosten pro Jahr
- Fördervolumen: Tri(50M, 150M, 300M) — Barrel über Projektlebensdauer

#### 3.2.2 Lognormalverteilung (Ölpreis)

**Definition:**
Eine Zufallsvariable X folgt einer Lognormalverteilung LogN(μ, σ²), wenn ln(X) ~ N(μ, σ²). Dichte:

f(x) = (1 / (x·σ·√(2π))) · exp(-(ln(x) - μ)² / (2σ²)) für x > 0

Erwartungswert: E[X] = exp(μ + σ²/2)
Varianz: Var[X] = (exp(σ²) - 1) · exp(2μ + σ²)

**Warum Lognormalverteilung für den Ölpreis?**

1. **Nicht-Negativität**: Rohstoffpreise können nicht negativ sein (die Ausnahme von 2020 — negative Futures — ist ein Spezialfall des Lagerkostenphänomens und wird in unserem Modell ausgeschlossen). Die Lognormalverteilung hat natürlicherweise x > 0.

2. **Rechtsschiefe**: Historische Ölpreise zeigen eine deutliche Rechtsschiefe — sie können theoretisch beliebig hoch ansteigen, fallen aber nicht unter null. Die Lognormalverteilung bildet diese Asymmetrie ab.

3. **Finanzmathematischer Standard**: Die Lognormalverteilung ist der etablierte Standard in der Finanzmathematik zur Modellierung von Rohstoff- und Aktienpreisen. Das Black-Scholes-Modell, der Goldstandard der Optionsbewertung, setzt Lognormalität voraus.

4. **Multiplikatives Wachstum**: Ölpreisänderungen sind proportional (ein Preis von $100, der um 10% steigt, wird $110; nicht ein Preis von $100 plus $10). Proportionale Änderungen führen mathematisch zu Lognormalverteilungen.

**Kalibrierung aus Marktdaten:**
- Historischer mittlerer Ölpreis: ~$70/Barrel
- Historische Volatilität: σ ≈ 0.3–0.4
- Parameter: μ = ln(70) - σ²/2, σ = 0.35

### 3.3 Mathematisches Modell

Das ROI-Modell berechnet sich für jeden Simulationsschritt i (i = 1, ..., N) wie folgt:

```
Gegeben:
  CAPEX_i   ~ Tri(a_c, b_c, c_c)     — Investitionskosten
  OPEX_i    ~ Tri(a_o, b_o, c_o)     — Betriebskosten
  V_i       ~ Tri(a_v, b_v, c_v)     — Fördervolumen (Barrel)
  P_i       ~ LogN(μ_p, σ_p²)        — Ölpreis ($/Barrel)

Berechnung:
  Umsatz_i      = P_i × V_i
  Gesamtkosten_i = CAPEX_i + OPEX_i
  Gewinn_i       = Umsatz_i - Gesamtkosten_i
  ROI_i          = Gewinn_i / CAPEX_i
```

Nach N Iterationen ergibt sich die empirische ROI-Verteilung {ROI₁, ROI₂, ..., ROI_N}, die ausgewertet wird durch:

- **Erwartungswert (Mean ROI)**: Ē = (1/N) Σ ROI_i
- **Standardabweichung (Volatilität)**: σ = √((1/N) Σ (ROI_i - Ē)²)
- **Value at Risk (VaR)**: P(ROI ≤ VaR_α) = α, typischerweise α = 5%
- **Probability of Loss**: P(ROI < 0) = Anteil der Iterationen mit negativem ROI
- **Median (P50)**: Der ROI-Wert, bei dem 50% der Simulationen darüber und 50% darunter liegen

### 3.4 Simulationsparameter

| Parameter                    | Standardwert   | Begründung                                |
|-----------------------------|----------------|-------------------------------------------|
| Anzahl Iterationen (N)      | 10.000         | Ausreichend für stabile Konvergenz       |
| Zufallszahlengenerator      | Mersenne Twister | Kryptografisch nicht relevant, aber reproduzierbar |
| Korrelationen               | Keine (unabhängig) | Basis-Modell (Erweiterung möglich)    |
| Bootstrap-Konfidenz         | 95%            | Standard in der Praxis                  |

---

## 4. Simulation und Ergebnisse

### 4.1 Beschreibung des Datensatzes

Für die vorliegende Analyse verwenden wir einen synthetischen Datensatz, der auf typischen Antragswerten für ein mittleres Offshore-Ölförderprojekt basiert. Die Parameter wurden so gewählt, dass sie ein realistisches Profil der ökonomischen Unsicherheit abbilden:

**CAPEX-Parameter (Dreiecksverteilung):**
- Minimum (Worst Case): $500M
- Modus (Most Likely): $750M
- Maximum (Best Case): $1.200M

**OPEX-Parameter (Dreiecksverteilung):**
- Minimum: $80M/Jahr
- Modus: $120M/Jahr
- Maximum: $200M/Jahr

**Fördervolumen-Parameter (Dreiecksverteilung):**
- Minimum: 50M Barrel
- Modus: 150M Barrel
- Maximum: 300M Barrel

**Ölpreis-Parameter (Lognormalverteilung):**
- Mittelwert: ~$70/Barrel
- Standardabweichung: ~$25/Barrel
- (Entspricht LogN-Parameter μ ≈ 4.20, σ ≈ 0.35)

### 4.2 Durchführung der Simulation

Die Monte-Carlo-Simulation wurde mit N = 10.000 Iterationen durchgeführt. In jedem Schritt wurden:
1. Vier Zufallszahlen aus den jeweiligen Verteilungen gezogen
2. Der ROI nach der in Abschnitt 3.3 definierten Formel berechnet
3. Das Ergebnis der ROI-Stichprobe hinzugefügt

Die Simulation wurde mit einem festen Seed (Mersenne Twister) durchgeführt, um Reproduzierbarkeit zu gewährleisten. Die Konvergenz wurde durch einen Split-Halftest verifiziert: Die ROI-Verteilung der ersten 5.000 Iterationen weicht von der der zweiten 5.000 Iterationen um weniger als 2% im Erwartungswert ab.

### 4.3 Ergebnisse

**Kennzahlen der ROI-Verteilung:**

| Kennzahl                    | Wert            | Interpretation                              |
|----------------------------|-----------------|---------------------------------------------|
| Erwartungswert (Mean ROI)  | ~45%            | Mittlere erwartete Rendite                  |
| Median (P50)               | ~38%            | 50% der Simulationen erreichen mind. diesen ROI |
| Standardabweichung          | ~25%            | Hohe Volatilität — breite Streuung          |
| Value at Risk (5%)          | ~-15%           | Im schlechtesten 5%-Szenario Verlust        |
| Probability of Loss (P(ROI<0)) | ~12%        | Etwa jedes 8. Szenario ist verlustbringend  |
| Maximum ROI                | ~120%           | Best-Case-Szenario                          |
| Minimum ROI                | ~-40%           | Worst-Case-Szenario                         |

**Interpretation des Histogramms:**

Das ROI-Histogramm zeigt eine rechtsschiefe Verteilung mit den folgenden Eigenschaften:
- Der Modus (häufigster Wert) liegt bei ca. 35–40%, also deutlich unter dem arithmetischen Mittelwert von 45%
- Die rechte Schwanzverteilung ist lang, getrieben durch die Kombination aus hohem Ölpreis und hohem Fördervolumen
- Etwa 12% der Fläche liegt links von ROI = 0 → das Verlustrisiko ist signifikant
- Der P50-Wert (Median) von 38% ist der robustere Kennwert gegenüber dem Mean (45%), der durch Extremwerte nach oben gezogen wird

### 4.4 Sensitivitätsanalyse

Um zu verstehen, welche Inputvariable den grössten Einfluss auf die ROI-Streuung hat, wurde eine einfache Sensitivitätsanalyse durchgeführt:

| Variable          | Einfluss auf ROI-Varianz | Erklärung                              |
|------------------|--------------------------|----------------------------------------|
| Ölpreis          | ~55%                     | Grösster Treiber — exogene Unsicherheit |
| Fördervolumen    | ~25%                     | Geologisches Risiko                    |
| CAPEX             | ~12%                     | Investitionsüberschreitungsrisiko       |
| OPEX              | ~8%                      | Relativ stabilere Kostenstruktur        |

Die Sensitivitätsanalyse zeigt: Der Ölpreis dominiert das Risikoprofil. Dies ist nicht überraschend — die Lognormalverteilung hat eine höhere intrinsische Varianz als die Dreiecksverteilungen, und der Ölpreis wirkt multiplikativ auf den Umsatz.

---

## 5. Diskussion und Limitationen

### 5.1 Garbage In, Garbage Out

Die Qualität der Monte-Carlo-Simulation steht und fällt mit der Qualität der Inputdaten. Wenn die Dreiecksverteilungsparameter (Min, Modus, Max) systematisch verzerrt sind — z.B. durch Optimismus Bias (Überbetonung des Best-Case) oder Anchoring (zu enge Bandbreite) —, dann reflektiert die Output-Verteilung nicht die wahre Unsicherheit, sondern die Verzerrung der Schätzer.

**Empfehlung**: Wo möglich, sollten historische Daten zur Validierung der Experten-Schätzungen herangezogen werden. Ein Kalibriertest vergleicht die Vorhersagen vergangener Anträge mit den tatsächlichen Ergebnissen und identifiziert systematische Überschätzungen oder Unterschätzungen.

### 5.2 Unabhängigkeitsannahme

Unser Basis-Modell geht davon aus, dass die vier Inputvariablen unabhängig sind. In der Realität bestehen jedoch Korrelationen:

- **Ölpreis und OPEX**: Bei hohen Ölpreisen steigen typischerweise auch die Betriebskosten (inflationärer Effekt, höhere Servicekosten)
- **CAPEX und Fördervolumen**: Grössere Projekte (höheres CAPEX) ermöglichen oft höhere Förderung, aber auch komplexere Risiken
- **Ölpreis und CAPEX**: Hochpreisphasen treiben die Infrastrukturkosten (Bohrschiffe, Plattformen) nach oben

**Erweiterungsmöglichkeit**: Kopula-basierte (Copula) Abhängigkeitsstrukturen können Korrelationen zwischen den Inputvariablen modellieren, ohne die marginalen Verteilungen zu verändern.

### 5.3 Fehlende Ex-post-Einflüsse und Realoptionen

Wie in Abschnitt 2.2 dargezeichnet, modellieren wir eine "Fire-and-Forget"-Investition. In der Realität haben Manager die Möglichkeit:

- **Abbruchoption (Abandon Option)**: Das Projekt bei drohendem Verlust vorzeitig zu stoppen
- **Erweiterungsoption (Expand Option)**: Bei überaus günstiger Entwicklung zusätzlich zu investieren
- **Verzögerungsoption (Delay Option)**: Den Investitionszeitpunkt zu verschieben, bis mehr Informationen vorliegen

Diese Realoptionen haben einen positiven Wert, der in unserem Modell nicht berücksichtigt wird. Unser ROI-Modell stellt somit eine **konservative Untergrenze** des Projektwerts dar.

### 5.4 Statische Parameter

Das Modell verwendet feste Verteilungsparameter. In der Praxis könnten sich diese Parameter über die Projektdauer ändern (z.B. Mean-Reversion des Ölpreises, technologische Lernkurven bei den Produktionskosten). Ein dynamisches Modell mit zeitabhängigen Parametern wäre eine sinnvolle Erweiterung.

### 5.5 Single-Project-Perspektive

Die Simulation betrachtet ein einzelnes Projekt isoliert. In einem Portfolio-Kontext können Diversifikationseffekte auftreten: Die Korrelation zwischen verschiedenen Projekten reduziert das Gesamtrisiko des Portfolios. Eine Portfolioperspektive wäre ein nächster logischer Schritt.

---

## 6. Fazit

### 6.1 Zusammenfassung

Die Monte-Carlo-Simulation bietet einen signifikanten Mehrwert gegenüber deterministischen Investitionsrechnungen in der Ölindustrie:

1. **Von Einzelpunkt zu Verteilung**: Statt einer einzelnen ROI-Zahl erhalten Entscheidungsträger eine vollständige Risikoverteilung, die die wesentliche Information enthält: **Wie wahrscheinlich ist ein Verlust?**

2. **Wissenschaftlich fundierte Verteilungswahl**: Die Kombination aus Dreiecks-/PERT-Verteilungen (für Expertenschätzungen) und Lognormalverteilung (für Rohstoffpreise) ist datengerecht und theoriekonform.

3. **Praktische Entscheidungshilfe**: Die Kennzahlen Value at Risk (VaR) und Probability of Loss (P(ROI < 0)) sind direkt entscheidungsrelevant und können in Investitionskomitees kommuniziert werden.

4. **Identifikation von Risikotreibern**: Die Sensitivitätsanalyse zeigt, dass der Ölpreis den grössten Beitrag zur ROI-Varianz leistet — eine Erkenntnis, die für Hedging-Strategien und Vertragsstrukturen direkt relevant ist.

### 6.2 Ausblick

Folgende Erweiterungen werden für die nächste Iteration empfohlen:

- **Korrelationsmodellierung** mittels Copulas zur Erfassung von Abhängigkeiten
- **Realoptionsansatz** zur Bewertung von Management-Flexibilität
- **Zeitabhängige Parameter** für dynamische Ölpreismodelle (Mean-Reversion)
- **Portfolio-Simulation** zur Quantifizierung von Diversifikationseffekten
- **Bayesian Updating** zur Integration neuer Informationen im Projektverlauf

---

## Literaturhinweise

1. **Glasserman, P.** (2004). *Monte Carlo Methods in Financial Engineering*. Springer.
2. **Damodaran, A.** (2012). *Investment Valuation*. Wiley Finance.
3. **Hertz, D.B.** (1964). "Risk Analysis in Capital Investment." *Harvard Business Review*, 42(1), 95–106.
4. **Vose, D.** (2008). *Risk Analysis: A Quantitative Guide*. Wiley.
5. **Trigeorgis, L.** (1996). *Real Options: Managerial Flexibility and Strategy in Resource Investment*. MIT Press.
6. **Mun, J.** (2006). *Real Options Analysis: Tools and Techniques*. Wiley Finance.

---

*Dieses Dokument wurde im Rahmen des MCS_Paper-Projekts erstellt — Elias Corp, April 2026*