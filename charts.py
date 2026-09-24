import plotly.graph_objects as go
import plotly.express as px


PURPLE_COLORS = [
    "#7C3AED", "#6D28D9", "#5B21B6", "#4C1D95",
    "#8B5CF6", "#A78BFA", "#C4B5FD", "#DDD6FE"
]


def language_pie_chart(languages):
    """Pie chart of top programming languages used across repos."""
    if not languages:
        return None

    labels = list(languages.keys())[:8]
    values = list(languages.values())[:8]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=PURPLE_COLORS),
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Repos: %{value}<br>Share: %{percent}<extra></extra>"
    )])

    fig.update_layout(
        title=dict(text="Top Languages", font=dict(size=18, color="#A78BFA")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0"),
        showlegend=True,
        legend=dict(font=dict(color="#E2E8F0")),
        margin=dict(t=50, b=20, l=20, r=20)
    )

    return fig


def top_repos_bar_chart(repos):
    """Horizontal bar chart of top repos by star count."""
    if not repos:
        return None

    names = [r.get("name", "unknown")[:25] for r in repos]
    stars = [r.get("stargazers_count", 0) for r in repos]

    fig = go.Figure(go.Bar(
        x=stars,
        y=names,
        orientation="h",
        marker=dict(
            color=stars,
            colorscale=[[0, "#4C1D95"], [0.5, "#7C3AED"], [1, "#A78BFA"]],
            line=dict(color="#6D28D9", width=1)
        ),
        hovertemplate="<b>%{y}</b><br>⭐ Stars: %{x}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(text="Top Repos by Stars", font=dict(size=18, color="#A78BFA")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0"),
        xaxis=dict(
            title="Stars",
            gridcolor="#2D2D3D",
            color="#E2E8F0"
        ),
        yaxis=dict(
            autorange="reversed",
            color="#E2E8F0"
        ),
        margin=dict(t=50, b=40, l=20, r=20)
    )

    return fig


def score_gauge(score):
    """Gauge chart showing the profile score out of 100."""
    if score >= 75:
        color = "#22C55E"
    elif score >= 50:
        color = "#F59E0B"
    elif score >= 25:
        color = "#F97316"
    else:
        color = "#EF4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Profile Score", "font": {"size": 20, "color": "#A78BFA"}},
        number={"suffix": "/100", "font": {"size": 36, "color": color}},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "#4B5563",
                "tickfont": {"color": "#9CA3AF"}
            },
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "#1F2937",
            "borderwidth": 2,
            "bordercolor": "#374151",
            "steps": [
                {"range": [0, 25], "color": "#1F1130"},
                {"range": [25, 50], "color": "#2D1A4A"},
                {"range": [50, 75], "color": "#3B2063"},
                {"range": [75, 100], "color": "#4C2A7A"}
            ],
            "threshold": {
                "line": {"color": "#F8FAFC", "width": 3},
                "thickness": 0.75,
                "value": score
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0"),
        height=280,
        margin=dict(t=40, b=10, l=30, r=30)
    )

    return fig


def score_breakdown_bar(breakdown):
    """Horizontal bar chart showing score breakdown by category."""
    categories = list(breakdown.keys())
    points = list(breakdown.values())

    colors = ["#7C3AED" if p > 0 else "#374151" for p in points]

    fig = go.Figure(go.Bar(
        x=points,
        y=categories,
        orientation="h",
        marker=dict(color=colors),
        hovertemplate="<b>%{y}</b><br>Points: %{x}<extra></extra>",
        text=points,
        textposition="outside",
        textfont=dict(color="#E2E8F0", size=12)
    ))

    fig.update_layout(
        title=dict(text="Score Breakdown", font=dict(size=18, color="#A78BFA")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0"),
        xaxis=dict(
            range=[0, 20],
            gridcolor="#2D2D3D",
            color="#E2E8F0"
        ),
        yaxis=dict(color="#E2E8F0"),
        margin=dict(t=50, b=20, l=20, r=60),
        height=380
    )

    return fig
