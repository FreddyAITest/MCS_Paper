# Das ROI-Modell: Mathematische Formulierung

## 1. Grundgleichung

Für jeden Simulationsschritt *i* (i = 1, ..., N) berechnet sich der Return on Investment (ROI):

```
ROI_i = (Umsatz_i - Gesamtkosten_i) / CAPEX_i
      = (P_i × V_i - CAPEX_i - OPEX_i) / CAPEX_i
```

### Variablendefinitionen

| Symbol | Beschreibung | Einheit | Verteilung |
|--------|-------------|---------|-----------|
| P_i | Ölpreis | $/Barrel | LogN(μ_p, σ_p²) |
| V_i | Fördervolumen | Barrel | Tri(a_v, m_v, b_v) |
| CAPEX_i | Investitionskosten | $ | Tri(a_c, m_c, b_c) |
| OPEX_i | Betriebskosten | $ | Tri(a_o, m_o, b_o) |
| ROI_i | Return on Investment | dimensionslos | — (abgeleitet) |

## 2. Erweiterte Form

Durch Multiplikation aus:

```
ROI_i = P_i × (V_i / CAPEX_i) - 1 - (OPEX_i / CAPEX_i)
```

Diese Form zeigt die drei Bestandteile:
1. **Erlös-Rendite**: P_i × (V_i / CAPEX_i)
2. **Basis-Abzug**: -1 (die Investition selbst)
3. **Betriebskosten-Rendite**: -(OPEX_i / CAPEX_i)

## 3. Statistische Kennzahlen der ROI-Verteilung

### Erwartungswert (Mean)
```
Ē = (1/N) × Σ(i=1 to N) ROI_i
```

### Standardabweichung (Risikomass)
```
σ = √((1/N) × Σ(i=1 to N) (ROI_i - Ē)²)
```

### Value at Risk (VaR)
```
VaR_α = Quantil(α) der empirischen ROI-Verteilung
```
Für α = 5%: VaR_5% ist der ROI-Wert, unterhalb dessen nur 5% der Simulationen liegen.

### Probability of Loss
```
P(ROI < 0) = (Anzahl der Iterationen mit ROI_i < 0) / N
```

### Conditional Value at Risk (CVaR / Expected Shortfall)
```
CVaR_α = (1/(N × α)) × Σ(i=1 to N) ROI_i × I(ROI_i ≤ VaR_α)
```
Wobei I die Indikatorfunktion ist. CVaR gibt den durchschnittlichen ROI im Worst-α%-Szenario an.

### Sharpe-ähnliches Risikoadjustiertes Mass
```
RARR = Ē / σ    (Risk-Adjusted Return Ratio)
```
Analog zum Sharpe-Ratio, aber mit ROI statt Rendite und Standardabweichung statt Downside-Risk.

## 4. Analytische Näherungen

Für schnelle Abschätzungen (ohne Simulation) können die Momente der ROI-Verteilung approximiert werden:

### Erste Näherung (Unabhängigkeitsannahme, Taylor-Reihe)

Wenn CAPEX ≈ E[CAPEX] = μ_c konstant angenommen wird:

```
E[ROI] ≈ (E[P] × E[V] - μ_c - E[OPEX]) / μ_c
       ≈ (E[P] × E[V]) / μ_c - 1 - E[OPEX] / μ_c
```

### Varianz der ersten Näherung

Mit der Delta-Methode (Linearisierung um die Erwartungswerte):

```
Var[ROI] ≈ (∂ROI/∂P)² × Var[P] + (∂ROI/∂V)² × Var[V] 
          + (∂ROI/∂CAPEX)² × Var[CAPEX] + (∂ROI/∂OPEX)² × Var[OPEX]
```

Mit:
- ∂ROI/∂P = V / CAPEX
- ∂ROI/∂V = P / CAPEX
- ∂ROI/∂CAPEX = -(P×V - OPEX) / CAPEX²
- ∂ROI/∂OPEX = -1 / CAPEX

Diese Näherung ist nützlich für Schnellabschätzungen, unterliegt aber der Linearisierungsapproximation und unterschätzt typischerweise die wahre Varianz bei nicht-linearen Abhängigkeiten.

## 5. Korrelationserweiterung (Future Work)

Wenn Korrelationen zwischen den Variablen berücksichtigt werden, wird das Sampling-Verfahren angepasst:

### Copula-basierter Ansatz

Anstatt unabhängiges Ziehen aus den Randverteilungen wird eine Copula C(·) verwendet:

```
(U1, U2, U3, U4) ~ C(ρ12, ρ13, ρ14, ρ23, ρ24, ρ34)
P_i = F_P^(-1)(U1)
V_i = F_V^(-1)(U2)
CAPEX_i = F_C^(-1)(U3)
OPEX_i = F_O^(-1)(U4)
```

Die Wahl der Copula (Gaussian, Student-t, Clayton, Gumbel) bestimmt die Art der Abhängigkeit:
- **Gaussian Copula**: Lineare Korrelation, symmetrische Schwänze
- **Student-t Copula**: Dickere Schwänze, bessere Modellierung extremer gemeinsamer Ereignisse
- **Clayton Copula**: Untere Schwanzabhängigkeit (gemeinsame extreme Verluste)

---

*Die Implementierung dieser Formeln erfolgt in `src/simulation/roi_calculator.py`*