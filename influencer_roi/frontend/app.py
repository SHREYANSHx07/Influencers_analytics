import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Influencer ROI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Amazon theme
st.markdown("""
<style>
    .main-header {
        background-color: #146eb4;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9900;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stButton > button {
        background-color: #ff9900;
        color: white;
        border: none;
        border-radius: 0.25rem;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        background-color: #e68900;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://localhost:8000/api"

def safe_convert(value, target_type=float, default=0):
    """Safely convert value to target type with default fallback"""
    try:
        if target_type == float:
            return float(str(value).replace(',', ''))
        elif target_type == int:
            return int(str(value).replace(',', ''))
        else:
            return value
    except (ValueError, TypeError):
        return default

def fetch_data(endpoint, params=None):
    """Fetch data from Django API"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}/", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Influencer Marketing ROI Dashboard</h1>
        <p>Track performance, analyze ROAS, and optimize your influencer campaigns</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.markdown("## 🔍 Filters")
    
    # Date range filter
    st.sidebar.markdown("### Date Range")
    st.sidebar.markdown("*💡 Tip: Sample data is from 2024*")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime(2024, 1, 1))
    with col2:
        end_date = st.date_input("End Date", value=datetime(2024, 12, 31))
    
    # Platform filter
    platforms = ["All", "Instagram", "YouTube", "Twitter", "TikTok", "LinkedIn"]
    selected_platform = st.sidebar.selectbox("Platform", platforms)
    
    # Category filter
    categories = ["All", "Fashion", "Tech", "Fitness", "Beauty", "Food", "Travel"]
    selected_category = st.sidebar.selectbox("Category", categories)
    
    # Gender filter
    genders = ["All", "Male", "Female", "Other"]
    selected_gender = st.sidebar.selectbox("Gender", genders)
    
    # Brand filter
    brands = ["All", "Nike", "Adidas", "Apple", "Samsung", "Coca-Cola", "Pepsi", "McDonald's", "KFC"]
    selected_brand = st.sidebar.selectbox("Brand", brands)
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Campaign Performance", 
        "👥 Influencer Comparison", 
        "💰 Incremental ROAS", 
        "💸 Payout Tracking", 
        "💡 Insights & Innovation"
    ])
    
    with tab1:
        show_campaign_performance(start_date, end_date, selected_platform, selected_category, selected_gender, selected_brand)
    
    with tab2:
        show_influencer_comparison(start_date, end_date, selected_platform, selected_category, selected_gender, selected_brand)
    
    with tab3:
        show_incremental_roas(start_date, end_date, selected_platform, selected_category, selected_gender, selected_brand)
    
    with tab4:
        show_payout_tracking(start_date, end_date, selected_platform, selected_category, selected_gender, selected_brand)
    
    with tab5:
        show_insights_innovation(start_date, end_date, selected_platform, selected_category, selected_gender, selected_brand)

def show_campaign_performance(start_date, end_date, platform, category, gender, brand):
    """Campaign Performance Dashboard"""
    st.markdown("## 📈 Campaign Performance")
    
    # Fetch summary data
    params = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
    
    # Add filters if not "All"
    if platform != "All":
        params['influencer__platform'] = platform.lower()
    if category != "All":
        params['influencer__category'] = category
    if gender != "All":
        params['influencer__gender'] = gender.lower()
    if brand != "All":
        params['influencer__brand'] = brand.lower()
    
    tracking_summary = fetch_data('tracking/summary', params)
    
    if tracking_summary:
        # KPI metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = safe_convert(tracking_summary['total_revenue'], float, 0)
            st.metric(
                "Total Revenue", 
                f"${total_revenue:,.2f}",
                delta=f"${total_revenue * 0.05:,.2f}"
            )
        
        with col2:
            total_orders = safe_convert(tracking_summary['total_orders'], int, 0)
            st.metric(
                "Total Orders", 
                f"{total_orders:,}",
                delta=f"{total_orders * 0.03:,}"
            )
        
        with col3:
            avg_order_value = safe_convert(tracking_summary['average_order_value'], float, 0)
            st.metric(
                "Avg Order Value", 
                f"${avg_order_value:,.2f}",
                delta=f"${avg_order_value * 0.02:,.2f}"
            )
        
        with col4:
            st.metric(
                "Active Campaigns", 
                f"{tracking_summary['total_campaigns']}",
                delta="2"
            )
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Revenue by Campaign")
            campaign_data = fetch_data('tracking/by_campaign', params)
            if campaign_data and len(campaign_data) > 0:
                df = pd.DataFrame(campaign_data)
                if not df.empty and 'campaign' in df.columns and 'total_revenue' in df.columns:
                    fig = px.bar(
                        df.head(10), 
                        x='campaign', 
                        y='total_revenue',
                        title="Top 10 Campaigns by Revenue",
                        color='total_revenue',
                        color_continuous_scale='Blues'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No campaign data available yet.")
            else:
                st.info("No campaign data available yet.")
        
        with col2:
            st.markdown("### Revenue by Influencer")
            influencer_data = fetch_data('tracking/by_influencer', params)
            if influencer_data and len(influencer_data) > 0:
                df = pd.DataFrame(influencer_data)
                if not df.empty and 'influencer__name' in df.columns and 'total_revenue' in df.columns:
                    fig = px.bar(
                        df.head(10), 
                        x='influencer__name', 
                        y='total_revenue',
                        title="Top 10 Influencers by Revenue",
                        color='total_revenue',
                        color_continuous_scale='Oranges'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No influencer data available yet.")
            else:
                st.info("No influencer data available yet.")

def show_influencer_comparison(start_date, end_date, platform, category, gender, brand):
    """Influencer Comparison Dashboard"""
    st.markdown("## 👥 Influencer Comparison")
    
    # Fetch influencer data
    params = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
    
    # Add filters if not "All"
    if platform != "All":
        params['platform'] = platform.lower()
    if category != "All":
        params['category'] = category
    if gender != "All":
        params['gender'] = gender.lower()
    if brand != "All":
        params['brand'] = brand.lower()
    
    influencers = fetch_data('influencers', params)
    
    if influencers and 'results' in influencers:
        # Extract results from paginated response
        influencers_data = influencers['results']
        
        # Top performers
        st.markdown("### 🏆 Top Performing Influencers")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### By Revenue")
            top_revenue = fetch_data('influencers/top_performers', params)
            if top_revenue and len(top_revenue) > 0:
                df = pd.DataFrame(top_revenue)
                if not df.empty and 'name' in df.columns and 'total_revenue' in df.columns:
                    fig = px.bar(
                        df.head(10), 
                        x='name', 
                        y='total_revenue',
                        title="Top 10 Influencers by Revenue",
                        color='total_revenue',
                        color_continuous_scale='Greens'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No revenue data available yet.")
            else:
                st.info("No top performers data available yet.")
        
        with col2:
            st.markdown("#### By Engagement Rate")
            df = pd.DataFrame(influencers_data)
            if not df.empty and 'follower_count' in df.columns and 'engagement_rate' in df.columns:
                fig = px.scatter(
                    df, 
                    x='follower_count', 
                    y='engagement_rate',
                    size='total_revenue',
                    color='platform',
                    hover_data=['name', 'category'],
                    title="Engagement Rate vs Follower Count"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No engagement data available yet.")
    else:
        st.info("No influencer data available yet. Upload some data to see analytics!")
        
        # Platform analysis
        st.markdown("### 📱 Platform Analysis")
        platform_data = fetch_data('influencers/by_platform', params)
        if platform_data and len(platform_data) > 0:
            df = pd.DataFrame(platform_data)
            if not df.empty and 'count' in df.columns and 'platform' in df.columns:
                fig = px.pie(
                    df, 
                    values='count', 
                    names='platform',
                    title="Influencer Distribution by Platform"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No platform data available yet.")
        else:
            st.info("No platform data available yet.")

def show_incremental_roas(start_date, end_date, platform, category, gender, brand):
    """Incremental ROAS Analysis"""
    st.markdown("## 💰 Incremental ROAS Analysis")
    
    params = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
    
    # Add filters if not "All"
    if platform != "All":
        params['influencer__platform'] = platform.lower()
    if category != "All":
        params['influencer__category'] = category
    if gender != "All":
        params['influencer__gender'] = gender.lower()
    if brand != "All":
        params['influencer__brand'] = brand.lower()
    
    # ROAS analysis
    roas_data = fetch_data('tracking/roas_analysis', params)
    
    if roas_data:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_revenue = safe_convert(roas_data['total_revenue'], float, 0)
            st.metric(
                "Total Revenue", 
                f"${total_revenue:,.2f}"
            )
        
        with col2:
            total_payouts = safe_convert(roas_data['total_payouts'], float, 0)
            st.metric(
                "Total Payouts", 
                f"${total_payouts:,.2f}"
            )
        
        with col3:
            roas_value = safe_convert(roas_data['roas'], float, 0)
            roas_percentage = safe_convert(roas_data['roas_percentage'], float, 0)
            if roas_value > 0:
                st.metric(
                    "Overall ROAS", 
                    f"{roas_value:.2f}x",
                    delta=f"{roas_percentage:.1f}%"
                )
            else:
                st.metric(
                    "Overall ROAS", 
                    "N/A"
                )
        
        # ROAS by influencer
        st.markdown("### ROAS by Influencer")
        payout_data = fetch_data('payouts/by_influencer', params)
        if payout_data and len(payout_data) > 0:
            df = pd.DataFrame(payout_data)
            if not df.empty and 'avg_roas' in df.columns:
                fig = px.bar(
                    df.head(15), 
                    x='influencer__name', 
                    y='avg_roas',
                    title="ROAS by Influencer",
                    color='avg_roas',
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No ROAS data available yet. Upload some data to see analytics!")
        else:
            st.info("No payout data available yet. Upload some data to see analytics!")

def show_payout_tracking(start_date, end_date, platform, category, gender, brand):
    """Payout Tracking Dashboard"""
    st.markdown("## 💸 Payout Tracking")
    
    params = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
    
    # Add filters if not "All"
    if platform != "All":
        params['influencer__platform'] = platform.lower()
    if category != "All":
        params['influencer__category'] = category
    if gender != "All":
        params['influencer__gender'] = gender.lower()
    if brand != "All":
        params['influencer__brand'] = brand.lower()
    
    payout_summary = fetch_data('payouts/summary', params)
    efficiency_metrics = fetch_data('payouts/efficiency_metrics', params)
    
    if payout_summary and efficiency_metrics:
        # KPI metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_payouts = safe_convert(payout_summary['total_payouts'], float, 0)
            st.metric(
                "Total Payouts", 
                f"${total_payouts:,.2f}"
            )
        
        with col2:
            total_orders = safe_convert(payout_summary['total_orders'], int, 0)
            st.metric(
                "Total Orders", 
                f"{total_orders:,}"
            )
        
        with col3:
            avg_roas = safe_convert(payout_summary['average_roas'], float, 0)
            if avg_roas > 0:
                st.metric(
                    "Avg ROAS", 
                    f"{avg_roas:.2f}x"
                )
            else:
                st.metric(
                    "Avg ROAS", 
                    "N/A"
                )
        
        with col4:
            st.metric(
                "Active Influencers", 
                f"{payout_summary['total_influencers']}"
            )
        
        # Efficiency Metrics
        st.markdown("### 📊 Payout Efficiency Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_payout_per_order = safe_convert(efficiency_metrics['avg_payout_per_order'], float, 0)
            st.metric(
                "Avg Payout/Order", 
                f"${avg_payout_per_order:,.2f}"
            )
        
        with col2:
            avg_payout_per_influencer = safe_convert(efficiency_metrics['avg_payout_per_influencer'], float, 0)
            st.metric(
                "Avg Payout/Influencer", 
                f"${avg_payout_per_influencer:,.2f}"
            )
        
        with col3:
            payout_efficiency = safe_convert(efficiency_metrics['payout_efficiency'], float, 0)
            st.metric(
                "Payout Efficiency", 
                f"{payout_efficiency:.1f} orders/influencer"
            )
        
        with col4:
            overall_roas = safe_convert(efficiency_metrics['overall_roas'], float, 0)
            if overall_roas > 0:
                st.metric(
                    "Overall ROAS", 
                    f"{overall_roas:.2f}x"
                )
            else:
                st.metric(
                    "Overall ROAS", 
                    "N/A"
                )
        
        # Charts Section 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Payouts by Basis Type")
            basis_data = fetch_data('payouts/by_basis', params)
            if basis_data and len(basis_data) > 0:
                df = pd.DataFrame(basis_data)
                if not df.empty and 'total_payout' in df.columns:
                    fig = px.pie(
                        df, 
                        values='total_payout', 
                        names='basis',
                        title="Payout Distribution by Basis"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No payout data available yet.")
            else:
                st.info("No payout data available yet.")
        
        with col2:
            st.markdown("### Top Performers by Payout")
            top_performers = fetch_data('payouts/top_performers', params)
            if top_performers and len(top_performers) > 0:
                df = pd.DataFrame(top_performers)
                if not df.empty and 'total_payout' in df.columns:
                    fig = px.bar(
                        df.head(10), 
                        x='influencer__name', 
                        y='total_payout',
                        title="Top 10 Influencers by Payout",
                        color='total_payout',
                        color_continuous_scale='Greens'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No payout data available yet.")
            else:
                st.info("No payout data available yet.")
        
        # Charts Section 2 - Platform Analysis
        st.markdown("### 📱 Payout Analysis by Platform")
        platform_data = fetch_data('payouts/by_platform', params)
        if platform_data and len(platform_data) > 0:
            df = pd.DataFrame(platform_data)
            if not df.empty and 'total_payout' in df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.bar(
                        df, 
                        x='influencer__platform', 
                        y='total_payout',
                        title="Total Payouts by Platform",
                        color='avg_roas',
                        color_continuous_scale='RdYlGn'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.bar(
                        df, 
                        x='influencer__platform', 
                        y='avg_roas',
                        title="ROAS by Platform",
                        color='avg_roas',
                        color_continuous_scale='RdYlGn'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No platform payout data available yet.")
        else:
            st.info("No platform payout data available yet.")
        
        # Charts Section 3 - Category Analysis
        st.markdown("### 🏷️ Payout Analysis by Category")
        category_data = fetch_data('payouts/by_category', params)
        if category_data and len(category_data) > 0:
            df = pd.DataFrame(category_data)
            if not df.empty and 'total_payout' in df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.bar(
                        df, 
                        x='influencer__category', 
                        y='total_payout',
                        title="Total Payouts by Category",
                        color='avg_roas',
                        color_continuous_scale='RdYlGn'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.bar(
                        df, 
                        x='influencer__category', 
                        y='avg_roas',
                        title="ROAS by Category",
                        color='avg_roas',
                        color_continuous_scale='RdYlGn'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No category payout data available yet.")
        else:
            st.info("No category payout data available yet.")
        
        # Charts Section 4 - ROAS Analysis
        st.markdown("### 💰 ROAS Performance Analysis")
        payout_data = fetch_data('payouts/by_influencer', params)
        if payout_data and len(payout_data) > 0:
            df = pd.DataFrame(payout_data)
            if not df.empty and 'avg_roas' in df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Top ROAS performers
                    top_roas = df.nlargest(10, 'avg_roas')
                    fig = px.bar(
                        top_roas, 
                        x='influencer__name', 
                        y='avg_roas',
                        title="Top 10 ROAS Performers",
                        color='avg_roas',
                        color_continuous_scale='RdYlGn'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Payout vs ROAS scatter plot
                    fig = px.scatter(
                        df, 
                        x='total_payout', 
                        y='avg_roas',
                        title="Payout vs ROAS Performance",
                        color='avg_roas',
                        color_continuous_scale='RdYlGn',
                        hover_data=['influencer__name', 'total_orders']
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No ROAS data available yet.")
        else:
            st.info("No ROAS data available yet.")
        
        # Performance Summary Table
        st.markdown("### 📋 Payout Performance Summary")
        if payout_data and len(payout_data) > 0:
            df = pd.DataFrame(payout_data)
            if not df.empty:
                # Calculate summary statistics
                summary_stats = {
                    'Metric': [
                        'Total Influencers',
                        'Average ROAS',
                        'Highest ROAS',
                        'Lowest ROAS',
                        'Average Payout',
                        'Highest Payout',
                        'Total Orders'
                    ],
                    'Value': [
                        len(df),
                        f"{df['avg_roas'].mean():.2f}x",
                        f"{df['avg_roas'].max():.2f}x",
                        f"{df['avg_roas'].min():.2f}x",
                        f"${df['total_payout'].mean():,.2f}",
                        f"${df['total_payout'].max():,.2f}",
                        f"{df['total_orders'].sum():,}"
                    ]
                }
                
                summary_df = pd.DataFrame(summary_stats)
                st.dataframe(summary_df, use_container_width=True)
            else:
                st.info("No performance data available yet.")
        else:
            st.info("No performance data available yet.")
    else:
        st.info("No payout data available yet. Upload some data to see analytics!")

def show_insights_innovation(start_date, end_date, platform, category, gender, brand):
    """Insights and Innovation Dashboard"""
    st.markdown("## 💡 Insights & Innovation")
    
    # Innovation ideas section
    st.markdown("### 🚀 Innovation Ideas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Predictive Analytics")
        st.info("""
        **Next Best Influencer Prediction**
        - Use machine learning to predict which influencers will perform best
        - Consider factors: follower count, engagement rate, category match
        - Implement A/B testing for new influencer partnerships
        """)
        
        st.markdown("#### What-If Scenarios")
        st.info("""
        **Rate Optimization Tool**
        - Adjust payout rates and predict ROI impact
        - Test different compensation models
        - Optimize for maximum ROAS
        """)
    
    with col2:
        st.markdown("#### Performance Alerts")
        st.info("""
        **Smart Notifications**
        - Alert on underperforming campaigns
        - Flag influencers below ROAS thresholds
        - Real-time performance monitoring
        """)
        
        st.markdown("#### Trend Analysis")
        st.info("""
        **Seasonal Patterns**
        - Identify best posting times
        - Track seasonal performance trends
        - Optimize campaign timing
        """)
    
    # Data upload section
    st.markdown("### 📤 Data Upload")
    
    # Clear database button (for testing)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Database (Testing)", type="secondary"):
            try:
                response = requests.post(f"{API_BASE_URL}/clear/")
                if response.status_code == 200:
                    st.success("Database cleared successfully!")
                else:
                    st.error(f"Failed to clear database: {response.text}")
            except Exception as e:
                st.error(f"Error clearing database: {str(e)}")
    
    with col2:
        st.info("💡 **Tip**: Clear database first to test uploads")
    
    uploaded_file = st.file_uploader(
        "Upload CSV/JSON data", 
        type=['csv', 'json'],
        help="Upload influencer, post, tracking, or payout data"
    )
    
    if uploaded_file is not None:
        model_type = st.selectbox(
            "Select data type",
            ["influencers", "posts", "tracking", "payouts"]
        )
        
        if st.button("Upload Data"):
            try:
                files = {'file': uploaded_file}
                data = {'model_type': model_type}
                
                response = requests.post(
                    f"{API_BASE_URL}/upload/",
                    files=files,
                    data=data
                )
                
                if response.status_code == 201:
                    result = response.json()
                    st.success(result['message'])
                    
                    # Show detailed statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Records", result.get('total_records', 0))
                    with col2:
                        st.metric("Created", result.get('created_count', 0))
                    with col3:
                        st.metric("Already Existed", result.get('existing_count', 0))
                    
                    if result.get('errors'):
                        st.warning(f"Some errors occurred: {result['errors']}")
                else:
                    st.error(f"Upload failed: {response.text}")
                    
            except Exception as e:
                st.error(f"Upload error: {str(e)}")

if __name__ == "__main__":
    main() 