"""
Flora & Fauna Chatbot - Stage 2
Database-powered conversational AI for flora and fauna queries
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import re
from typing import List, Dict, Optional

try:
    from supabase_db import supabase_manager
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

class FloraFaunaChatbot:
    """AI Chatbot for Flora & Fauna database queries"""
    
    def __init__(self):
        self.conversation_history = []
        self.db_cache = None
        self.last_cache_update = None
        
    def load_database_content(self) -> Optional[pd.DataFrame]:
        """Load and cache database content for faster queries"""
        try:
            if not SUPABASE_AVAILABLE:
                return None
                
            current_time = datetime.now()
            
            # Cache data for 5 minutes to improve performance
            if (self.db_cache is None or 
                self.last_cache_update is None or 
                (current_time - self.last_cache_update).seconds > 300):
                
                self.db_cache = supabase_manager.get_all_data()
                self.last_cache_update = current_time
                
            return self.db_cache
            
        except Exception as e:
            st.error(f"Error loading database: {str(e)}")
            return None
    
    def extract_keywords(self, query: str) -> List[str]:
        """Extract relevant keywords from user query"""
        # Remove common words and extract meaningful terms
        stop_words = {'the', 'is', 'at', 'which', 'on', 'what', 'where', 'when', 'how', 'why', 'who', 'a', 'an', 'and', 'or', 'but', 'in', 'of', 'to', 'for', 'with', 'by'}
        
        # Clean and split query
        query_clean = re.sub(r'[^\w\s]', ' ', query.lower())
        words = [word.strip() for word in query_clean.split() if len(word.strip()) > 2]
        
        # Filter out stop words
        keywords = [word for word in words if word not in stop_words]
        
        return keywords[:10]  # Limit to top 10 keywords
    
    def search_database(self, query: str, keywords: List[str]) -> Dict:
        """Search database for relevant content"""
        df = self.load_database_content()
        
        if df is None or len(df) == 0:
            return {
                'found_items': 0,
                'results': [],
                'message': "No data available in the database."
            }
        
        results = []
        search_columns = ['title', 'description', 'content', 'category', 'tags', 'city', 'country']
        
        # Search for each keyword across relevant columns
        for _, row in df.iterrows():
            relevance_score = 0
            matched_fields = []
            
            # Check each searchable column
            for col in search_columns:
                if col in row and pd.notna(row[col]) and str(row[col]).strip():
                    content = str(row[col]).lower()
                    
                    # Count keyword matches
                    for keyword in keywords:
                        if keyword in content:
                            relevance_score += 1
                            if col not in matched_fields:
                                matched_fields.append(col)
            
            # Also check for direct query match
            row_text = " ".join([str(row.get(col, '')) for col in search_columns if pd.notna(row.get(col))])
            if any(keyword in row_text.lower() for keyword in keywords):
                relevance_score += 2
            
            # If relevant, add to results
            if relevance_score > 0:
                result_item = {
                    'relevance': relevance_score,
                    'data': row.to_dict(),
                    'matched_fields': matched_fields,
                    'type': row.get('entry_type', 'unknown'),
                    'title': row.get('title', 'Unknown'),
                    'description': row.get('description', 'No description'),
                    'location': f"{row.get('city', 'Unknown')}, {row.get('country', 'Unknown')}",
                    'timestamp': row.get('timestamp', 'Unknown')
                }
                results.append(result_item)
        
        # Sort by relevance score
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        return {
            'found_items': len(results),
            'results': results[:10],  # Limit to top 10 results
            'total_items': len(df),
            'message': f"Found {len(results)} relevant items from {len(df)} total records."
        }
    
    def generate_response(self, query: str, search_results: Dict) -> str:
        """Generate natural language response based on search results"""
        
        if search_results['found_items'] == 0:
            return f"""
🤖 **Flora & Fauna Assistant**: I couldn't find any information about "{query}" in our database.

💡 **Suggestions:**
- Try using different keywords
- Ask about specific locations, species, or data types
- Examples: "show me images from Mumbai", "audio recordings of birds", "text data about plants"

📊 **Database Status**: {search_results.get('total_items', 0)} total records available.
            """
        
        results = search_results['results']
        response_parts = []
        
        # Introduction
        response_parts.append(f"🤖 **Flora & Fauna Assistant**: I found {search_results['found_items']} relevant items for your query: \"{query}\"")
        
        # Top results summary
        response_parts.append("\n📋 **Top Results:**")
        
        for i, result in enumerate(results[:5], 1):
            data_type_icon = {
                'text': '📝', 'audio': '🎵', 
                'video': '🎥', 'image': '🖼️'
            }.get(result['type'], '📄')
            
            response_parts.append(f"\n**{i}. {data_type_icon} {result['title']}**")
            response_parts.append(f"   📍 Location: {result['location']}")
            
            if result['description'] and result['description'] != 'No description':
                desc = result['description'][:100] + "..." if len(result['description']) > 100 else result['description']
                response_parts.append(f"   📄 Description: {desc}")
            
            response_parts.append(f"   🕐 Collected: {result['timestamp'][:10] if result['timestamp'] != 'Unknown' else 'Unknown date'}")
            
            # Show matched content if available
            if result.get('matched_fields'):
                response_parts.append(f"   🎯 Matched in: {', '.join(result['matched_fields'])}")
        
        # Data type breakdown
        type_counts = {}
        location_counts = {}
        
        for result in results:
            data_type = result['type']
            type_counts[data_type] = type_counts.get(data_type, 0) + 1
            
            location = result['location']
            if location != 'Unknown, Unknown':
                location_counts[location] = location_counts.get(location, 0) + 1
        
        if type_counts:
            response_parts.append("\n📊 **Data Types Found:**")
            for dtype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
                icon = {'text': '📝', 'audio': '🎵', 'video': '🎥', 'image': '🖼️'}.get(dtype, '📄')
                response_parts.append(f"   {icon} {dtype.title()}: {count} items")
        
        if location_counts:
            response_parts.append("\n🌍 **Top Locations:**")
            for location, count in list(sorted(location_counts.items(), key=lambda x: x[1], reverse=True))[:3]:
                response_parts.append(f"   📍 {location}: {count} items")
        
        # Additional suggestions
        if search_results['found_items'] > 5:
            response_parts.append(f"\n💡 **Note**: Showing top 5 of {search_results['found_items']} total matches. You can view all data in the 'View Collected Data' section.")
        
        response_parts.append("\n🔍 **Need more specific info?** Try asking about particular locations, dates, or data types!")
        
        return "\n".join(response_parts)
    
    def get_chatbot_suggestions(self) -> List[str]:
        """Generate helpful query suggestions based on database content"""
        df = self.load_database_content()
        
        suggestions = [
            "Show me all images collected",
            "What audio recordings do you have?",
            "Tell me about data from Mumbai",
            "Show me recent collections",
            "What types of data have been collected?"
        ]
        
        if df is not None and len(df) > 0:
            # Add location-based suggestions
            locations = df[df['city'].notna()]['city'].unique()[:3]
            for location in locations:
                suggestions.append(f"Show me data from {location}")
            
            # Add category-based suggestions
            categories = df[df['category'].notna()]['category'].unique()[:3]
            for category in categories:
                suggestions.append(f"Tell me about {category} data")
        
        return suggestions[:8]  # Limit to 8 suggestions
    
    def process_query(self, user_query: str) -> str:
        """Main method to process user queries and generate responses"""
        if not user_query or len(user_query.strip()) < 3:
            return "🤖 Please ask me a question about the flora and fauna data! For example: 'Show me images from Mumbai' or 'What audio recordings do you have?'"
        
        # Extract keywords and search database
        keywords = self.extract_keywords(user_query)
        search_results = self.search_database(user_query, keywords)
        
        # Generate response
        response = self.generate_response(user_query, search_results)
        
        # Store conversation
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'query': user_query,
            'keywords': keywords,
            'results_found': search_results['found_items'],
            'response': response
        })
        
        # Limit conversation history
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-25:]
        
        return response

def render_chatbot_interface():
    """Render the chatbot interface in Streamlit"""
    
    st.header("🤖 Flora & Fauna AI Assistant")
    st.markdown("*Ask me anything about your collected flora and fauna data!*")
    
    # Check database availability
    if not SUPABASE_AVAILABLE:
        st.error("❌ Database connection not available. Please check your Supabase setup.")
        return
    
    # Initialize chatbot in session state if not already present
    if 'flora_chatbot' not in st.session_state:
        try:
            st.session_state.flora_chatbot = FloraFaunaChatbot()
        except Exception as e:
            st.error(f"❌ Failed to initialize chatbot: {str(e)}")
            return
    
    chatbot = st.session_state.flora_chatbot
    
    # Quick suggestions
    st.markdown("### 💡 Try asking:")
    try:
        suggestions = chatbot.get_chatbot_suggestions()
    except Exception as e:
        st.warning(f"⚠️ Could not load suggestions: {str(e)}")
        suggestions = [
            "Show me all images collected",
            "What audio recordings do you have?",
            "Tell me about data from Mumbai",
            "Show me recent collections"
        ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(f"💬 {suggestion}", key=f"suggestion_{i}"):
                st.session_state.chatbot_query = suggestion
                st.rerun()
    
    st.markdown("---")
    
    # Chat interface
    with st.container():
        st.markdown("### 💬 Ask Your Question")
        
        # Query input
        query = st.text_input(
            "Your question:",
            value=st.session_state.get('chatbot_query', ''),
            placeholder="e.g., 'Show me all images from Mumbai' or 'What audio data do you have?'",
            key="chatbot_input"
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            ask_button = st.button("🚀 Ask", type="primary")
        
        with col2:
            clear_button = st.button("🗑️ Clear")
        
        # Process query
        if ask_button and query:
            with st.spinner("🔍 Searching database..."):
                try:
                    response = chatbot.process_query(query)
                    st.session_state.chatbot_response = response
                    st.session_state.chatbot_query = ""
                except Exception as e:
                    st.error(f"❌ Error processing query: {str(e)}")
                    st.session_state.chatbot_response = "Sorry, I encountered an error while processing your query. Please try again or rephrase your question."
        
        if clear_button:
            st.session_state.chatbot_query = ""
            st.session_state.chatbot_response = ""
            st.rerun()
    
    # Display response
    if st.session_state.get('chatbot_response'):
        st.markdown("---")
        st.markdown("### 🤖 Assistant Response")
        st.markdown(st.session_state.chatbot_response)
    
    # Conversation history (collapsible)
    if chatbot.conversation_history:
        with st.expander(f"📜 Conversation History ({len(chatbot.conversation_history)} queries)"):
            for i, conv in enumerate(reversed(chatbot.conversation_history[-10:]), 1):
                st.markdown(f"**{i}. Q:** {conv['query']}")
                st.markdown(f"**A:** Found {conv['results_found']} results")
                st.caption(f"Asked: {conv['timestamp'][:19]}")
                st.markdown("---")

if __name__ == "__main__":
    render_chatbot_interface()
