import plotly.graph_objects as go
import plotly.express as px

def create_hourly_chart(hourly_data):
    if not hourly_data:
        return ""
    
    times = [h['time'] for h in hourly_data]
    temps = [h['temp'] for h in hourly_data]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times, y=temps,
        mode='lines+markers',
        name='Nhiệt độ',
        line=dict(color='#4facfe', width=3),
        fill='tozeroy',
        fillcolor='rgba(79, 172, 254, 0.2)',
        marker=dict(size=8, color='#4facfe')
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=200,
        showlegend=False,
        xaxis=dict(showgrid=False, tickfont=dict(color='rgba(255,255,255,0.6)')),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='rgba(255,255,255,0.6)'))
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn', config={'displayModeBar': False}).replace('\u2212', '-')

def create_temp_trend_chart(daily_data):
    if not daily_data:
        return ""
    
    labels = [d['day_name'][:3] for d in daily_data[:7]]
    temps = [round((d['temp_max'] + d['temp_min']) / 2) for d in daily_data[:7]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels, y=temps,
        mode='lines',
        line=dict(color='#4facfe', width=2, shape='spline'),
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=100,
        showlegend=False,
        xaxis=dict(showgrid=False, tickfont=dict(color='rgba(255,255,255,0.4)', size=10)),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=False, config={'displayModeBar': False}).replace('\u2212', '-')

def create_precip_chart(daily_data):
    if not daily_data:
        return ""
    
    labels = [d['date'][5:] for d in daily_data[:7]]
    pops = [d['pop_max'] for d in daily_data[:7]]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels, y=pops,
        marker_color='rgba(79, 172, 254, 0.5)',
        marker_line_width=0,
        marker_pattern_shape=""
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=100,
        showlegend=False,
        xaxis=dict(showgrid=False, tickfont=dict(color='rgba(255,255,255,0.4)', size=10)),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=False, config={'displayModeBar': False}).replace('\u2212', '-')

def create_detailed_forecast_chart(daily_data):
    if not daily_data:
        return ""
    
    slice_data = daily_data[:7]
    labels = [d['day_name'] for d in slice_data]
    max_temps = [round(d['temp_max']) for d in slice_data]
    min_temps = [round(d['temp_min']) for d in slice_data]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels, y=max_temps,
        mode='lines+markers',
        name='Cao nhất',
        line=dict(color='#4facfe', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=labels, y=min_temps,
        mode='lines+markers',
        name='Thấp nhất',
        line=dict(color='#f87171', width=3)
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0),
        height=400,
        legend=dict(font=dict(color='#fff'), orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(showgrid=False, tickfont=dict(color='rgba(255,255,255,0.6)')),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='rgba(255,255,255,0.6)'))
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=False, config={'displayModeBar': False}).replace('\u2212', '-')

def create_analysis_charts(processed_data):
    if not processed_data:
        return {}
    
    daily = processed_data.get('daily', [])
    hourly = processed_data.get('hourly', [])
    aqi = processed_data.get('aqi')
    
    charts = {}
    
    # 1. Monthly Compare (using daily data as proxy)
    if daily:
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=[d['date'][5:] for d in daily[:7]],
            y=[round(d['temp_min']) for d in daily[:7]],
            name='Thấp nhất',
            marker_color='rgba(255,255,255,0.2)'
        ))
        fig1.add_trace(go.Bar(
            x=[d['date'][5:] for d in daily[:7]],
            y=[round(d['temp_max']) for d in daily[:7]],
            name='Cao nhất',
            marker_color='#4facfe'
        ))
        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            height=200,
            legend=dict(font=dict(color='#fff'), orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            xaxis=dict(showgrid=False, tickfont=dict(color='rgba(255,255,255,0.6)')),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='rgba(255,255,255,0.6)'))
        )
        charts['monthly'] = fig1.to_html(full_html=False, include_plotlyjs=False, config={'displayModeBar': False}).replace('\u2212', '-')

    # 2. AQI Distribution
    if aqi:
        val = aqi['val'] / 20 # back to 1-5
        labels = ['Tốt', 'Trung bình', 'Kém']
        if val <= 2: values = [1, 0, 0]
        elif val == 3: values = [0, 1, 0]
        else: values = [0, 0, 1]
        
        fig2 = go.Figure(data=[go.Pie(
            labels=labels, values=values,
            hole=.6,
            marker=dict(colors=['#4ade80', '#facc15', '#f87171']),
            textinfo='none'
        )])
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=200,
            showlegend=True,
            legend=dict(font=dict(color='#fff'), orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5)
        )
        charts['aqi_dist'] = fig2.to_html(full_html=False, include_plotlyjs=False, config={'displayModeBar': False}).replace('\u2212', '-')

    # 3. Weather Events (Precip probability)
    if hourly:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=[f"+{i*3}h" for i in range(len(hourly[:8]))],
            y=[h['pop'] for h in hourly[:8]],
            mode='lines+markers',
            name='Xác suất mưa (%)',
            line=dict(color='#facc15', width=3),
            fill='tozeroy',
            fillcolor='rgba(250, 204, 21, 0.1)'
        ))
        fig3.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            height=300,
            xaxis=dict(showgrid=False, tickfont=dict(color='rgba(255,255,255,0.6)')),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='rgba(255,255,255,0.6)'))
        )
        charts['events'] = fig3.to_html(full_html=False, include_plotlyjs=False, config={'displayModeBar': False}).replace('\u2212', '-')

    return charts
