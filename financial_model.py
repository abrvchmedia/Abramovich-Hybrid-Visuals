#!/usr/bin/env python3
"""
Abramovich Hybrid Visuals - Financial Projections Generator
Generates investor-ready financial models for multiple revenue tiers
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
from pathlib import Path


class FinancialModel:
    """Generate comprehensive financial projections for media production company"""
    
    def __init__(self, tier_name, annual_revenue_target):
        self.tier_name = tier_name
        self.annual_revenue_target = annual_revenue_target
        self.assumptions = self._build_assumptions()
        
    def _build_assumptions(self):
        """Build tier-specific assumptions based on revenue target"""
        target = self.annual_revenue_target
        
        # Scale assumptions based on tier
        if target <= 100000:
            return {
                'tier': 'Startup',
                'annual_revenue_target': target,
                
                # Production Revenue
                'avg_production_contract': 8000,
                'production_projects_y1': int(target * 0.60 / 8000),  # 60% from production
                'production_direct_cost_pct': 0.50,
                
                # Marketing Revenue
                'avg_monthly_marketing_retainer': 2500,
                'marketing_clients_y1': int(target * 0.30 / (2500 * 12)),  # 30% from marketing
                
                # Media/Distribution Revenue  
                'avg_media_deployment_fee': 1500,
                'media_projects_y1': int(target * 0.10 / 1500),  # 10% from media
                
                # Operating Costs
                'annual_payroll': int(target * 0.25),
                'annual_overhead': int(target * 0.15),
                
                # Growth
                'year_2_growth': 0.50,
                'year_3_growth': 0.40,
            }
        elif target <= 500000:
            return {
                'tier': 'Growth',
                'annual_revenue_target': target,
                
                'avg_production_contract': 15000,
                'production_projects_y1': int(target * 0.55 / 15000),
                'production_direct_cost_pct': 0.48,
                
                'avg_monthly_marketing_retainer': 3500,
                'marketing_clients_y1': int(target * 0.35 / (3500 * 12)),
                
                'avg_media_deployment_fee': 2500,
                'media_projects_y1': int(target * 0.10 / 2500),
                
                'annual_payroll': int(target * 0.30),
                'annual_overhead': int(target * 0.18),
                
                'year_2_growth': 0.40,
                'year_3_growth': 0.35,
            }
        elif target <= 1000000:
            return {
                'tier': 'Scale',
                'annual_revenue_target': target,
                
                'avg_production_contract': 25000,
                'production_projects_y1': int(target * 0.50 / 25000),
                'production_direct_cost_pct': 0.45,
                
                'avg_monthly_marketing_retainer': 5000,
                'marketing_clients_y1': int(target * 0.40 / (5000 * 12)),
                
                'avg_media_deployment_fee': 4000,
                'media_projects_y1': int(target * 0.10 / 4000),
                
                'annual_payroll': int(target * 0.32),
                'annual_overhead': int(target * 0.20),
                
                'year_2_growth': 0.35,
                'year_3_growth': 0.30,
            }
        else:  # $2M+
            return {
                'tier': 'Enterprise',
                'annual_revenue_target': target,
                
                'avg_production_contract': 50000,
                'production_projects_y1': int(target * 0.45 / 50000),
                'production_direct_cost_pct': 0.42,
                
                'avg_monthly_marketing_retainer': 8000,
                'marketing_clients_y1': int(target * 0.45 / (8000 * 12)),
                
                'avg_media_deployment_fee': 6000,
                'media_projects_y1': int(target * 0.10 / 6000),
                
                'annual_payroll': int(target * 0.35),
                'annual_overhead': int(target * 0.22),
                
                'year_2_growth': 0.30,
                'year_3_growth': 0.25,
            }
    
    def generate_production_pl(self):
        """Generate production division P&L"""
        a = self.assumptions
        
        # Calculate actual revenue mix
        prod_revenue = a['avg_production_contract'] * a['production_projects_y1']
        prod_cogs = prod_revenue * a['production_direct_cost_pct']
        
        pl = {
            'Division': 'Production',
            'Year_1': {
                'Revenue': prod_revenue,
                'COGS': prod_cogs,
                'Gross_Profit': prod_revenue - prod_cogs,
                'Gross_Margin': (prod_revenue - prod_cogs) / prod_revenue if prod_revenue > 0 else 0,
            }
        }
        
        # Year 2 & 3 projections
        for year in [2, 3]:
            growth_key = f'year_{year}_growth'
            prev_year = f'Year_{year-1}'
            curr_year = f'Year_{year}'
            
            revenue = pl[prev_year]['Revenue'] * (1 + a[growth_key])
            cogs = revenue * a['production_direct_cost_pct']
            
            pl[curr_year] = {
                'Revenue': revenue,
                'COGS': cogs,
                'Gross_Profit': revenue - cogs,
                'Gross_Margin': (revenue - cogs) / revenue,
            }
        
        return pl
    
    def generate_marketing_pl(self):
        """Generate marketing division P&L"""
        a = self.assumptions
        
        # Marketing has lower COGS (mostly labor/tools)
        mrr_revenue = a['avg_monthly_marketing_retainer'] * a['marketing_clients_y1'] * 12
        mrr_cogs = mrr_revenue * 0.25  # 25% COGS for marketing
        
        pl = {
            'Division': 'Marketing',
            'Year_1': {
                'Revenue': mrr_revenue,
                'COGS': mrr_cogs,
                'Gross_Profit': mrr_revenue - mrr_cogs,
                'Gross_Margin': (mrr_revenue - mrr_cogs) / mrr_revenue if mrr_revenue > 0 else 0,
            }
        }
        
        for year in [2, 3]:
            growth_key = f'year_{year}_growth'
            prev_year = f'Year_{year-1}'
            curr_year = f'Year_{year}'
            
            revenue = pl[prev_year]['Revenue'] * (1 + a[growth_key])
            cogs = revenue * 0.25
            
            pl[curr_year] = {
                'Revenue': revenue,
                'COGS': cogs,
                'Gross_Profit': revenue - cogs,
                'Gross_Margin': (revenue - cogs) / revenue,
            }
        
        return pl
    
    def generate_media_pl(self):
        """Generate media/distribution division P&L"""
        a = self.assumptions
        
        # Media deployment has minimal COGS
        media_revenue = a['avg_media_deployment_fee'] * a['media_projects_y1']
        media_cogs = media_revenue * 0.15  # 15% COGS for media
        
        pl = {
            'Division': 'Media/Distribution',
            'Year_1': {
                'Revenue': media_revenue,
                'COGS': media_cogs,
                'Gross_Profit': media_revenue - media_cogs,
                'Gross_Margin': (media_revenue - media_cogs) / media_revenue if media_revenue > 0 else 0,
            }
        }
        
        for year in [2, 3]:
            growth_key = f'year_{year}_growth'
            prev_year = f'Year_{year-1}'
            curr_year = f'Year_{year}'
            
            revenue = pl[prev_year]['Revenue'] * (1 + a[growth_key])
            cogs = revenue * 0.15
            
            pl[curr_year] = {
                'Revenue': revenue,
                'COGS': cogs,
                'Gross_Profit': revenue - cogs,
                'Gross_Margin': (revenue - cogs) / revenue,
            }
        
        return pl
    
    def generate_consolidated_pl(self):
        """Generate consolidated P&L combining all divisions"""
        prod_pl = self.generate_production_pl()
        mkt_pl = self.generate_marketing_pl()
        media_pl = self.generate_media_pl()
        
        a = self.assumptions
        
        consolidated = {'Division': 'Consolidated'}
        
        for year in ['Year_1', 'Year_2', 'Year_3']:
            total_revenue = (prod_pl[year]['Revenue'] + 
                           mkt_pl[year]['Revenue'] + 
                           media_pl[year]['Revenue'])
            
            total_cogs = (prod_pl[year]['COGS'] + 
                         mkt_pl[year]['COGS'] + 
                         media_pl[year]['COGS'])
            
            gross_profit = total_revenue - total_cogs
            
            # Operating expenses scale with revenue
            year_num = int(year.split('_')[1])
            if year_num == 1:
                payroll = a['annual_payroll']
                overhead = a['annual_overhead']
            else:
                growth = a[f'year_{year_num}_growth']
                payroll = consolidated[f'Year_{year_num-1}']['Payroll'] * (1 + growth * 0.8)
                overhead = consolidated[f'Year_{year_num-1}']['Overhead'] * (1 + growth * 0.6)
            
            operating_expenses = payroll + overhead
            operating_income = gross_profit - operating_expenses
            
            consolidated[year] = {
                'Revenue': total_revenue,
                'COGS': total_cogs,
                'Gross_Profit': gross_profit,
                'Gross_Margin': gross_profit / total_revenue if total_revenue > 0 else 0,
                'Payroll': payroll,
                'Overhead': overhead,
                'Operating_Expenses': operating_expenses,
                'Operating_Income': operating_income,
                'Operating_Margin': operating_income / total_revenue if total_revenue > 0 else 0,
                'EBITDA': operating_income,  # Simplified - no D&A in early stage
                'EBITDA_Margin': operating_income / total_revenue if total_revenue > 0 else 0,
            }
        
        return consolidated
    
    def generate_cash_flow(self):
        """Generate cash flow statement with quarterly breakdown"""
        consolidated = self.generate_consolidated_pl()
        
        # Year 1 quarterly cash flow
        q1_revenue = consolidated['Year_1']['Revenue'] * 0.20  # Ramp up
        q2_revenue = consolidated['Year_1']['Revenue'] * 0.23
        q3_revenue = consolidated['Year_1']['Revenue'] * 0.27
        q4_revenue = consolidated['Year_1']['Revenue'] * 0.30
        
        cash_flow = {
            'Year_1_Quarterly': {
                'Q1': {
                    'Revenue': q1_revenue,
                    'Operating_Cash_Flow': q1_revenue * consolidated['Year_1']['Operating_Margin'],
                    'Cumulative_Cash': q1_revenue * consolidated['Year_1']['Operating_Margin'],
                },
                'Q2': {
                    'Revenue': q2_revenue,
                    'Operating_Cash_Flow': q2_revenue * consolidated['Year_1']['Operating_Margin'],
                    'Cumulative_Cash': 0,  # Will calculate
                },
                'Q3': {
                    'Revenue': q3_revenue,
                    'Operating_Cash_Flow': q3_revenue * consolidated['Year_1']['Operating_Margin'],
                    'Cumulative_Cash': 0,
                },
                'Q4': {
                    'Revenue': q4_revenue,
                    'Operating_Cash_Flow': q4_revenue * consolidated['Year_1']['Operating_Margin'],
                    'Cumulative_Cash': 0,
                },
            }
        }
        
        # Calculate cumulative
        cumulative = cash_flow['Year_1_Quarterly']['Q1']['Cumulative_Cash']
        for q in ['Q2', 'Q3', 'Q4']:
            cumulative += cash_flow['Year_1_Quarterly'][q]['Operating_Cash_Flow']
            cash_flow['Year_1_Quarterly'][q]['Cumulative_Cash'] = cumulative
        
        # Annual summary
        cash_flow['Annual'] = {
            'Year_1': consolidated['Year_1']['Operating_Income'],
            'Year_2': consolidated['Year_2']['Operating_Income'],
            'Year_3': consolidated['Year_3']['Operating_Income'],
        }
        
        return cash_flow
    
    def generate_investor_waterfall(self, investment_amount):
        """Generate investor recoupment waterfall"""
        consolidated = self.generate_consolidated_pl()
        
        # Simple waterfall: investors get 100% until recoupment, then pro-rata
        cumulative_cash = 0
        recouped = False
        recoupment_period = None
        
        waterfall = []
        
        for year in ['Year_1', 'Year_2', 'Year_3']:
            operating_income = consolidated[year]['Operating_Income']
            
            if not recouped:
                if cumulative_cash + operating_income >= investment_amount:
                    to_investor = investment_amount - cumulative_cash
                    remaining = operating_income - to_investor
                    to_company = remaining * 0.5  # 50/50 split after recoupment
                    to_investor += remaining * 0.5
                    recouped = True
                    recoupment_period = year
                else:
                    to_investor = operating_income
                    to_company = 0
                
                cumulative_cash += operating_income
            else:
                # Post-recoupment: 50/50 split
                to_investor = operating_income * 0.5
                to_company = operating_income * 0.5
                cumulative_cash += operating_income
            
            waterfall.append({
                'Year': year,
                'Operating_Income': operating_income,
                'To_Investor': to_investor,
                'To_Company': to_company,
                'Cumulative_To_Investor': sum(w['To_Investor'] for w in waterfall) + to_investor,
                'Recouped': recouped,
            })
        
        return {
            'Investment_Amount': investment_amount,
            'Recoupment_Period': recoupment_period,
            'Waterfall': waterfall,
        }
    
    def generate_scenarios(self):
        """Generate Conservative, Target, and Upside scenarios"""
        
        # Base model is "Target"
        target_consolidated = self.generate_consolidated_pl()
        
        # Conservative: -20% revenue, same costs
        conservative = self.generate_consolidated_pl()
        for year in ['Year_1', 'Year_2', 'Year_3']:
            conservative[year]['Revenue'] *= 0.80
            conservative[year]['COGS'] *= 0.80
            conservative[year]['Gross_Profit'] = conservative[year]['Revenue'] - conservative[year]['COGS']
            conservative[year]['Operating_Income'] = conservative[year]['Gross_Profit'] - conservative[year]['Operating_Expenses']
            conservative[year]['Operating_Margin'] = conservative[year]['Operating_Income'] / conservative[year]['Revenue'] if conservative[year]['Revenue'] > 0 else 0
        
        # Upside: +30% revenue, +10% costs
        upside = self.generate_consolidated_pl()
        for year in ['Year_1', 'Year_2', 'Year_3']:
            upside[year]['Revenue'] *= 1.30
            upside[year]['COGS'] *= 1.30
            upside[year]['Operating_Expenses'] *= 1.10
            upside[year]['Gross_Profit'] = upside[year]['Revenue'] - upside[year]['COGS']
            upside[year]['Operating_Income'] = upside[year]['Gross_Profit'] - upside[year]['Operating_Expenses']
            upside[year]['Operating_Margin'] = upside[year]['Operating_Income'] / upside[year]['Revenue'] if upside[year]['Revenue'] > 0 else 0
        
        return {
            'Conservative': conservative,
            'Target': target_consolidated,
            'Upside': upside,
        }
    
    def export_to_dict(self):
        """Export full model to dictionary"""
        return {
            'tier_name': self.tier_name,
            'assumptions': self.assumptions,
            'production_pl': self.generate_production_pl(),
            'marketing_pl': self.generate_marketing_pl(),
            'media_pl': self.generate_media_pl(),
            'consolidated_pl': self.generate_consolidated_pl(),
            'cash_flow': self.generate_cash_flow(),
            'scenarios': self.generate_scenarios(),
            'generated_at': datetime.now().isoformat(),
        }
    
    def export_to_excel(self, filename):
        """Export model to Excel workbook"""
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Assumptions
            pd.DataFrame([self.assumptions]).T.to_excel(writer, sheet_name='Assumptions')
            
            # P&Ls
            for name, pl_func in [
                ('Production', self.generate_production_pl),
                ('Marketing', self.generate_marketing_pl),
                ('Media', self.generate_media_pl),
                ('Consolidated', self.generate_consolidated_pl),
            ]:
                df = pd.DataFrame(pl_func()).T
                df.to_excel(writer, sheet_name=name)
            
            # Cash Flow
            cf = self.generate_cash_flow()
            pd.DataFrame(cf['Year_1_Quarterly']).T.to_excel(writer, sheet_name='Cash Flow Q')
            pd.DataFrame([cf['Annual']]).T.to_excel(writer, sheet_name='Cash Flow Annual')
            
            # Scenarios
            scenarios = self.generate_scenarios()
            for scenario_name, scenario_data in scenarios.items():
                df = pd.DataFrame(scenario_data).T
                df.to_excel(writer, sheet_name=f'Scenario_{scenario_name}')


def generate_all_tiers():
    """Generate models for all requested tiers"""
    tiers = [
        ('$100K', 100000),
        ('$500K', 500000),
        ('$1M', 1000000),
        ('$2M', 2000000),
    ]
    
    models = {}
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    for tier_name, revenue in tiers:
        print(f"\nGenerating {tier_name} tier...")
        model = FinancialModel(tier_name, revenue)
        models[tier_name] = model
        
        # Export to JSON
        json_path = output_dir / f'financial_model_{tier_name}.json'
        with open(json_path, 'w') as f:
            json.dump(model.export_to_dict(), f, indent=2, default=str)
        print(f"  ✓ Exported JSON: {json_path}")
        
        # Export to Excel
        excel_path = output_dir / f'financial_model_{tier_name}.xlsx'
        model.export_to_excel(excel_path)
        print(f"  ✓ Exported Excel: {excel_path}")
    
    return models


if __name__ == '__main__':
    print("Abramovich Hybrid Visuals - Financial Projections Generator")
    print("=" * 60)
    models = generate_all_tiers()
    print("\n✓ All tiers generated successfully!")
    print(f"\nOutput directory: {Path('output').absolute()}")
