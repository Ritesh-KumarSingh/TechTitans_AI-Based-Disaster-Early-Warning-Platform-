"""
Plotly Charts - Risk Gauge and Probability Bar Chart
"""

import plotly.graph_objects as go


def create_risk_gauge(probability, color):
    """Create a modern risk gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        number={'suffix': '%', 'font': {'size': 40, 'color': 'white', 'family': 'Poppins'}},
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 0,
                'tickfont': {'size': 1}
            },
            'bar': {'color': color, 'thickness': 0.8},
            'bgcolor': 'rgba(255,255,255,0.05)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 25], 'color': 'rgba(16, 185, 129, 0.15)'},
                {'range': [25, 50], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [50, 75], 'color': 'rgba(249, 115, 22, 0.15)'},
                {'range': [75, 100], 'color': 'rgba(239, 68, 68, 0.15)'}
            ],
            'threshold': {
                'line': {'color': color, 'width': 3},
                'thickness': 0.8,
                'value': probability * 100
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Poppins'),
        height=200,
        margin=dict(l=20, r=20, t=30, b=10)
    )

    return fig


def create_prob_chart(all_probs):
    """Create horizontal bar chart for risk probabilities"""
    labels = list(all_probs.keys())
    values = [v * 100 for v in all_probs.values()]
    colors = ['#10b981', '#f59e0b', '#f97316', '#ef4444']

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(width=0),
            cornerradius=8
        ),
        text=[f'{v:.1f}%' for v in values],
        textposition='auto',
        textfont=dict(color='white', size=13, family='Poppins')
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(255,255,255,0.7)', family='Poppins'),
        height=200,
        margin=dict(l=0, r=20, t=10, b=10),
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[0, 105]
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=13)
        ),
        bargap=0.3
    )

    return fig
