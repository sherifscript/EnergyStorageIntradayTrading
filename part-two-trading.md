---
layout: post
title: "Intraday Trading Algorithm for Energy Storage Systems - Part Two: The Optimization Approach"
description: "Why the greedy heuristic failed and how Linear Programming provides the global optimum for energy trading."
---

## Intraday Trading Algorithm for Energy Storage Systems: Part Two

In my [previous post](https://asherif.me/1intraday-trading-energy-storage-systems.html), I documented my initial attempt at developing an algorithm to estimate the cycle costs for an energy storage system. That approach relied heavily on a **combinatory (greedy) algorithm**. While it was a great learning experience and an intuitive starting point, it ultimately failed to meet all the constraints robustly and optimally. 

Here is a deeper dive into why that first approach didn't work out as planned and how I rebuilt the solution using **Linear Programming (LP)** to successfully complete the challenge.

### Why the Combinatory Approach Failed

The initial heuristic calculated spreads for all possible pairs of buy and sell intervals within a 24-hour horizon, prioritized the most profitable, and greedily selected them. However, energy storage is fundamentally an intertemporal optimization problem. The greedy approach ran into a few critical flaws:

1. **Local vs. Global Optima:** By greedily picking the highest spreads first, the algorithm trapped itself in local optima. It failed to recognize that sacrificing a slightly better spread now could unlock substantially better compounding opportunities later in the day.
2. **Cycle Constraints Mismanagement:** The problem requires hitting a strict *average* of 1.5 cycles per day across the trading horizon while ensuring no single day breaches 2.5 cycles. A greedy combinatory check limited cycles strictly on a daily basis (often breaching limits due to overlapping conditions) and completely ignored the global average requirement.
3. **Imperfect State of Charge (SoC) Tracking:** Checking overlapping intervals with a `used_intervals` set completely bypassed the continuous nature of battery charging. You don't have to fully charge and fully discharge in independent blocks; you can partially charge, wait, and charge some more.

### The True Solution: Linear Programming

To properly solve this, the problem must be modeled mathematically. By transitioning to a Linear Programming (LP) framework, we can explicitly define our physics, capacities, and business goals as linear constraints, and let an optimization solver (like the Highs solver in `scipy.optimize`) find the absolute maximum profit.

#### Defining the Optimization Model

We divide the trading horizon into 15-minute intervals ($t$). For each interval, we have three continuous variables:
*   $P_{ch}(t)$: Power charged (MW)
*   $P_{dis}(t)$: Power discharged (MW)
*   $E(t)$: State of Charge / Energy in the battery (MWh)

**Objective Function:**
Maximize the total profit over the entire grid period:
$$\text{Maximize} \sum \left( \text{Price}(t) \times (P_{dis}(t) - P_{ch}(t)) \times \Delta t \right)$$

**Constraints:**
1.  **Power Bounds:** Both charging and discharging power are bounded between $0$ and the nominal power ($2$ MW).
2.  **Capacity Bounds:** The energy state $E(t)$ is strictly bounded between $0$ and the usable capacity ($4$ MWh).
3.  **Energy Balance:** The energy in the battery at time $t$ depends on the previous state and the efficiency ($\eta = 0.9$):
    $$E(t) - E(t-1) = \left( P_{ch}(t) \times \eta - \frac{P_{dis}(t)}{\eta} \right) \times \Delta t$$
4.  **Daily Maximum Cycles:** For each day $d$, the total discharged energy cannot exceed $2.5 \times \text{Capacity}$:
    $$\sum_{t \in \text{day } d} P_{dis}(t) \times \Delta t \le 10 \text{ MWh}$$
5.  **Average Target Cycles:** Over the entire data horizon ($N$ days), the average cycles must be precisely $1.5$:
    $$\sum_{\text{all } t} P_{dis}(t) \times \Delta t = 1.5 \times 4 \text{ MWh} \times N$$

### Results

By defining strict matrix representations for `A_eq` and `A_ub` and executing the solver across the massive year-long dataset (over 105,000 variables using `scipy.sparse` to manage memory!), the solver achieves a mathematically proven global optimum.

*   **Average Daily Cycles:** Exactly 1.5
*   **Total Cycles Over 1 Year:** 547.5
*   **Constraint Breaches:** 0 (Greedy approach breached multiple capacity & cycle limits).

### Conclusion

This interview challenge proved the immense value of transitioning from *heuristic programming* to *mathematical optimization* in Data Science. The ability to abstract a physical energy asset into equality and inequality matrices completely removes the guesswork. This is exactly how modern intraday trading desks at energy utilities operate.

You can find the updated LP solver script (`intraday_lp.py`) directly on the [GitHub Repository](https://github.com/sherifscript/EnergyStorageIntradayTrading)!
