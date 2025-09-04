import os
import pandas as pd
import numpy as np
from datetime import datetime
import random


class DataManager:
    """Handles data generation and loading for PSU analysis"""

    def generate_psu_data(self, num_psus=20, years=5):
        """Generate simplified synthetic financial data for PSUs"""
        np.random.seed(42)

        sectors = ["Energy", "Manufacturing",
                   "Mining", "Transportation", "Telecom"]
        psu_names = [f"PSU_{i+1}" for i in range(num_psus)]
        current_year = datetime.now().year
        years_list = [current_year - i for i in range(years, 0, -1)]

        data = []

        for psu in psu_names:
            sector = random.choice(sectors)
            size = random.choice(["Large", "Medium", "Small"])

            # Base financial metrics that will grow/change over years
            base_revenue = np.random.uniform(1000, 10000) if size == "Large" else \
                np.random.uniform(500, 2000) if size == "Medium" else \
                np.random.uniform(100, 500)

            base_profit_margin = np.random.uniform(0.08, 0.20)
            base_debt_equity = np.random.uniform(0.5, 2.0)

            # Growth/trend factor
            trend_factor = np.random.uniform(-0.1, 0.15)

            for year in years_list:
                year_index = years_list.index(year)

                # Generate metrics with some trend and randomness
                revenue_growth = trend_factor + np.random.uniform(-0.05, 0.05)
                current_revenue = base_revenue * \
                    (1 + revenue_growth) ** year_index

                profit_margin = max(min(base_profit_margin + trend_factor *
                                    year_index/5 + np.random.uniform(-0.02, 0.02), 0.35), -0.2)
                net_profit = current_revenue * profit_margin

                debt_equity = base_debt_equity + year_index * \
                    trend_factor/3 + np.random.uniform(-0.1, 0.1)

                # Calculate ROE
                assets = current_revenue * np.random.uniform(1.5, 3.0)
                liabilities = assets * np.random.uniform(0.4, 0.7)
                equity = assets - liabilities
                roe = net_profit / equity if equity > 0 else 0

                data.append({
                    "PSU_Name": psu,
                    "Sector": sector,
                    "Size": size,
                    "Year": year,
                    "Revenue": round(current_revenue, 2),
                    "Net_Profit": round(net_profit, 2),
                    "Profit_Margin": round(profit_margin, 4),
                    "Debt_Equity": round(debt_equity, 2),
                    "ROE": round(roe, 4),
                    "Assets": round(assets, 2),
                    "Liabilities": round(liabilities, 2)
                })

        return pd.DataFrame(data)

    def load_data(self):
        """Load or generate PSU data"""
        try:
            return pd.read_csv("data/psu_data.csv")
        except FileNotFoundError:
            df = self.generate_psu_data()
            df.to_csv("data/psu_data.csv", index=False)
            return df
