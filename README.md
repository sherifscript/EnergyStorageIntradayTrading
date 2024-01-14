# EnergyStorageIntradayTrading
Using Python to create an intraday energy trading algorithm for energy storage systems with under set constraints.
This project aims to develop a simplified trading algorithm for an energy storage system that estimates the cycle costs required to achieve a specific average daily cycle count under certain constraints. The project uses a dataset of price signals for every 15-minute intervals each a day for year. The algorithm should account for a list of things, namely:
1. The nominal power of the storage: 2 MW
1. The usable capacity of the storage: 4 MWh
1. The efficiency of the energy storage: (0.9) 90%
1. The target average cycles per 24-hour time horizon: 1.5
1. The maximum number of cycles per 24-hour time horizon: 2.5

The project uses different approaches in attempting to maximize the potential profits while remaining within the constraints by identifying the best cycles within a day to buy and sell energy. 

Each method, from the combinatory to the rolling horizon to the constrained optimization approach, was rigorously tested to identify the most efficient cycles for buying and selling energy throughout the day. While the results demonstrated varying degrees of success, they collectively contributed to a deeper understanding of the intricate dynamics of energy markets. 

This is the first version of this project and the algorithm will be revisited. For those interested in a more detailed analysis of these findings, including insights into the methodologies and a walkthrough of the project,  I invite you to read [my in-depth blog post on my website](https://asherif.me/1intraday-trading-energy-storage-systems.html).
