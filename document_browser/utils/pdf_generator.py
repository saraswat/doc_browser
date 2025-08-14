"""Utility to generate sample PDF documents."""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from pathlib import Path
import datetime


def create_financial_summary_pdf():
    """Create Financial Summary PDF document."""
    output_path = Path(__file__).parent.parent / "documents" / "content" / "Financial Summary_2024-01-30.pdf"
    
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("Financial Summary Q4 2023", title_style))
    story.append(Spacer(1, 20))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    story.append(Paragraph(
        "This financial summary presents the key performance indicators and financial metrics for Q4 2023, "
        "demonstrating strong revenue growth and operational efficiency improvements across all business units.",
        styles['Normal']
    ))
    story.append(Spacer(1, 12))
    
    # Revenue Table
    story.append(Paragraph("Revenue Breakdown", styles['Heading2']))
    revenue_data = [
        ['Business Unit', 'Q4 2023', 'Q3 2023', 'Growth'],
        ['Enterprise Solutions', '$2.4M', '$2.1M', '+14.3%'],
        ['Cloud Services', '$1.8M', '$1.5M', '+20.0%'],
        ['Professional Services', '$0.9M', '$0.8M', '+12.5%'],
        ['Total Revenue', '$5.1M', '$4.4M', '+15.9%']
    ]
    
    revenue_table = Table(revenue_data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1*inch])
    revenue_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgreen),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(revenue_table)
    story.append(Spacer(1, 20))
    
    # Key Metrics
    story.append(Paragraph("Key Performance Indicators", styles['Heading2']))
    kpi_data = [
        ['Metric', 'Q4 2023', 'Target', 'Status'],
        ['Customer Acquisition Cost', '$125', '$150', 'Above Target'],
        ['Customer Lifetime Value', '$2,400', '$2,000', 'Above Target'],
        ['Monthly Recurring Revenue', '$1.2M', '$1.0M', 'Above Target'],
        ['Gross Margin', '68%', '65%', 'Above Target'],
        ['Net Profit Margin', '22%', '20%', 'Above Target']
    ]
    
    kpi_table = Table(kpi_data, colWidths=[2.2*inch, 1.2*inch, 1*inch, 1.2*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(kpi_table)
    story.append(Spacer(1, 20))
    
    # Projections
    story.append(Paragraph("Q1 2024 Projections", styles['Heading2']))
    story.append(Paragraph(
        "Based on current market trends and pipeline analysis, we project continued growth in Q1 2024:",
        styles['Normal']
    ))
    story.append(Spacer(1, 6))
    
    projections = [
        "• Revenue growth of 18-22% compared to Q1 2023",
        "• Enterprise Solutions expected to reach $2.8M",
        "• Cloud Services projected at $2.2M (+22% QoQ)",
        "• New customer acquisition target: 150 new accounts",
        "• Expansion of Professional Services team by 25%"
    ]
    
    for proj in projections:
        story.append(Paragraph(proj, styles['Normal']))
    
    story.append(Spacer(1, 20))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=1
    )
    story.append(Paragraph(f"Generated on {datetime.date.today()}", footer_style))
    
    doc.build(story)
    print(f"Created Financial Summary PDF: {output_path}")


def create_product_roadmap_pdf():
    """Create Product Roadmap PDF document."""
    output_path = Path(__file__).parent.parent / "documents" / "content" / "Product Roadmap_2024-02-05.pdf"
    
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.darkgreen,
        alignment=1
    )
    story.append(Paragraph("Product Development Roadmap 2024", title_style))
    story.append(Spacer(1, 20))
    
    # Overview
    story.append(Paragraph("Strategic Overview", styles['Heading2']))
    story.append(Paragraph(
        "Our 2024 product roadmap focuses on AI integration, enhanced user experience, and scalability improvements. "
        "This roadmap aligns with our strategic objectives to capture 25% market share and achieve $15M ARR by Q4 2024.",
        styles['Normal']
    ))
    story.append(Spacer(1, 12))
    
    # Q1 2024 Deliverables
    story.append(Paragraph("Q1 2024 - Foundation Phase", styles['Heading2']))
    q1_data = [
        ['Feature', 'Priority', 'Team', 'Status'],
        ['AI-Powered Analytics Dashboard', 'High', 'Data Team', 'In Progress'],
        ['Mobile App MVP', 'High', 'Mobile Team', 'Planning'],
        ['API v2.0 Release', 'Medium', 'Backend Team', 'Development'],
        ['Enhanced Security Framework', 'High', 'Security Team', 'Testing'],
        ['User Onboarding Redesign', 'Medium', 'UX Team', 'Design Phase']
    ]
    
    q1_table = Table(q1_data, colWidths=[2.5*inch, 1*inch, 1.2*inch, 1*inch])
    q1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(q1_table)
    story.append(Spacer(1, 15))
    
    # Q2-Q4 High-Level Milestones
    story.append(Paragraph("Q2-Q4 2024 - Major Milestones", styles['Heading2']))
    
    milestones = [
        ("Q2 2024", [
            "Launch mobile application (iOS/Android)",
            "Implement machine learning recommendation engine",
            "Beta release of collaborative workspace features",
            "Integration with 5 major enterprise tools"
        ]),
        ("Q3 2024", [
            "Advanced reporting and analytics suite",
            "Multi-language support (Spanish, French, German)",
            "Enterprise SSO and advanced permissions",
            "Public API marketplace launch"
        ]),
        ("Q4 2024", [
            "AI-driven predictive analytics",
            "Advanced workflow automation",
            "White-label solution for enterprise clients",
            "International market expansion"
        ])
    ]
    
    for quarter, items in milestones:
        story.append(Paragraph(quarter, styles['Heading3']))
        for item in items:
            story.append(Paragraph(f"• {item}", styles['Normal']))
        story.append(Spacer(1, 10))
    
    # Technology Stack Evolution
    story.append(Paragraph("Technology Stack Evolution", styles['Heading2']))
    tech_data = [
        ['Component', 'Current', '2024 Target', 'Rationale'],
        ['Frontend', 'React 17', 'React 18 + Next.js', 'Performance & SEO'],
        ['Backend', 'Node.js + Express', 'Node.js + FastAPI', 'Better async support'],
        ['Database', 'PostgreSQL', 'PostgreSQL + Redis', 'Caching & speed'],
        ['AI/ML', 'Python scripts', 'TensorFlow + MLOps', 'Production ML pipeline'],
        ['Infrastructure', 'AWS EC2', 'AWS EKS + Serverless', 'Auto-scaling']
    ]
    
    tech_table = Table(tech_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 2*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(tech_table)
    story.append(Spacer(1, 20))
    
    # Success Metrics
    story.append(Paragraph("Success Metrics & KPIs", styles['Heading2']))
    story.append(Paragraph(
        "Our roadmap success will be measured against these key performance indicators:",
        styles['Normal']
    ))
    story.append(Spacer(1, 6))
    
    metrics = [
        "• User engagement: 40% increase in daily active users",
        "• Feature adoption: 80% of users using new AI features within 30 days",
        "• Performance: 50% improvement in page load times",
        "• Customer satisfaction: NPS score above 70",
        "• Revenue impact: 35% increase in average revenue per user"
    ]
    
    for metric in metrics:
        story.append(Paragraph(metric, styles['Normal']))
    
    # Footer
    story.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=1
    )
    story.append(Paragraph(f"Product Roadmap 2024 • Generated {datetime.date.today()}", footer_style))
    
    doc.build(story)
    print(f"Created Product Roadmap PDF: {output_path}")


if __name__ == "__main__":
    create_financial_summary_pdf()
    create_product_roadmap_pdf()
    print("Sample PDF documents created successfully!")