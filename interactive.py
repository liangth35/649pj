import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data
df=pd.read_csv('pj3.csv')
df=df[df.Question=='Mammogram in Past 2 Years']
state_map = data.us_10m.url

select_state = alt.selection_single(fields=['id'], init={'id': 48}, )

map1 = alt.Chart(alt.topo_feature(state_map, 'states')).mark_geoshape().encode(
   color=alt.Color('Difference(%):Q', scale=alt.Scale(scheme='reds')),
   opacity=alt.condition(select_state, alt.value(1), alt.value(0.5)),
   tooltip=['State:N', 'Difference(%):Q'],
).transform_lookup(
   lookup='id',
   from_=alt.LookupData(df, key='id', fields=['Difference(%)','State'])
).project(
   'albersUsa'
).add_selection(
   select_state
)

bar = alt.Chart(df).mark_bar().encode(
   y=alt.Y('mean(Percentage):Q',scale=alt.Scale(domain=[0, 100]), title='Percentage(%)'),
   x=alt.X('Status:N'),
   tooltip=alt.Tooltip('mean(Percentage):Q', format='.1f'),
).transform_filter(
   select_state
)

chart=(map1|bar).resolve_scale(y='shared').configure_view(strokeWidth=0).configure_legend(orient='left')
chart.title =  alt.TitleParams('Difference between the percentage of normal and disabled people who have taken mammogram in the past two years', anchor='middle')
st.altair_chart(chart, theme='streamlit')