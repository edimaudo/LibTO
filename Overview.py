from utils import *
from data import *

st.title(APP_NAME)
st.header(OVERVIEW_HEADER)
st.write("LibTO is a civic intelligence app designed for Toronto denizens to get insights into the Toronto Public Library (TPL) Network.")

# KPIs
num_libraries = len(physical)
avg_sq_ft = f"{physical['SquareFootage'].mean():,.0f}"
oldest_info = f"{oldest['BranchName']}"
avg_ws = f"{physical['Workstations'].mean():.0f}"
kidstop = f"{physical['KidsStop'].sum():.0f}"
leading_reading = f"{physical['LeadingReading'].sum():.0f}"
teen_council = f"{physical['TeenCouncil'].sum():.0f}"
youth_hub = f"{physical['YouthHub'].sum():.0f}"
adult_literacy = f"{physical['AdultLiteracyProgram'].sum():.0f}"

top_container = st.container()
bottom_container = st.container()

with top_container:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="No. of Branches", value=num_libraries)
        st.metric(label="Oldest Branch", value=oldest_info)
        st.metric(label="Avg. Branch Sq. Footage", value=avg_sq_ft) 
    with col2:
        st.metric(label="Youth Hubs Branches", value=youth_hub)
        st.metric(label="Teen Council Branches", value=teen_council)
        st.metric(label="Leading Reading Branches", value=leading_reading )
    with col3:
        st.metric(label="Avg. Branch Workstations", value=int(avg_ws))
        st.metric(label="Kid Stop Branches", value=kidstop)
        st.metric(label="Adult Literacy Branches", value=adult_literacy)

with bottom_container:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["TPL Network Q&A",'Branch Size Heatmap', "Branch Metrics Rankings", "Branch Size vs Metrics", "Metric Correlations", "Annual Metrics Trends"])
    with tab1:
        map_clean = df_map_data.dropna(subset=['Lat', 'Long']).copy()
        map_clean['SquareFootage'] = pd.to_numeric(map_clean['SquareFootage'], errors='coerce')
        map_clean.dropna(subset=['SquareFootage'], inplace=True)
        fig_heatmap = px.scatter_map(
                map_clean, lat="Lat", lon="Long", size="SquareFootage", color="SquareFootage",
                hover_name="BranchName", hover_data={"Address": True, "SquareFootage": ':,.0f'},
                labels={"SquareFootage": "Sq. Ft"}, color_continuous_scale=px.colors.sequential.Plasma,
                zoom=10, center={"lat": 43.7, "lon": -79.4}, map_style="carto-positron"
            )
        fig_heatmap.update_layout(template='plotly_white', height=400,title_text="Square Footage Heatmap", title_x=0.5)
        st.plotly_chart(fig_heatmap, width='stretch')
        
        with tab2: st.plotly_chart(fig_rankings, width='stretch')
        with tab3: st.plotly_chart(fig_bubble, width='stretch')
        with tab4: st.plotly_chart(fig_correlation)
        with tab5: 
            col_a, col_b = st.columns(2)
            for i, m in enumerate(METRIC_MAP):
                annual = m['df'].groupby('Year')[m['id']].sum().reset_index()
                fig_t = px.line(annual, x='Year', y=m['id'], title=f'{m["label"]} Trend',hover_data={m['id']: ':.0f'})
                fig_t.update_layout(template='plotly_white', height=400, title_x=0.5)
                if i % 2 == 0: col_a.plotly_chart(fig_t)
                else: col_b.plotly_chart(fig_t)
        with tab6:
            st.write("Ask a question about the Toronto Public Library Network or Metrics")
            tpl_question_txt = st.text_area(label=" ",value="",placeholder=None,key=1)
            tpl_question_button = st.button("Get Inisghts", type="primary")
            instruction="""
                Return your entire response in professional Markdown format:
                1. Use ## for Section Headers. The sections are 'Question','Analysis','Insight'
                2. Use **bold** for key insights and numbers.
                3. Use Markdown tables if comparing multiple data points.
                4. If there is a clear trend, add a 'Key Takeaway' section at the end.
            """
            if tpl_question_button:
                st.html("<p> </p>")
                if tpl_question_txt.strip():    
                    st.subheader("Q&A Results")
                    with st.spinner("Analyzing data..."):
                        analysis = analyze_dataframe(df_master, tpl_question_txt,instruction)
                        st.markdown(analysis)
                else:
                    st.warning("Please enter a question in the text area above.")


                    