# EnergyStorageIntradayTrading
Using Python to create an intraday energy trading algorithm for energy storage systems with under set constraints.
This project aims to develop a simplified trading algorithm for an energy storage system that estimates the cycle costs required to achieve a specific average daily cycle count under certain constraints. The project uses a dataset of price signals for every 15-minute intervals each a day for year. The algorithm should account for a list of things, namely:
1. The nominal power of the storage: 2 MW
1. The usable capacity of the storage: 4 MWh
1. The efficiency of the energy storage: (0.9) 90%
1. The target average cycles per 24-hour time horizon: 1.5
1. The maximum number of cycles per 24-hour time horizon: 2.5

The project uses different approaches in attempting to maximize the potential profits while remaining within the constraints by identifying the best cycles within a day to buy and sell energy. 

Each method, from the combinatory heuristic to the mathematical Linear Programming approach, was rigorously tested. The final globally-optimal Linear Programming approach successfully identifies optimal trading cycles across the entire year dataset, avoiding local-optima pitfalls and strictly adhering to average and daily cycle capacity constraints without breaches.

This algorithm serves as an robust proof-of-concept for how trading desks model energy storage physically. For those interested in a more detailed analysis, including insights into why heuristics fall short and a walkthrough of the global LP implementation, I invite you to read [my in-depth "Part Two" blog post](part-two-trading.md). You can also run the new optimized LP algorithm in the `intraday_lp.ipynb` Jupyter Notebook locally.
