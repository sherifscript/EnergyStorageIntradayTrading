import pandas as pd
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

def solve_lp_global(df):
    nominal = 2  # MW
    capacity = 4  # MWh
    efficiency = 0.9
    dt = 0.25  # 15 min intervals
    max_cycles_per_day = 2.5
    target_average_cycles = 1.5
    
    price_data = df['EUR/MWh'].values
    n = len(price_data)
    num_days = n // 96
    
    # Variables: P_ch(t), P_dis(t), E(t)
    c = np.zeros(3 * n)
    for t in range(n):
        c[3 * t] = price_data[t] * dt
        c[3 * t + 1] = -price_data[t] * dt
        
    bounds = []
    for t in range(n):
        bounds.append((0, nominal))
        bounds.append((0, nominal))
        bounds.append((0, capacity))
        
    from scipy.sparse import lil_matrix
    
    # We have n energy balance eq constraints + 1 average cycle eq constraint
    A_eq_sparse = lil_matrix((n + 1, 3 * n))
    b_eq = np.zeros(n + 1)
    
    for t in range(n):
        A_eq_sparse[t, 3 * t + 2] = 1.0
        A_eq_sparse[t, 3 * t] = -efficiency * dt
        A_eq_sparse[t, 3 * t + 1] = (1.0 / efficiency) * dt
        if t > 0:
            A_eq_sparse[t, 3 * (t - 1) + 2] = -1.0
            
    # Equality constraint (average cycles over the whole period)
    # sum(P_dis * dt) over all t == target_average_cycles * capacity * num_days
    for t in range(n):
        A_eq_sparse[n, 3 * t + 1] = dt
    b_eq[n] = target_average_cycles * capacity * num_days
    
    # Inequality constraints (daily max cycles)
    # sum(P_dis * dt) for each day <= max_cycles_per_day * capacity
    A_ub_sparse = lil_matrix((num_days, 3 * n))
    b_ub = np.full(num_days, max_cycles_per_day * capacity)
    for d in range(num_days):
        for t in range(d * 96, (d + 1) * 96):
            if t < n:
                A_ub_sparse[d, 3 * t + 1] = dt
                
    print("Solving LP with Highs...")
    res = linprog(c, A_ub=A_ub_sparse, b_ub=b_ub, A_eq=A_eq_sparse, b_eq=b_eq, bounds=bounds, method='highs')
    
    if res.success:
        cost = res.fun
        x = res.x
        total_p_ch = sum(x[3*t] * dt for t in range(n))
        total_p_dis = sum(x[3*t+1] * dt for t in range(n))
        total_purchase_cost = sum(x[3*t] * dt * price_data[t] for t in range(n))
        total_sales_revenue = sum(x[3*t+1] * dt * price_data[t] for t in range(n))
        
        cycle_cost = (total_purchase_cost - total_sales_revenue) / total_p_ch
        
        return {
            'success': True,
            'profit': -cost,
            'cycle_cost': cycle_cost,
            'total_discharged': total_p_dis,
            'total_charged': total_p_ch,
            'total_cycles': total_p_dis / capacity,
            'average_daily_cycles': (total_p_dis / capacity) / num_days
        }
    else:
        return {'success': False}

if __name__ == '__main__':
    df = pd.read_csv('market_prices.csv', sep=';', parse_dates=['timestamp_UTC'], dayfirst=True)
    df = df.rename(columns={df.columns[1]: 'EUR/MWh'})
    
    res = solve_lp_global(df)
    print("Global LP Result:", res)
