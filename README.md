# MCS_Paper

1. Das wissenschaftliche Setup: Variablen und Verteilungen

Für eine Monte-Carlo-Simulation brauchst du stochastische Inputgrößen. Da ihr Antragsdaten auswertet, basieren diese oft auf Expertenschätzungen.

Die 4 klassischen Inputgrößen für Ölkonzerne:

CAPEX (Capital Expenditure / Investitionskosten): Bohrungen, Plattformbau, Infrastruktur.

OPEX (Operational Expenditure / Betriebskosten): Laufende Kosten für Förderung und Logistik.

Fördervolumen (Reserven/Produktion): Wie viel Öl tatsächlich im Boden ist und gefördert werden kann (geologisches Risiko).

Ölpreis (Marktpreis): Der zukünftige Verkaufspreis pro Barrel (Marktrisiko).

Welche Wahrscheinlichkeitsverteilungen nehmen wir an?
In der Wissenschaft müssen Verteilungen begründet werden. Da ihr mit Antragsdaten (Schätzungen) arbeitet, bieten sich folgende Verteilungen an:

Dreiecksverteilung (Triangular Distribution) oder PERT-Verteilung:

Einsatzort: CAPEX, OPEX und oft auch Fördervolumen.

Wissenschaftliche Begründung: Bei Anträgen werden selten gigantische historische Datensätze mitgeliefert. Meist geben Ingenieure drei Werte an: einen Worst-Case (Minimum), einen Best-Case (Maximum) und einen Most-Likely-Case (Modus/wahrscheinlichster Wert). Die Dreiecks- oder PERT-Verteilung modelliert genau dieses Expertenwissen perfekt, ohne eine Normalverteilung erzwingen zu müssen (die Ausreißer ins Unendliche hätte).

Lognormalverteilung (Lognormal Distribution):

Einsatzort: Ölpreis.

Wissenschaftliche Begründung: Rohstoffpreise können nicht negativ werden (die Ausnahme von 2020 klammern wir mathematisch meist aus), können aber theoretisch extrem stark ansteigen (Rechtsschiefe). Die Lognormalverteilung ist der finanzmathematische Standard zur Modellierung von Asset- und Rohstoffpreisen (vgl. Black-Scholes-Modell).

Der ROI berechnet sich in der Simulation dann für jeden der zehntausend Durchläufe grob nach dem Schema:

ROI= 
CAPEX
( 
O
¨
 lpreis×F 
o
¨
 rdervolumen)−(CAPEX+OPEX)
​	
 
2. Strukturvorschlag für dein Paper (Gliederung)

Um das Ganze wissenschaftlich sauber aufzubauen, empfehle ich folgende Struktur:

1. Einleitung

Motivation: Hohe Volatilität und Kapitalintensität in der Ölindustrie.

Problemstellung: Klassische deterministische Modelle (Single-Point-Schätzungen) greifen zu kurz, da sie Unsicherheiten ignorieren. Die Abhängigkeit von reinen Ex-ante-Antragsdaten erfordert robuste Risikomessung.

Zielsetzung: Entwicklung eines stochastischen ROI-Modells mittels Monte-Carlo-Simulation.

2. Theoretischer Hintergrund

Investitionsrechnung unter Unsicherheit: Warum der traditionelle ROI limitiert ist.

Ex-ante vs. Ex-post Steuerung: Theoretische Einordnung eures Setups. Erklärung, dass es sich um eine "Fire-and-Forget"-Investition aus Sicht des Bewertenden handelt, da nach Bewilligung des Antrags keine "In-the-loop"-Eingriffe mehr modelliert werden.

Funktionsweise der Monte-Carlo-Simulation: Das Gesetz der großen Zahlen und die Aggregation von Einzelrisiken zu einer Gesamtrisikoverteilung.

3. Methodik und Modelldesign (Dein Hauptteil)

Variablenselektion: Vorstellung der 4 Inputgrößen (Preis, Volumen, CAPEX, OPEX) und Begründung, warum diese das Risikoprofil dominieren.

Verteilungsannahmen (Stochastische Modellierung): Hier argumentierst du, warum ihr euch für PERT/Dreiecksverteilungen (für Expertenschätzungen) und Lognormalverteilungen (für den Preis) entscheidet.

Mathematisches Modell: Darstellung der ROI-Gleichung, die in der Simulation iteriert wird.

4. Simulation und Ergebnisse

Beschreibung des Datensatzes (fiktive oder anonymisierte Antragsdaten).

Durchführung der Simulation (z.B. 10.000 Iterationen).

Auswertung der Output-Verteilung: Statt eines einzigen ROI-Wertes präsentiert ihr ein Histogramm. Wichtige Kennzahlen hier: Erwartungswert des ROI (Mean), Standardabweichung (Volatilität) und die Wahrscheinlichkeit eines negativen ROI (Value at Risk).

5. Diskussion und Limitationen

Kritische Reflexion: Die Qualität der Simulation hängt von der Güte der Antragsdaten ab ("Garbage in, Garbage out").

Diskussion des fehlenden Ex-post-Einflusses: Wie würde sich das Risiko verändern, wenn man Realoptionen (z.B. die Option, das Projekt später abzubrechen) hätte?

6. Fazit

Zusammenfassung des Mehrwerts der MCS für die finale Investitionsentscheidung.

Um dir ein Gefühl dafür zu geben, wie die Verteilungen dieser vier Variablen das finale Risiko (die Form des Histogramms) beeinflussen, habe ich dir einen interaktiven Simulator gebaut. Du kannst hier mit den Antragsdaten (Min, Max, Modus) spielen und sehen, wie sich die Streuung des ROI verändert.
