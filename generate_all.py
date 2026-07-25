#!/usr/bin/env python3
"""
Master script to generate all financial projections and investor memorandums
"""

import sys
from pathlib import Path
from financial_model import generate_all_tiers
from pdf_generator import generate_all_pdfs

def main():
    """Generate all financial models and PDFs"""
    print("="*70)
    print("ABRAMOVICH HYBRID VISUALS")
    print("Financial Projections & Investor Memorandum Generator")
    print("="*70)
    print()
    print("Generating comprehensive financial models for:")
    print("  • $100K Tier (Startup)")
    print("  • $500K Tier (Growth)")
    print("  • $1M Tier (Scale)")
    print("  • $2M Tier (Enterprise)")
    print()
    print("="*70)
    
    # Create output directory
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Step 1: Generate financial models
        print("\n[STEP 1/2] Generating Financial Models...")
        print("-" * 70)
        models = generate_all_tiers()
        
        # Step 2: Generate PDFs
        print("\n[STEP 2/2] Generating Investor Memorandum PDFs...")
        print("-" * 70)
        generate_all_pdfs()
        
        # Success summary
        print("\n" + "="*70)
        print("✓ GENERATION COMPLETE")
        print("="*70)
        print("\nGenerated Files:")
        print("\n📊 Financial Models (JSON & Excel):")
        for tier in ['$100K', '$500K', '$1M', '$2M']:
            print(f"  • output/financial_model_{tier}.json")
            print(f"  • output/financial_model_{tier}.xlsx")
        
        print("\n📄 Investor Memorandums (PDF):")
        for tier in ['$100K', '$500K', '$1M', '$2M']:
            print(f"  • output/Investor_Memorandum_{tier}.pdf")
        
        print("\n📈 Charts & Graphics:")
        print(f"  • output/charts/*.png ({len(list((output_dir / 'charts').glob('*.png')))} files)")
        
        print("\n" + "="*70)
        print(f"Output Location: {output_dir.absolute()}")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
