import pandas as pd
import numpy as np
import json


class AnalysisToolkit:
    """Provides simplified analysis tools for PSU data"""

    def __init__(self, df):
        self.df = df

    def get_dataset_overview(self):
        """Get a high-level overview of the dataset"""
        # Latest year data
        latest_year = self.df['Year'].max()
        latest_data = self.df[self.df['Year'] == latest_year]

        # Count PSUs and sectors
        psu_count = len(self.df['PSU_Name'].unique())
        sector_count = len(self.df['Sector'].unique())
        sectors = self.df['Sector'].unique().tolist()

        # Year range
        year_min = self.df['Year'].min()
        year_max = self.df['Year'].max()

        # Financial summary
        total_revenue = latest_data['Revenue'].sum()
        profitable_psus = sum(latest_data['Net_Profit'] > 0)
        loss_making_psus = sum(latest_data['Net_Profit'] <= 0)

        return {
            "psu_count": psu_count,
            "sector_count": sector_count,
            "sectors": sectors,
            "year_range": f"{year_min} to {year_max}",
            "latest_year": int(latest_year),
            "total_revenue": float(total_revenue),
            "profitable_psus": int(profitable_psus),
            "loss_making_psus": int(loss_making_psus)
        }

    def get_psu_data(self, psu_name=None):
        """
        Get financial data for a specific PSU or all PSUs

        Parameters:
        - psu_name: Name of the PSU (or "all" for all PSUs)

        Returns:
        - List of financial records or error message
        """
        if psu_name and psu_name != "all":
            if psu_name not in self.df['PSU_Name'].unique():
                return {"error": f"PSU '{psu_name}' not found"}
            filtered_df = self.df[self.df['PSU_Name'] == psu_name]
        else:
            filtered_df = self.df

        return filtered_df.to_dict(orient='records')

    def get_sector_data(self, sector=None):
        """
        Get data for a specific sector or list of all sectors

        Parameters:
        - sector: Name of the sector (or "all" for all sectors)

        Returns:
        - List of financial records or error message
        """
        if sector and sector != "all":
            if sector not in self.df['Sector'].unique():
                return {"error": f"Sector '{sector}' not found"}

            # Get latest year data for each PSU in the sector
            latest_year_data = self.df.sort_values(
                'Year').groupby('PSU_Name').tail(1)
            filtered_df = latest_year_data[latest_year_data['Sector'] == sector]
            return filtered_df.to_dict(orient='records')
        else:
            sectors = self.df['Sector'].unique().tolist()
            return {"sectors": sectors}

    def analyze_psu(self, psu_name):
        """
        Analyze a specific PSU's financial performance

        Parameters:
        - psu_name: Name of the PSU

        Returns:
        - Dictionary with financial metrics and trend analysis
        """
        if psu_name not in self.df['PSU_Name'].unique():
            return {"error": f"PSU '{psu_name}' not found"}

        # Get PSU data sorted by year
        psu_data = self.df[self.df['PSU_Name'] == psu_name].sort_values('Year')

        # Get sector information
        sector = psu_data['Sector'].iloc[0]

        # Extract financial metrics by year
        yearly_metrics = {
            "years": psu_data['Year'].tolist(),
            "revenue": psu_data['Revenue'].tolist(),
            "net_profit": psu_data['Net_Profit'].tolist(),
            "profit_margin": psu_data['Profit_Margin'].tolist(),
            "debt_equity": psu_data['Debt_Equity'].tolist(),
            "roe": psu_data['ROE'].tolist()
        }

        # Calculate trends if we have multiple years
        trends = {}
        if len(psu_data) > 1:
            # Revenue growth
            first_year_revenue = psu_data['Revenue'].iloc[0]
            last_year_revenue = psu_data['Revenue'].iloc[-1]
            revenue_growth = (
                (last_year_revenue / first_year_revenue) - 1) * 100

            # Profit margin change
            first_year_margin = psu_data['Profit_Margin'].iloc[0]
            last_year_margin = psu_data['Profit_Margin'].iloc[-1]
            margin_change = last_year_margin - first_year_margin

            trends = {
                "revenue_growth_percent": round(revenue_growth, 2),
                "profit_margin_change": round(margin_change, 4),
                "latest_year_profit": round(float(psu_data['Net_Profit'].iloc[-1]), 2),
                "trend_direction": "improving" if revenue_growth > 0 and margin_change > 0 else
                "mixed" if (revenue_growth > 0) != (margin_change > 0) else
                "declining"
            }

        return {
            "psu_name": psu_name,
            "sector": sector,
            "size": psu_data['Size'].iloc[0],
            "latest_year": int(psu_data['Year'].iloc[-1]),
            "yearly_metrics": yearly_metrics,
            "trends": trends
        }

    def compare_with_sector(self, psu_name):
        """
        Compare a PSU with its sector averages

        Parameters:
        - psu_name: Name of the PSU

        Returns:
        - Dictionary with comparison metrics
        """
        if psu_name not in self.df['PSU_Name'].unique():
            return {"error": f"PSU '{psu_name}' not found"}

        # Get PSU data for the latest year
        psu_latest = self.df[self.df['PSU_Name'] ==
                             psu_name].sort_values('Year').iloc[-1]
        sector = psu_latest['Sector']

        # Get latest data for the sector
        latest_year_data = self.df.sort_values(
            'Year').groupby('PSU_Name').tail(1)
        sector_data = latest_year_data[latest_year_data['Sector'] == sector]

        # Calculate sector averages
        sector_avg = {
            "revenue": float(sector_data['Revenue'].mean()),
            "profit_margin": float(sector_data['Profit_Margin'].mean()),
            "debt_equity": float(sector_data['Debt_Equity'].mean()),
            "roe": float(sector_data['ROE'].mean())
        }

        # Calculate PSU's percentile in the sector
        def percentile_rank(series, value):
            return (series < value).mean() * 100

        percentiles = {
            "revenue": float(percentile_rank(sector_data['Revenue'], psu_latest['Revenue'])),
            "profit_margin": float(percentile_rank(sector_data['Profit_Margin'], psu_latest['Profit_Margin'])),
            "roe": float(percentile_rank(sector_data['ROE'], psu_latest['ROE']))
        }

        return {
            "psu_name": psu_name,
            "sector": sector,
            "psu_metrics": {
                "revenue": float(psu_latest['Revenue']),
                "profit_margin": float(psu_latest['Profit_Margin']),
                "debt_equity": float(psu_latest['Debt_Equity']),
                "roe": float(psu_latest['ROE'])
            },
            "sector_averages": sector_avg,
            "percentile_rankings": percentiles
        }

    def identify_top_performers(self, sector=None, metric="ROE", top_n=5):
        """
        Identify top performing PSUs based on a specified metric

        Parameters:
        - sector: Optional sector filter
        - metric: Financial metric to rank by (ROE, Profit_Margin, Revenue)
        - top_n: Number of top performers to return

        Returns:
        - Dictionary with top performers and relevant metrics
        """
        valid_metrics = ["ROE", "Profit_Margin",
                         "Revenue", "Net_Profit", "Debt_Equity"]
        if metric not in valid_metrics:
            return {"error": f"Invalid metric: {metric}. Valid options are: {', '.join(valid_metrics)}"}

        # Get latest year data for each PSU
        latest_data = self.df.sort_values('Year').groupby('PSU_Name').tail(1)

        # Filter by sector if specified
        if sector and sector != "all":
            if sector not in self.df['Sector'].unique():
                return {"error": f"Sector '{sector}' not found"}
            filtered_data = latest_data[latest_data['Sector'] == sector]
        else:
            filtered_data = latest_data

        # Sort by metric (lower is better for Debt_Equity)
        ascending = True if metric == "Debt_Equity" else False
        sorted_data = filtered_data.sort_values(metric, ascending=ascending)

        # Extract top performers
        top_performers = []
        for _, row in sorted_data.head(top_n).iterrows():
            top_performers.append({
                "psu_name": row['PSU_Name'],
                "sector": row['Sector'],
                "metric_value": float(row[metric]),
                "profit": float(row['Net_Profit']),
                "revenue": float(row['Revenue']),
                "size": row['Size']
            })

        return {
            "metric": metric,
            "top_performers": top_performers,
            "average_value": float(filtered_data[metric].mean())
        }

    def analyze_sector(self, sector):
        """
        Analyze a specific sector's performance

        Parameters:
        - sector: Name of the sector

        Returns:
        - Dictionary with sector analysis metrics
        """
        if sector not in self.df['Sector'].unique():
            return {"error": f"Sector '{sector}' not found"}

        # Get all PSUs in this sector
        sector_data = self.df[self.df['Sector'] == sector]

        # Get unique years in descending order
        years = sorted(sector_data['Year'].unique(), reverse=True)

        # Calculate yearly metrics
        yearly_metrics = []
        for year in years:
            year_data = sector_data[sector_data['Year'] == year]

            yearly_metrics.append({
                "year": int(year),
                "total_revenue": float(year_data['Revenue'].sum()),
                "total_profit": float(year_data['Net_Profit'].sum()),
                "avg_profit_margin": float(year_data['Profit_Margin'].mean()),
                "avg_roe": float(year_data['ROE'].mean()),
                "avg_debt_equity": float(year_data['Debt_Equity'].mean()),
                "profitable_psus": int(sum(year_data['Net_Profit'] > 0)),
                "loss_making_psus": int(sum(year_data['Net_Profit'] <= 0))
            })

        # Get latest year data for all PSUs in the sector
        latest_year = max(years)
        latest_data = sector_data[sector_data['Year'] == latest_year]

        # Find best and worst performers
        best_psu = latest_data.loc[latest_data['ROE'].idxmax(
        )]['PSU_Name'] if len(latest_data) > 0 else "N/A"
        worst_psu = latest_data.loc[latest_data['ROE'].idxmin(
        )]['PSU_Name'] if len(latest_data) > 0 else "N/A"

        return {
            "sector": sector,
            "psu_count": len(sector_data['PSU_Name'].unique()),
            "yearly_metrics": yearly_metrics,
            "latest_year": int(latest_year),
            "best_performer": best_psu,
            "worst_performer": worst_psu
        }
