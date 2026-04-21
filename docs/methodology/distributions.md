# Verteilungsannahmen und wissenschaftliche Begründung

## Übersicht

Dieses Dokument begründet die Wahl der Wahrscheinlichkeitsverteilungen für die vier stochastischen Inputvariablen des MCS-ROI-Modells.

---

## 1. Dreiecksverteilung (Triangular Distribution)

### Einsatz: CAPEX, OPEX, Fördervolumen

### Mathematische Definition

Eine Zufallsvariable X ~ Tri(a, m, b) hat die Dichtefunktion:

```
f(x) = {
  2(x - a) / ((m - a)(b - a))  für a ≤ x ≤ m
  2(b - x) / ((b - m)(b - a))  für m < x ≤ b
  0                             sonst
}
```

Mit:
- a = Minimum (Worst Case)
- m = Modus (Most Likely)
- b = Maximum (Best Case)

### Kennzahlen
- Erwartungswert: E[X] = (a + m + b) / 3
- Varianz: Var[X] = (a² + m² + b² - am - ab - mb) / 18
- Schiefe: (a + b - 2m)(2b - a - m)(m - 2a + b) / (30 · σ³) — kann positiv, negativ oder null sein

### Wissenschaftliche Begründung

1. **Datenadäquanz**: Die drei Parameter (Min, Modus, Max) korrespondieren direkt mit den drei Werten, die Ingenieure in Investitionsanträgen liefern. Keine Verteilung bildet diese verfügbare Information präziser ab.

2. **Minimale Informationsverteilung**: Nach dem Prinzip der maximalen Entropie ist die Dreiecksverteilung die "minimalste" Annahme, die mit den drei gegebenen Punkten konsistent ist. Sie erzwingt keine zusätzliche Struktur, die in den Daten nicht begründet ist.

3. **Beschränkter Support**: Im Gegensatz zur Normalverteilung (die negative Werte erlaubt) hat die Dreiecksverteilung einen endlichen Definitionsbereich [a, b]. Dies ist physikalisch sinnvoll: CAPEX, OPEX und Fördervolumen können nicht negativ sein und haben plausible obere Grenzen.

4. **Keine Symmetrieannahme**: Die Dreiecksverteilung muss nicht symmetrisch sein. Dies ist wichtig, weil Experten oft asymmetrische Risiken wahrnehmen: Der Worst-Case könnte weiter vom Most Likely entfernt sein als der Best-Case.

---

## 2. PERT-Verteilung (Beta-Verteilung)

### Einsatz: Alternative zu Dreieck für CAPEX, OPEX, Fördervolumen

### Mathematische Definition

Die PERT-Verteilung (Program Evaluation and Review Technique) ist eine Beta-Verteilung, die mit denselben drei Parametern (Min, Modus, Max) plus einem Gewichtsparameter λ kalibriert wird:

```
μ = (a + λ·m + b) / (2 + λ)   (Standard: λ = 4)
```

Die PERT-Verteilung hat ähnliche Eigenschaften wie die Dreiecksverteilung, aber:
- **Glattere Dichtefunktion** (keine Knickpunkte beim Modus)
- **Geringeres Gewicht der Extremwerte** (schlankere Schwänze)
- **Natürlichere Glockenform** für Werte, bei denen Experten eine Konzentration um den Mittelpunkt erwarten

### Wann PERT statt Dreieck?

| Kriterium | Dreieck | PERT |
|----------|---------|------|
| Konservative Experten-Schätzungen | ✅ | |
| Optimistische Schätzungen (Betonzentration um Modus) | | ✅ |
| Experte sehr sicher über den wahrscheinlichsten Wert | | ✅ |
| Experte gibt bewusst weite Bandbreiten an | ✅ | |
| Einfachheit/Transparenz wichtiger als Glätte | ✅ | |

---

## 3. Lognormalverteilung (Lognormal Distribution)

### Einsatz: Ölpreis

### Mathematische Definition

Eine Zufallsvariable X ~ LogN(μ, σ²) hat die Dichtefunktion:

```
f(x) = (1 / (x · σ · √(2π))) · exp(-(ln(x) - μ)² / (2σ²))   für x > 0
```

Äquivalent: ln(X) ~ N(μ, σ²)

### Kennzahlen
- Median: exp(μ)
- Erwartungswert: exp(μ + σ²/2)
- Varianz: (exp(σ²) - 1) · exp(2μ + σ²)
- Schiefe: (exp(σ²) + 2) · √(exp(σ²) - 1) — immer rechtsschief

### Wissenschaftliche Begründung

1. **Nicht-Negativität**: Ölpreise können nicht negativ sein. Die Lognormalverteilung hat natürlicherweise x > 0, im Gegensatz zur Normalverteilung, die negative Werte zulässt.

2. **Rechtsschiefe**: Historische Ölpreisdaten zeigen eine deutliche Rechtsschiefe — es gibt extreme Spitzen nach oben (Olpreisschocks), die in einer symmetrischen Verteilung unterschätzt würden.

3. **Proportionale Änderungen**: Ölpreisänderungen sind multiplikativ, nicht additiv. Ein Preisanstieg von 10% auf $110 ist nicht dasselbe wie ein Anstieg von $10. Diese Multiplikativität führt mathematisch zur Lognormalverteilung.

4. **Finanzmathematischer Standard**: Das Black-Scholes-Modell und die moderne Finanzmathematik setzen Lognormalität für Assetpreise voraus. Die Verwendung derselben Verteilung ermöglicht die Konsistenz mit anderen Finanzmodellen.

### Kalibrierung aus Marktdaten

Für den Ölpreis: Wenn der historische Mittelwert bei ca. $70/Barrel liegt und die historische Volatilität bei ca. 35%:

```
E[X] = $70
E[X] = exp(μ + σ²/2)  →  exp(μ + σ²/2) = 70
σ_relative = 0.35

Aus σ_relative² = (exp(σ²) - 1) · exp(σ²) / (exp(σ²) - 1)²
vereinfacht: σ ≈ 0.34  (close to σ_relative für moderate Werte)

μ = ln(70) - σ²/2 ≈ 4.248 - 0.058 ≈ 4.19
```

Parameter: LogN(μ ≈ 4.19, σ² ≈ 0.12)

---

## 4. Vergleich der Verteilungen

| Eigenschaft | Normal | Dreieck | PERT | Lognormal |
|------------|--------|---------|------|-----------|
| Nicht-negativ | ❌ | ✅ | ✅ | ✅ |
| Beschränkter Support | ❌ | ✅ | ✅ | ❌ (rechtsschwanz) |
| Rechtsschief | ❌ | möglich | möglich | ✅ (immer) |
| 3-Parameter (Min,Mod,Max) | ❌ | ✅ | ✅ | ❌ |
| Finanz-Standard | ❌ | ❌ | ❌ | ✅ |
| Geeignet für | Residuen | CAPEX/OPEX | CAPEX/OPEX | Ölpreis |

---

## 5. Referenzen

- Vose, D. (2008). *Risk Analysis: A Quantitative Guide*. Wiley.
- Hertz, D.B. (1964). "Risk Analysis in Capital Investment." *Harvard Business Review*.
- Hull, J.C. (2018). *Options, Futures, and Other Derivatives*. Pearson.