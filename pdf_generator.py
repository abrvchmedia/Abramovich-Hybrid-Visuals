#!/usr/bin/env python3
"""
Investor Memorandum PDF Generator
Creates professional 12-page investor documents with charts and graphics
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, Frame, PageTemplate
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
from pathlib import Path
from datetime import datetime
from financial_model import FinancialModel

# Set style
plt.style.use('seaborn-v0_8-darkgrid')


class InvestorMemorandum:
    """Generate professional investor memorandum PDF"""
    
    def __init__(self, model, investment_amount=None):
        self.model = model
        self.assumptions = model.assumptions
        self.investment_amount = investment_amount or int(model.annual_revenue_target * 0.5)
        
        # Generate all financial data
        self.prod_pl = model.generate_production_pl()
        self.mkt_pl = model.generate_marketing_pl()
        self.media_pl = model.generate_media_pl()
        self.consolidated = model.generate_consolidated_pl()
        self.cash_flow = model.generate_cash_flow()
        self.scenarios = model.generate_scenarios()
        self.waterfall = model.generate_investor_waterfall(self.investment_amount)
        
        # Styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))
    
    def _format_currency(self, value):
        """Format value as currency"""
        if value >= 1000000:
            return f"${value/1000000:.2f}M"
        elif value >= 1000:
            return f"${value/1000:.1f}K"
        else:
            return f"${value:,.0f}"
    
    def _format_percent(self, value):
        """Format value as percentage"""
        return f"{value*100:.1f}%"
    
    def _create_chart_revenue_by_division(self, filename):
        """Create revenue by division chart"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        years = ['Year 1', 'Year 2', 'Year 3']
        production = [self.prod_pl[f'Year_{i}']['Revenue'] for i in [1, 2, 3]]
        marketing = [self.mkt_pl[f'Year_{i}']['Revenue'] for i in [1, 2, 3]]
        media = [self.media_pl[f'Year_{i}']['Revenue'] for i in [1, 2, 3]]
        
        x = np.arange(len(years))
        width = 0.25
        
        ax.bar(x - width, [p/1000 for p in production], width, label='Production', color='#3498db')
        ax.bar(x, [m/1000 for m in marketing], width, label='Marketing', color='#2ecc71')
        ax.bar(x + width, [m/1000 for m in media], width, label='Media', color='#e74c3c')
        
        ax.set_ylabel('Revenue ($K)', fontsize=12, fontweight='bold')
        ax.set_title('Revenue by Division (3-Year Projection)', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(years)
        ax.legend(frameon=True, shadow=True)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _create_chart_margin_analysis(self, filename):
        """Create margin analysis chart"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        years = ['Year 1', 'Year 2', 'Year 3']
        gross_margin = [self.consolidated[f'Year_{i}']['Gross_Margin']*100 for i in [1, 2, 3]]
        operating_margin = [self.consolidated[f'Year_{i}']['Operating_Margin']*100 for i in [1, 2, 3]]
        
        x = np.arange(len(years))
        width = 0.35
        
        ax.bar(x - width/2, gross_margin, width, label='Gross Margin', color='#9b59b6')
        ax.bar(x + width/2, operating_margin, width, label='Operating Margin', color='#e67e22')
        
        ax.set_ylabel('Margin (%)', fontsize=12, fontweight='bold')
        ax.set_title('Margin Analysis', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(years)
        ax.legend(frameon=True, shadow=True)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, (gm, om) in enumerate(zip(gross_margin, operating_margin)):
            ax.text(i - width/2, gm + 1, f'{gm:.1f}%', ha='center', fontweight='bold', fontsize=9)
            ax.text(i + width/2, om + 1, f'{om:.1f}%', ha='center', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _create_chart_cash_flow_quarterly(self, filename):
        """Create quarterly cash flow chart"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        quarters = ['Q1', 'Q2', 'Q3', 'Q4']
        cash_flow_data = [self.cash_flow['Year_1_Quarterly'][q]['Operating_Cash_Flow']/1000 
                         for q in quarters]
        cumulative_data = [self.cash_flow['Year_1_Quarterly'][q]['Cumulative_Cash']/1000 
                          for q in quarters]
        
        x = np.arange(len(quarters))
        width = 0.35
        
        ax.bar(x - width/2, cash_flow_data, width, label='Quarterly Operating Cash', color='#16a085')
        ax.plot(x, cumulative_data, marker='o', linewidth=2, color='#c0392b', 
                label='Cumulative Cash', markersize=8)
        
        ax.set_ylabel('Cash Flow ($K)', fontsize=12, fontweight='bold')
        ax.set_title('Year 1 Quarterly Cash Flow', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(quarters)
        ax.legend(frameon=True, shadow=True)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _create_chart_scenarios(self, filename):
        """Create scenarios comparison chart"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        scenarios_names = ['Conservative', 'Target', 'Upside']
        year1_revenue = [self.scenarios[s]['Year_1']['Revenue']/1000 for s in scenarios_names]
        year1_operating = [self.scenarios[s]['Year_1']['Operating_Income']/1000 for s in scenarios_names]
        
        x = np.arange(len(scenarios_names))
        width = 0.35
        
        ax.bar(x - width/2, year1_revenue, width, label='Revenue', color='#3498db')
        ax.bar(x + width/2, year1_operating, width, label='Operating Income', color='#2ecc71')
        
        ax.set_ylabel('Amount ($K)', fontsize=12, fontweight='bold')
        ax.set_title('Year 1 Scenario Analysis', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(scenarios_names)
        ax.legend(frameon=True, shadow=True)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _create_chart_revenue_mix_pie(self, filename):
        """Create revenue mix pie chart"""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        prod_rev = self.prod_pl['Year_1']['Revenue']
        mkt_rev = self.mkt_pl['Year_1']['Revenue']
        media_rev = self.media_pl['Year_1']['Revenue']
        
        sizes = [prod_rev, mkt_rev, media_rev]
        labels = ['Production', 'Marketing', 'Media']
        colors_pie = ['#3498db', '#2ecc71', '#e74c3c']
        explode = (0.05, 0, 0)
        
        ax.pie(sizes, explode=explode, labels=labels, colors=colors_pie, autopct='%1.1f%%',
               shadow=True, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
        ax.set_title('Year 1 Revenue Mix', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _create_waterfall_chart(self, filename):
        """Create investor waterfall chart"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        years = ['Year 1', 'Year 2', 'Year 3']
        to_investor = [w['To_Investor']/1000 for w in self.waterfall['Waterfall']]
        to_company = [w['To_Company']/1000 for w in self.waterfall['Waterfall']]
        
        x = np.arange(len(years))
        width = 0.35
        
        ax.bar(x - width/2, to_investor, width, label='To Investor', color='#8e44ad')
        ax.bar(x + width/2, to_company, width, label='To Company', color='#27ae60')
        
        ax.set_ylabel('Amount ($K)', fontsize=12, fontweight='bold')
        ax.set_title('Investor Recoupment Waterfall', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(years)
        ax.legend(frameon=True, shadow=True)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add recoupment line
        recoupment_line = self.investment_amount / 1000
        ax.axhline(y=recoupment_line, color='r', linestyle='--', linewidth=2, 
                  label=f'Investment: {self._format_currency(self.investment_amount)}')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
    
    def generate_pdf(self, filename):
        """Generate complete investor memorandum PDF"""
        print(f"\nGenerating PDF: {filename}")
        
        # Create charts directory
        charts_dir = Path('output/charts')
        charts_dir.mkdir(exist_ok=True, parents=True)
        
        # Generate all charts
        print("  Creating charts...")
        chart_files = {}
        chart_files['revenue_by_division'] = charts_dir / f'revenue_division_{self.model.tier_name}.png'
        chart_files['margin_analysis'] = charts_dir / f'margin_analysis_{self.model.tier_name}.png'
        chart_files['cash_flow'] = charts_dir / f'cash_flow_{self.model.tier_name}.png'
        chart_files['scenarios'] = charts_dir / f'scenarios_{self.model.tier_name}.png'
        chart_files['revenue_mix'] = charts_dir / f'revenue_mix_{self.model.tier_name}.png'
        chart_files['waterfall'] = charts_dir / f'waterfall_{self.model.tier_name}.png'
        
        self._create_chart_revenue_by_division(chart_files['revenue_by_division'])
        self._create_chart_margin_analysis(chart_files['margin_analysis'])
        self._create_chart_cash_flow_quarterly(chart_files['cash_flow'])
        self._create_chart_scenarios(chart_files['scenarios'])
        self._create_chart_revenue_mix_pie(chart_files['revenue_mix'])
        self._create_waterfall_chart(chart_files['waterfall'])
        
        # Create PDF
        print("  Building PDF document...")
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
        )
        
        story = []
        
        # Page 1: Cover
        story.extend(self._build_cover_page())
        story.append(PageBreak())
        
        # Page 2: Executive Summary
        story.extend(self._build_executive_summary())
        story.append(PageBreak())
        
        # Page 3: Business Model & Assumptions
        story.extend(self._build_assumptions_page())
        story.append(PageBreak())
        
        # Page 4: Revenue Mix
        story.extend(self._build_revenue_mix_page(chart_files))
        story.append(PageBreak())
        
        # Page 5: Production P&L
        story.extend(self._build_production_pl_page())
        story.append(PageBreak())
        
        # Page 6: Marketing P&L
        story.extend(self._build_marketing_pl_page())
        story.append(PageBreak())
        
        # Page 7: Media P&L
        story.extend(self._build_media_pl_page())
        story.append(PageBreak())
        
        # Page 8: Consolidated P&L
        story.extend(self._build_consolidated_pl_page(chart_files))
        story.append(PageBreak())
        
        # Page 9: Cash Flow Analysis
        story.extend(self._build_cash_flow_page(chart_files))
        story.append(PageBreak())
        
        # Page 10: Scenario Analysis
        story.extend(self._build_scenarios_page(chart_files))
        story.append(PageBreak())
        
        # Page 11: Investor Waterfall
        story.extend(self._build_waterfall_page(chart_files))
        story.append(PageBreak())
        
        # Page 12: Financial Ratios & Metrics
        story.extend(self._build_ratios_page())
        
        # Build PDF
        doc.build(story)
        print(f"  ✓ PDF generated: {filename}")
    
    def _build_cover_page(self):
        """Build cover page"""
        elements = []
        
        elements.append(Spacer(1, 1.5*inch))
        
        title = Paragraph(
            "Abramovich Hybrid Visuals",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        subtitle = Paragraph(
            f"<b>Investor Memorandum</b><br/>{self.model.tier_name} Tier Financial Projections",
            ParagraphStyle(
                'subtitle',
                parent=self.styles['Normal'],
                fontSize=16,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#34495e')
            )
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 0.5*inch))
        
        # Key metrics box
        target_revenue = self._format_currency(self.assumptions['annual_revenue_target'])
        target_margin = self._format_percent(self.consolidated['Year_1']['Operating_Margin'])
        
        metrics_data = [
            ['Target Annual Revenue:', target_revenue],
            ['Year 1 Operating Margin:', target_margin],
            ['Investment Opportunity:', self._format_currency(self.investment_amount)],
            ['Business Model:', 'Production • Marketing • Media'],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ]))
        elements.append(metrics_table)
        
        elements.append(Spacer(1, 1*inch))
        
        date_text = Paragraph(
            f"<i>Generated: {datetime.now().strftime('%B %d, %Y')}</i>",
            ParagraphStyle(
                'date',
                parent=self.styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER,
                textColor=colors.grey
            )
        )
        elements.append(date_text)
        
        confidential = Paragraph(
            "<b>CONFIDENTIAL</b><br/>For Investor Review Only",
            ParagraphStyle(
                'confidential',
                parent=self.styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER,
                textColor=colors.red
            )
        )
        elements.append(confidential)
        
        return elements
    
    def _build_executive_summary(self):
        """Build executive summary page"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.3*inch))
        
        summary_text = f"""
        <b>Business Overview:</b><br/>
        Abramovich Hybrid Visuals operates a diversified media production company with three 
        complementary revenue streams: Premium Production Services, Recurring Marketing Retainers, 
        and Media Distribution/Deployment.
        <br/><br/>
        <b>Financial Highlights ({self.model.tier_name} Tier):</b><br/>
        • Year 1 Revenue Target: {self._format_currency(self.consolidated['Year_1']['Revenue'])}<br/>
        • Year 1 Gross Margin: {self._format_percent(self.consolidated['Year_1']['Gross_Margin'])}<br/>
        • Year 1 Operating Margin: {self._format_percent(self.consolidated['Year_1']['Operating_Margin'])}<br/>
        • Year 3 Revenue Projection: {self._format_currency(self.consolidated['Year_3']['Revenue'])}<br/>
        <br/>
        <b>Revenue Composition:</b><br/>
        • Production: {self._format_percent(self.prod_pl['Year_1']['Revenue'] / self.consolidated['Year_1']['Revenue'])} 
          ({self.assumptions['production_projects_y1']} projects @ avg {self._format_currency(self.assumptions['avg_production_contract'])})<br/>
        • Marketing: {self._format_percent(self.mkt_pl['Year_1']['Revenue'] / self.consolidated['Year_1']['Revenue'])} 
          ({self.assumptions['marketing_clients_y1']} clients @ {self._format_currency(self.assumptions['avg_monthly_marketing_retainer'])}/mo)<br/>
        • Media: {self._format_percent(self.media_pl['Year_1']['Revenue'] / self.consolidated['Year_1']['Revenue'])} 
          ({self.assumptions['media_projects_y1']} deployments)<br/>
        <br/>
        <b>Investment Opportunity:</b><br/>
        Seeking {self._format_currency(self.investment_amount)} to fund operations and growth. 
        Investors receive 100% of operating cash flow until capital is recouped, then 50/50 profit split.
        {f"Projected recoupment: {self.waterfall['Recoupment_Period']}" if self.waterfall['Recoupment_Period'] else "Recoupment expected beyond Year 3"}.
        <br/><br/>
        <b>Key Strengths:</b><br/>
        • Diversified revenue streams reduce client concentration risk<br/>
        • Recurring marketing revenue provides stable cash flow base<br/>
        • High-margin media deployment services improve overall profitability<br/>
        • Scalable model with clear path to {self._format_currency(self.consolidated['Year_3']['Revenue'])}+ by Year 3<br/>
        """
        
        elements.append(Paragraph(summary_text, self.styles['Normal']))
        
        return elements
    
    def _build_assumptions_page(self):
        """Build assumptions page"""
        elements = []
        
        elements.append(Paragraph("Business Model & Financial Assumptions", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Assumptions table
        assumptions_data = [
            ['Assumption', 'Value'],
            ['Target Tier', self.assumptions['tier']],
            ['Annual Revenue Target', self._format_currency(self.assumptions['annual_revenue_target'])],
            ['', ''],
            ['<b>Production Division</b>', ''],
            ['Avg Contract Value', self._format_currency(self.assumptions['avg_production_contract'])],
            ['Year 1 Projects', str(self.assumptions['production_projects_y1'])],
            ['Direct Cost %', self._format_percent(self.assumptions['production_direct_cost_pct'])],
            ['', ''],
            ['<b>Marketing Division</b>', ''],
            ['Avg Monthly Retainer', self._format_currency(self.assumptions['avg_monthly_marketing_retainer'])],
            ['Year 1 Clients', str(self.assumptions['marketing_clients_y1'])],
            ['', ''],
            ['<b>Media Division</b>', ''],
            ['Avg Deployment Fee', self._format_currency(self.assumptions['avg_media_deployment_fee'])],
            ['Year 1 Projects', str(self.assumptions['media_projects_y1'])],
            ['', ''],
            ['<b>Operating Costs</b>', ''],
            ['Annual Payroll', self._format_currency(self.assumptions['annual_payroll'])],
            ['Annual Overhead', self._format_currency(self.assumptions['annual_overhead'])],
            ['', ''],
            ['<b>Growth Rates</b>', ''],
            ['Year 2 Growth', self._format_percent(self.assumptions['year_2_growth'])],
            ['Year 3 Growth', self._format_percent(self.assumptions['year_3_growth'])],
        ]
        
        table = Table(assumptions_data, colWidths=[4*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_revenue_mix_page(self, chart_files):
        """Build revenue mix visualization page"""
        elements = []
        
        elements.append(Paragraph("Revenue Mix Analysis", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add pie chart
        if chart_files['revenue_mix'].exists():
            img = Image(str(chart_files['revenue_mix']), width=5*inch, height=5*inch)
            elements.append(img)
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Revenue breakdown table
        rev_data = [
            ['Division', 'Year 1', 'Year 2', 'Year 3', '3-Yr Total'],
            ['Production', 
             self._format_currency(self.prod_pl['Year_1']['Revenue']),
             self._format_currency(self.prod_pl['Year_2']['Revenue']),
             self._format_currency(self.prod_pl['Year_3']['Revenue']),
             self._format_currency(sum(self.prod_pl[f'Year_{i}']['Revenue'] for i in [1,2,3]))],
            ['Marketing',
             self._format_currency(self.mkt_pl['Year_1']['Revenue']),
             self._format_currency(self.mkt_pl['Year_2']['Revenue']),
             self._format_currency(self.mkt_pl['Year_3']['Revenue']),
             self._format_currency(sum(self.mkt_pl[f'Year_{i}']['Revenue'] for i in [1,2,3]))],
            ['Media',
             self._format_currency(self.media_pl['Year_1']['Revenue']),
             self._format_currency(self.media_pl['Year_2']['Revenue']),
             self._format_currency(self.media_pl['Year_3']['Revenue']),
             self._format_currency(sum(self.media_pl[f'Year_{i}']['Revenue'] for i in [1,2,3]))],
        ]
        
        table = Table(rev_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_production_pl_page(self):
        """Build production P&L page"""
        elements = []
        
        elements.append(Paragraph("Production Division P&L", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        pl_data = [
            ['', 'Year 1', 'Year 2', 'Year 3'],
            ['Revenue', 
             self._format_currency(self.prod_pl['Year_1']['Revenue']),
             self._format_currency(self.prod_pl['Year_2']['Revenue']),
             self._format_currency(self.prod_pl['Year_3']['Revenue'])],
            ['COGS',
             self._format_currency(self.prod_pl['Year_1']['COGS']),
             self._format_currency(self.prod_pl['Year_2']['COGS']),
             self._format_currency(self.prod_pl['Year_3']['COGS'])],
            ['Gross Profit',
             self._format_currency(self.prod_pl['Year_1']['Gross_Profit']),
             self._format_currency(self.prod_pl['Year_2']['Gross_Profit']),
             self._format_currency(self.prod_pl['Year_3']['Gross_Profit'])],
            ['Gross Margin',
             self._format_percent(self.prod_pl['Year_1']['Gross_Margin']),
             self._format_percent(self.prod_pl['Year_2']['Gross_Margin']),
             self._format_percent(self.prod_pl['Year_3']['Gross_Margin'])],
        ]
        
        table = Table(pl_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
            ('LINEABOVE', (0, 3), (-1, 3), 2, colors.black),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_marketing_pl_page(self):
        """Build marketing P&L page"""
        elements = []
        
        elements.append(Paragraph("Marketing Division P&L", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        pl_data = [
            ['', 'Year 1', 'Year 2', 'Year 3'],
            ['Revenue', 
             self._format_currency(self.mkt_pl['Year_1']['Revenue']),
             self._format_currency(self.mkt_pl['Year_2']['Revenue']),
             self._format_currency(self.mkt_pl['Year_3']['Revenue'])],
            ['COGS',
             self._format_currency(self.mkt_pl['Year_1']['COGS']),
             self._format_currency(self.mkt_pl['Year_2']['COGS']),
             self._format_currency(self.mkt_pl['Year_3']['COGS'])],
            ['Gross Profit',
             self._format_currency(self.mkt_pl['Year_1']['Gross_Profit']),
             self._format_currency(self.mkt_pl['Year_2']['Gross_Profit']),
             self._format_currency(self.mkt_pl['Year_3']['Gross_Profit'])],
            ['Gross Margin',
             self._format_percent(self.mkt_pl['Year_1']['Gross_Margin']),
             self._format_percent(self.mkt_pl['Year_2']['Gross_Margin']),
             self._format_percent(self.mkt_pl['Year_3']['Gross_Margin'])],
        ]
        
        table = Table(pl_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
            ('LINEABOVE', (0, 3), (-1, 3), 2, colors.black),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_media_pl_page(self):
        """Build media P&L page"""
        elements = []
        
        elements.append(Paragraph("Media/Distribution Division P&L", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        pl_data = [
            ['', 'Year 1', 'Year 2', 'Year 3'],
            ['Revenue', 
             self._format_currency(self.media_pl['Year_1']['Revenue']),
             self._format_currency(self.media_pl['Year_2']['Revenue']),
             self._format_currency(self.media_pl['Year_3']['Revenue'])],
            ['COGS',
             self._format_currency(self.media_pl['Year_1']['COGS']),
             self._format_currency(self.media_pl['Year_2']['COGS']),
             self._format_currency(self.media_pl['Year_3']['COGS'])],
            ['Gross Profit',
             self._format_currency(self.media_pl['Year_1']['Gross_Profit']),
             self._format_currency(self.media_pl['Year_2']['Gross_Profit']),
             self._format_currency(self.media_pl['Year_3']['Gross_Profit'])],
            ['Gross Margin',
             self._format_percent(self.media_pl['Year_1']['Gross_Margin']),
             self._format_percent(self.media_pl['Year_2']['Gross_Margin']),
             self._format_percent(self.media_pl['Year_3']['Gross_Margin'])],
        ]
        
        table = Table(pl_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
            ('LINEABOVE', (0, 3), (-1, 3), 2, colors.black),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_consolidated_pl_page(self, chart_files):
        """Build consolidated P&L page with charts"""
        elements = []
        
        elements.append(Paragraph("Consolidated P&L", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Full P&L table
        pl_data = [
            ['', 'Year 1', 'Year 2', 'Year 3'],
            ['Revenue', 
             self._format_currency(self.consolidated['Year_1']['Revenue']),
             self._format_currency(self.consolidated['Year_2']['Revenue']),
             self._format_currency(self.consolidated['Year_3']['Revenue'])],
            ['COGS',
             self._format_currency(self.consolidated['Year_1']['COGS']),
             self._format_currency(self.consolidated['Year_2']['COGS']),
             self._format_currency(self.consolidated['Year_3']['COGS'])],
            ['Gross Profit',
             self._format_currency(self.consolidated['Year_1']['Gross_Profit']),
             self._format_currency(self.consolidated['Year_2']['Gross_Profit']),
             self._format_currency(self.consolidated['Year_3']['Gross_Profit'])],
            ['Gross Margin',
             self._format_percent(self.consolidated['Year_1']['Gross_Margin']),
             self._format_percent(self.consolidated['Year_2']['Gross_Margin']),
             self._format_percent(self.consolidated['Year_3']['Gross_Margin'])],
            ['', '', '', ''],
            ['Payroll',
             self._format_currency(self.consolidated['Year_1']['Payroll']),
             self._format_currency(self.consolidated['Year_2']['Payroll']),
             self._format_currency(self.consolidated['Year_3']['Payroll'])],
            ['Overhead',
             self._format_currency(self.consolidated['Year_1']['Overhead']),
             self._format_currency(self.consolidated['Year_2']['Overhead']),
             self._format_currency(self.consolidated['Year_3']['Overhead'])],
            ['Operating Expenses',
             self._format_currency(self.consolidated['Year_1']['Operating_Expenses']),
             self._format_currency(self.consolidated['Year_2']['Operating_Expenses']),
             self._format_currency(self.consolidated['Year_3']['Operating_Expenses'])],
            ['', '', '', ''],
            ['Operating Income',
             self._format_currency(self.consolidated['Year_1']['Operating_Income']),
             self._format_currency(self.consolidated['Year_2']['Operating_Income']),
             self._format_currency(self.consolidated['Year_3']['Operating_Income'])],
            ['Operating Margin',
             self._format_percent(self.consolidated['Year_1']['Operating_Margin']),
             self._format_percent(self.consolidated['Year_2']['Operating_Margin']),
             self._format_percent(self.consolidated['Year_3']['Operating_Margin'])],
            ['', '', '', ''],
            ['EBITDA',
             self._format_currency(self.consolidated['Year_1']['EBITDA']),
             self._format_currency(self.consolidated['Year_2']['EBITDA']),
             self._format_currency(self.consolidated['Year_3']['EBITDA'])],
            ['EBITDA Margin',
             self._format_percent(self.consolidated['Year_1']['EBITDA_Margin']),
             self._format_percent(self.consolidated['Year_2']['EBITDA_Margin']),
             self._format_percent(self.consolidated['Year_3']['EBITDA_Margin'])],
        ]
        
        table = Table(pl_data, colWidths=[2.2*inch, 1.4*inch, 1.4*inch, 1.4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
            ('LINEABOVE', (0, 3), (-1, 3), 2, colors.black),
            ('LINEABOVE', (0, 10), (-1, 10), 2, colors.black),
            ('LINEABOVE', (0, 13), (-1, 13), 2, colors.black),
            ('FONTNAME', (0, 10), (-1, 10), 'Helvetica-Bold'),
            ('FONTNAME', (0, 13), (-1, 13), 'Helvetica-Bold'),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_cash_flow_page(self, chart_files):
        """Build cash flow analysis page"""
        elements = []
        
        elements.append(Paragraph("Cash Flow Analysis", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add chart
        if chart_files['cash_flow'].exists():
            img = Image(str(chart_files['cash_flow']), width=6*inch, height=3.6*inch)
            elements.append(img)
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Quarterly breakdown table
        q_data = [
            ['Quarter', 'Revenue', 'Operating CF', 'Cumulative CF'],
        ]
        
        for q in ['Q1', 'Q2', 'Q3', 'Q4']:
            q_data.append([
                q,
                self._format_currency(self.cash_flow['Year_1_Quarterly'][q]['Revenue']),
                self._format_currency(self.cash_flow['Year_1_Quarterly'][q]['Operating_Cash_Flow']),
                self._format_currency(self.cash_flow['Year_1_Quarterly'][q]['Cumulative_Cash']),
            ])
        
        table = Table(q_data, colWidths=[1.2*inch, 1.6*inch, 1.6*inch, 1.6*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a085')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ]))
        
        elements.append(table)
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Annual summary
        annual_data = [
            ['Year', 'Operating Cash Flow'],
            ['Year 1', self._format_currency(self.cash_flow['Annual']['Year_1'])],
            ['Year 2', self._format_currency(self.cash_flow['Annual']['Year_2'])],
            ['Year 3', self._format_currency(self.cash_flow['Annual']['Year_3'])],
        ]
        
        table2 = Table(annual_data, colWidths=[2*inch, 2*inch])
        table2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a085')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ]))
        
        elements.append(table2)
        
        return elements
    
    def _build_scenarios_page(self, chart_files):
        """Build scenario analysis page"""
        elements = []
        
        elements.append(Paragraph("Scenario Analysis", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add chart
        if chart_files['scenarios'].exists():
            img = Image(str(chart_files['scenarios']), width=6*inch, height=3.6*inch)
            elements.append(img)
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Scenarios comparison table
        scenarios_data = [
            ['Metric', 'Conservative', 'Target', 'Upside'],
            ['Year 1 Revenue',
             self._format_currency(self.scenarios['Conservative']['Year_1']['Revenue']),
             self._format_currency(self.scenarios['Target']['Year_1']['Revenue']),
             self._format_currency(self.scenarios['Upside']['Year_1']['Revenue'])],
            ['Year 1 Operating Income',
             self._format_currency(self.scenarios['Conservative']['Year_1']['Operating_Income']),
             self._format_currency(self.scenarios['Target']['Year_1']['Operating_Income']),
             self._format_currency(self.scenarios['Upside']['Year_1']['Operating_Income'])],
            ['Year 1 Operating Margin',
             self._format_percent(self.scenarios['Conservative']['Year_1']['Operating_Margin']),
             self._format_percent(self.scenarios['Target']['Year_1']['Operating_Margin']),
             self._format_percent(self.scenarios['Upside']['Year_1']['Operating_Margin'])],
            ['', '', '', ''],
            ['Year 3 Revenue',
             self._format_currency(self.scenarios['Conservative']['Year_3']['Revenue']),
             self._format_currency(self.scenarios['Target']['Year_3']['Revenue']),
             self._format_currency(self.scenarios['Upside']['Year_3']['Revenue'])],
            ['Year 3 Operating Income',
             self._format_currency(self.scenarios['Conservative']['Year_3']['Operating_Income']),
             self._format_currency(self.scenarios['Target']['Year_3']['Operating_Income']),
             self._format_currency(self.scenarios['Upside']['Year_3']['Operating_Income'])],
        ]
        
        table = Table(scenarios_data, colWidths=[2.2*inch, 1.4*inch, 1.4*inch, 1.4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_waterfall_page(self, chart_files):
        """Build investor waterfall page"""
        elements = []
        
        elements.append(Paragraph("Investor Recoupment Waterfall", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Investment terms
        terms_text = f"""
        <b>Investment Terms:</b><br/>
        Investment Amount: {self._format_currency(self.investment_amount)}<br/>
        Structure: 100% to investor until recoupment, then 50/50 profit split<br/>
        Recoupment Period: {self.waterfall['Recoupment_Period'] if self.waterfall['Recoupment_Period'] else 'Beyond Year 3'}<br/>
        """
        elements.append(Paragraph(terms_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add chart
        if chart_files['waterfall'].exists():
            img = Image(str(chart_files['waterfall']), width=6*inch, height=3.6*inch)
            elements.append(img)
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Waterfall table
        waterfall_data = [
            ['Year', 'Operating Income', 'To Investor', 'To Company', 'Cumulative to Investor', 'Status'],
        ]
        
        for w in self.waterfall['Waterfall']:
            waterfall_data.append([
                w['Year'],
                self._format_currency(w['Operating_Income']),
                self._format_currency(w['To_Investor']),
                self._format_currency(w['To_Company']),
                self._format_currency(w['Cumulative_To_Investor']),
                'Recouped' if w['Recouped'] else 'Recouping',
            ])
        
        table = Table(waterfall_data, colWidths=[0.8*inch, 1.3*inch, 1.2*inch, 1.2*inch, 1.4*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8e44ad')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _build_ratios_page(self):
        """Build financial ratios and metrics page"""
        elements = []
        
        elements.append(Paragraph("Financial Ratios & Key Metrics", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Calculate key ratios
        revenue_y1 = self.consolidated['Year_1']['Revenue']
        revenue_y3 = self.consolidated['Year_3']['Revenue']
        cagr = ((revenue_y3 / revenue_y1) ** (1/2) - 1) if revenue_y1 > 0 else 0
        
        opex_as_pct_revenue = self.consolidated['Year_1']['Operating_Expenses'] / revenue_y1 if revenue_y1 > 0 else 0
        
        break_even_revenue = self.consolidated['Year_1']['Operating_Expenses'] / (1 - (self.consolidated['Year_1']['COGS'] / revenue_y1)) if revenue_y1 > 0 else 0
        
        # Ratios table
        ratios_data = [
            ['Metric', 'Year 1', 'Year 2', 'Year 3'],
            ['', '', '', ''],
            ['<b>Profitability</b>', '', '', ''],
            ['Gross Margin',
             self._format_percent(self.consolidated['Year_1']['Gross_Margin']),
             self._format_percent(self.consolidated['Year_2']['Gross_Margin']),
             self._format_percent(self.consolidated['Year_3']['Gross_Margin'])],
            ['Operating Margin',
             self._format_percent(self.consolidated['Year_1']['Operating_Margin']),
             self._format_percent(self.consolidated['Year_2']['Operating_Margin']),
             self._format_percent(self.consolidated['Year_3']['Operating_Margin'])],
            ['EBITDA Margin',
             self._format_percent(self.consolidated['Year_1']['EBITDA_Margin']),
             self._format_percent(self.consolidated['Year_2']['EBITDA_Margin']),
             self._format_percent(self.consolidated['Year_3']['EBITDA_Margin'])],
            ['', '', '', ''],
            ['<b>Growth</b>', '', '', ''],
            ['Revenue Growth', 'Baseline',
             self._format_percent(self.assumptions['year_2_growth']),
             self._format_percent(self.assumptions['year_3_growth'])],
            ['3-Year CAGR', self._format_percent(cagr), '', ''],
            ['', '', '', ''],
            ['<b>Efficiency</b>', '', '', ''],
            ['OpEx as % of Revenue', self._format_percent(opex_as_pct_revenue), '', ''],
            ['Break-Even Revenue', self._format_currency(break_even_revenue), '', ''],
        ]
        
        table = Table(ratios_data, colWidths=[2.5*inch, 1.3*inch, 1.3*inch, 1.3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')]),
        ]))
        
        elements.append(table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Key insights
        insights_text = f"""
        <b>Key Insights:</b><br/>
        • <b>Revenue Growth:</b> 3-year CAGR of {self._format_percent(cagr)} demonstrates strong growth trajectory<br/>
        • <b>Profitability:</b> {self._format_percent(self.consolidated['Year_1']['Operating_Margin'])} operating margin in Year 1, 
          improving to {self._format_percent(self.consolidated['Year_3']['Operating_Margin'])} by Year 3<br/>
        • <b>Break-Even:</b> Company breaks even at {self._format_currency(break_even_revenue)} annual revenue<br/>
        • <b>Capital Efficiency:</b> Operating expenses at {self._format_percent(opex_as_pct_revenue)} of revenue enables profitable growth<br/>
        • <b>Cash Generation:</b> Positive operating cash flow from Year 1 with cumulative 3-year operating income of 
          {self._format_currency(sum(self.consolidated[f'Year_{i}']['Operating_Income'] for i in [1,2,3]))}<br/>
        """
        
        elements.append(Paragraph(insights_text, self.styles['Normal']))
        
        return elements


def generate_all_pdfs():
    """Generate PDFs for all tiers"""
    from financial_model import generate_all_tiers
    
    # Generate models
    models = generate_all_tiers()
    
    print("\n" + "="*60)
    print("Generating Investor Memorandum PDFs")
    print("="*60)
    
    output_dir = Path('output')
    
    for tier_name, model in models.items():
        print(f"\n{tier_name} Tier:")
        
        # Determine investment amount (50% of annual target)
        investment = int(model.annual_revenue_target * 0.5)
        
        memo = InvestorMemorandum(model, investment)
        pdf_path = output_dir / f'Investor_Memorandum_{tier_name}.pdf'
        memo.generate_pdf(str(pdf_path))
    
    print("\n" + "="*60)
    print("✓ All PDFs generated successfully!")
    print(f"Output directory: {output_dir.absolute()}")
    print("="*60)


if __name__ == '__main__':
    generate_all_pdfs()
