import streamlit as st
import os
import json
import pandas as pd
import matplotlib.pyplot as plt

def load_metadata():
    """Load metadata from JSON file"""
    metadata_file = "data/metadata.json"
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            return json.load(f)
    return []

def create_analytics_dashboard():
    """Create analytics dashboard for collected data"""
    st.title("📊 Data Collection Analytics")
    
    metadata = load_metadata()
    
    if not metadata:
        st.warning("No data available for analytics. Please collect some data first!")
        return
    
    df = pd.DataFrame(metadata)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Files", len(df))
    
    with col2:
        st.metric("Data Types", df['data_type'].nunique())
    
    with col3:
        st.metric("Collection Days", df['date'].nunique())
    
    with col4:
        latest_date = df['timestamp'].max().strftime("%Y-%m-%d")
        st.metric("Latest Collection", latest_date)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Data Type Distribution")
        type_counts = df['data_type'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        type_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=colors)
        ax.set_ylabel('')
        st.pyplot(fig)
    
    with col2:
        st.subheader("📅 Collection Timeline")
        daily_counts = df.groupby('date').size()
        fig, ax = plt.subplots(figsize=(10, 6))
        daily_counts.plot(kind='line', ax=ax, marker='o')
        ax.set_title("Daily Data Collection")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Files")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    # Detailed breakdown
    st.subheader("🔍 Detailed Breakdown")
    
    # Data type breakdown
    for data_type in df['data_type'].unique():
        with st.expander(f"{data_type.upper()} Data Details"):
            type_df = df[df['data_type'] == data_type]
            st.write(f"Total {data_type} files: {len(type_df)}")
            
            # Category breakdown if available
            if 'additional_info' in type_df.columns:
                categories = []
                for info in type_df['additional_info']:
                    if isinstance(info, dict) and 'category' in info:
                        categories.append(info['category'])
                
                if categories:
                    category_counts = pd.Series(categories).value_counts()
                    st.write("Categories:")
                    st.bar_chart(category_counts)
            
            st.write("Recent files:")
            recent_files = type_df.nlargest(5, 'timestamp')[['filename', 'timestamp']]
            st.dataframe(recent_files)

if __name__ == "__main__":
    create_analytics_dashboard()
