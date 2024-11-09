import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from data_processing import create_dataframe
from datetime import datetime

#data_file = 'data/transactions_emil.txt'
#data_file = 'data/transactions_test.txt'
data_file = 'data/transactions.txt'

df = create_dataframe(data_file)
df = df[df['Amount'] > -1000000]

#print(df.info())
#     Column    Non-Null Count  Dtype         
#---  ------    --------------  -----         
# 0   Datetime  228 non-null    datetime64[ns]
# 1   Title     228 non-null    object        
# 2   Amount    228 non-null    float64   


df['Type'] = df['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')
df['Amount'] = df['Amount'].abs()

df['Day'] = df['Datetime'].dt.date
df['Week'] = df['Datetime'].dt.to_period('W').apply(lambda r: r.start_time.date())
df['Month'] = df['Datetime'].dt.to_period('M').apply(lambda r: r.start_time.date())

min_date = df['Day'].min()
max_date = df['Day'].max()

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Income and Expense Analysis", style={'textAlign': 'center'}),
    
    html.Div([
        html.H3("Select Date Range:", style={'marginBottom': '10px'}),
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            start_date=min_date,
            end_date=max_date,
            display_format='YYYY-MM-DD'
        )
    ], style={'margin': '20px', 'textAlign': 'center'}),

    html.Div([
        html.H2("Daily Expenses"),
        dcc.Graph(id='daily-expenses')
    ]),

    html.Div([
        html.H2("Daily Expenses by Title (stacked)"),
        dcc.Graph(id='daily-expenses-by-title')
    ]),

    html.Div([
        html.H2("Weekly Expenses"),
        dcc.Graph(id='weekly-expenses')
    ]),

    html.Div([
        html.H2("Weekly Expenses by Title (stacked)"),
        dcc.Graph(id='weekly-expenses-by-title')
    ]),

    html.Div([
        html.H2("Monthly Expenses"),
        dcc.Graph(id='monthly-expenses')
    ]),

    html.Div([
        html.H2("Monthly Expenses by Title (stacked)"),
        dcc.Graph(id='monthly-expenses-by-title')
    ]),

    html.Div([
        html.H2("Weekly Incomes"),
        dcc.Graph(id='weekly-incomes')
    ]),
    
    html.Div([
        html.H2("Monthly Incomes"),
        dcc.Graph(id='monthly-incomes')
    ]),
])

def create_daily_expenses(filtered_expenses):
    fig = px.bar(
        filtered_expenses.groupby('Day')['Amount'].sum().div(1_000).round(2).reset_index(),
        x='Day', y='Amount', title='Daily Expenses (in thousands)',
        labels={'Day': 'Date', 'Amount': 'Amount (K UZS)'}
    )
    fig.update_xaxes(tickformat="%Y-%m-%d")
    fig.update_traces(texttemplate='%{y:.2f}K', textposition='outside')
    fig.update_layout(
        margin=dict(t=50), yaxis=dict(tickformat=".2f"),
        uniformtext_minsize=8, uniformtext_mode='hide',
        barmode='group', bargap=0.15
    )
    return fig

def create_daily_expenses_by_title(filtered_expenses):
    daily_expenses_by_title = (
        filtered_expenses.groupby(['Day', 'Title'])['Amount']
        .sum()
        .div(1_000)
        .round(2)
        .reset_index()
    )
    fig = px.bar(
        daily_expenses_by_title,
        x='Day', y='Amount', color='Title',
        title='Daily Expenses by Title (in thousands)',
        labels={'Day': 'Date', 'Amount': 'Amount (K UZS)', 'Title': 'Category'}
    )
    fig.update_xaxes(tickformat="%Y-%m-%d")
    fig.update_traces(texttemplate='%{y:.2f}K', textposition='outside')
    fig.update_layout(
        margin=dict(t=50), yaxis=dict(tickformat=".2f"),
        uniformtext_minsize=8, uniformtext_mode='hide',
        barmode='stack', bargap=0.15,
        showlegend=False
    )
    return fig

def create_weekly_expenses(filtered_expenses):
    weekly_expenses = filtered_expenses.groupby('Week')['Amount'].sum().div(1_000_000).round(2).reset_index()
    weekly_expenses['Week'] = weekly_expenses['Week'].astype(str)
    fig = px.bar(
        weekly_expenses.sort_values(by='Week'),
        x='Week', y='Amount', title='Weekly Expenses (in millions)',
        labels={'Week': 'Week Start Date', 'Amount': 'Amount (M UZS)'}
    )
    fig.update_xaxes(type='category')
    fig.update_traces(texttemplate='%{y:.2f}M', textposition='outside')
    fig.update_layout(
        margin=dict(t=50), yaxis=dict(tickformat=".2f"),
        uniformtext_minsize=8, uniformtext_mode='hide',
        barmode='group', bargap=0.15
    )
    return fig

def create_weekly_expenses_by_title(filtered_expenses):
    weekly_expenses_by_title = (
        filtered_expenses.groupby(['Week', 'Title'])['Amount']
        .sum()
        .div(1_000_000)
        .round(2)
        .reset_index()
    )
    weekly_expenses_by_title['Week'] = weekly_expenses_by_title['Week'].astype(str)
    
    weekly_totals = weekly_expenses_by_title.groupby('Week')['Amount'].sum().reset_index()
    
    fig = px.bar(
        weekly_expenses_by_title,
        x='Week', y='Amount', color='Title',
        title='Weekly Expenses by Title (stacked, in millions)',
        labels={'Week': 'Week Start Date', 'Amount': 'Amount (M UZS)', 'Title': 'Category'}
    )
    
    fig.update_xaxes(type='category')
    fig.update_traces(textposition='outside')
    fig.update_layout(
        margin=dict(t=50), yaxis=dict(tickformat=".2f"),
        uniformtext_minsize=8, uniformtext_mode='hide',
        barmode='stack', bargap=0.15
    )
    
    for i, row in weekly_totals.iterrows():
        fig.add_annotation(
            x=row['Week'], y=row['Amount'],
            text=f"{row['Amount']:.2f}M",
            showarrow=False,
            yshift=10
        )
    
    return fig

def create_monthly_expenses(filtered_expenses):
    monthly_expenses = filtered_expenses.groupby('Month')['Amount'].sum().div(1_000_000).round(2).reset_index()
    monthly_expenses['Month'] = monthly_expenses['Month'].astype(str)
    fig = px.bar(
        monthly_expenses.sort_values(by='Month'),
        x='Month', y='Amount', title='Monthly Expenses (in millions)',
        labels={'Month': 'Month', 'Amount': 'Amount (M UZS)'}
    )
    fig.update_xaxes(type='category')
    fig.update_traces(texttemplate='%{y:.2f}M', textposition='outside')
    fig.update_layout(
        margin=dict(t=50), yaxis=dict(tickformat=".2f"),
        uniformtext_minsize=8, uniformtext_mode='hide',
        barmode='group', bargap=0.15
    )
    return fig

def create_monthly_expenses_by_title(filtered_expenses):
    monthly_expenses_by_title = (
        filtered_expenses.groupby(['Month', 'Title'])['Amount']
        .sum()
        .div(1_000_000)
        .round(2)
        .reset_index()
    )
    monthly_expenses_by_title['Month'] = monthly_expenses_by_title['Month'].astype(str)
    
    fig = px.bar(
        monthly_expenses_by_title,
        x='Month', y='Amount', color='Title',
        title='Monthly Expenses by Title (stacked, in millions)',
        labels={'Month': 'Month', 'Amount': 'Amount (M UZS)', 'Title': 'Category'}
    )
    fig.update_xaxes(type='category')
    fig.update_traces(textposition='outside')
    fig.update_layout(
        margin=dict(t=50), yaxis=dict(tickformat=".2f"),
        uniformtext_minsize=8, uniformtext_mode='hide',
        barmode='stack', bargap=0.15
    )
    return fig

def create_weekly_incomes(filtered_incomes):
    weekly_incomes = filtered_incomes.groupby('Week')['Amount'].sum().div(1_000_000).round(2).reset_index()
    weekly_incomes['Week'] = weekly_incomes['Week'].astype(str)
    fig = px.bar(
        weekly_incomes.sort_values(by='Week'),
        x='Week', y='Amount', title='Weekly Incomes (in millions)',
        labels={'Week': 'Week Start Date', 'Amount': 'Amount (M UZS)'},
        color_discrete_sequence=['green']
    )
    fig.update_xaxes(type='category')
    fig.update_traces(texttemplate='%{y:.2f}M', textposition='outside')
    fig.update_layout(
        margin=dict(t=50), yaxis=dict(tickformat=".2f"),
        uniformtext_minsize=8, uniformtext_mode='hide',
        barmode='group', bargap=0.15
    )
    return fig

def create_monthly_incomes(filtered_incomes):
    monthly_incomes = filtered_incomes.groupby('Month')['Amount'].sum().div(1_000_000).round(2).reset_index()
    monthly_incomes['Month'] = monthly_incomes['Month'].astype(str)
    fig = px.bar(
        monthly_incomes.sort_values(by='Month'),
        x='Month', y='Amount', title='Monthly Incomes (in millions)',
        labels={'Month': 'Month', 'Amount': 'Amount (M UZS)'},
        color_discrete_sequence=['green']
    )
    fig.update_xaxes(type='category')
    fig.update_traces(texttemplate='%{y:.2f}M', textposition='outside')
    fig.update_layout(
        margin=dict(t=50), yaxis=dict(tickformat=".2f"),
        uniformtext_minsize=8, uniformtext_mode='hide',
        barmode='group', bargap=0.15
    )
    return fig

@app.callback(
    [
        Output('daily-expenses', 'figure'),
        Output('daily-expenses-by-title', 'figure'),
        Output('weekly-expenses', 'figure'),
        Output('weekly-expenses-by-title', 'figure'),
        Output('monthly-expenses', 'figure'),
        Output('monthly-expenses-by-title', 'figure'),
        Output('weekly-incomes', 'figure'),
        Output('monthly-incomes', 'figure')
    ],
    [Input('date-range', 'start_date'), Input('date-range', 'end_date')]
)
def update_graphs(start_date, end_date):
    filtered_df = df[(df['Day'] >= datetime.strptime(start_date, '%Y-%m-%d').date()) &
                     (df['Day'] <= datetime.strptime(end_date, '%Y-%m-%d').date())]
    
    filtered_expenses = filtered_df[filtered_df['Type'] == 'Expense']
    filtered_incomes = filtered_df[filtered_df['Type'] == 'Income']
    
    return (
        create_daily_expenses(filtered_expenses),
        create_daily_expenses_by_title(filtered_expenses),
        create_weekly_expenses(filtered_expenses),
        create_weekly_expenses_by_title(filtered_expenses),
        create_monthly_expenses(filtered_expenses),
        create_monthly_expenses_by_title(filtered_expenses),
        create_weekly_incomes(filtered_incomes),
        create_monthly_incomes(filtered_incomes)
    )

if __name__ == '__main__':
    app.run_server(debug=True)
