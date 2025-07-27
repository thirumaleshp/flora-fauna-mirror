"""
Flora & Fauna Chatbot - Stage 2
Database-powered conversational AI for flora and fauna queries
"""

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
            print(f"Error loading database: {str(e)}")  # Log error without streamlit dependency
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
    
    # Import streamlit only when needed for UI rendering
    import streamlit as st
    
    # Apply custom CSS for a modern interface
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    .main-header {
        text-align: center;
        padding: 3rem 0 1rem 0;
        font-size: 2.8rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .sub-header {
        text-align: center;
        color: #E5E7EB;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 400;
        opacity: 0.9;
    }
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    .input-section {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    .response-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #60A5FA;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        font-size: 1.1rem;
        padding: 12px 16px;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }
    .stMarkdown h3 {
        color: white;
        font-weight: 600;
    }
    .stExpander {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center-aligned header
    st.markdown('<div class="main-header">Hello, Thirumalesh</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ask me anything about your flora and fauna data</div>', unsafe_allow_html=True)
    
    # Check database availability
    if not SUPABASE_AVAILABLE:
        st.error("❌ Database connection not available. Please check your Supabase setup.")
        return
    
    # Safely initialize session state variables
    try:
        # Initialize chatbot in session state if not already present
        if 'flora_chatbot' not in st.session_state:
            st.session_state.flora_chatbot = FloraFaunaChatbot()
        
        # Initialize other session state variables safely
        if 'chatbot_query' not in st.session_state:
            st.session_state.chatbot_query = ""
        if 'chatbot_response' not in st.session_state:
            st.session_state.chatbot_response = ""
            
        chatbot = st.session_state.flora_chatbot
        
    except Exception as e:
        st.error(f"❌ Failed to initialize chatbot: {str(e)}")
        st.markdown("Please refresh the page and try again.")
        return
    
    # Create centered container for chat interface
    with st.container():
        # Quick suggestions with modern styling
        st.markdown("### 💡 Quick suggestions")
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
        
        # Display suggestions in a more modern way
        cols = st.columns(2)
        for i, suggestion in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(suggestion, key=f"suggestion_{i}", help="Click to use this suggestion"):
                    try:
                        st.session_state.chatbot_query = suggestion
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error setting suggestion: {str(e)}")
        
        st.markdown("---")
        
        # Main chat input with modern styling
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        
        # Query input with better styling
        query = st.text_input(
            "",
            value=st.session_state.get('chatbot_query', ''),
            placeholder="Ask me anything about your flora and fauna data...",
            key="chatbot_input",
            label_visibility="collapsed"
        )
        
        # Action buttons with better layout
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
        
        with col2:
            ask_button = st.button("🚀 Ask", type="primary", use_container_width=True)
        
        with col3:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process query with better UX
        if ask_button and query:
            with st.spinner("🔍 Searching your flora and fauna database..."):
                try:
                    response = chatbot.process_query(query)
                    st.session_state.chatbot_response = response
                    st.session_state.chatbot_query = ""
                except Exception as e:
                    st.error(f"❌ Error processing query: {str(e)}")
                    st.session_state.chatbot_response = "Sorry, I encountered an error while processing your query. Please try again or rephrase your question."
        
        if clear_button:
            try:
                st.session_state.chatbot_query = ""
                st.session_state.chatbot_response = ""
                st.rerun()
            except Exception as e:
                st.error(f"Error clearing chat: {str(e)}")
    
    # Display response with modern styling
    try:
        if st.session_state.get('chatbot_response'):
            st.markdown('<div class="response-container">', unsafe_allow_html=True)
            st.markdown("### 🤖 Assistant Response")
            st.markdown(st.session_state.chatbot_response)
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error displaying response: {str(e)}")
    
    # Conversation history with improved design
    try:
        if chatbot.conversation_history:
            with st.expander(f"📜 Recent Conversations ({len(chatbot.conversation_history)} total)", expanded=False):
                for i, conv in enumerate(reversed(chatbot.conversation_history[-5:]), 1):
                    st.markdown(f"**Q{i}:** {conv['query']}")
                    st.markdown(f"**A{i}:** Found {conv['results_found']} results")
                    st.caption(f"🕒 {conv['timestamp'][:19]}")
                    if i < len(chatbot.conversation_history[-5:]):
                        st.markdown("---")
    except Exception as e:
        st.warning(f"Error displaying conversation history: {str(e)}")

if __name__ == "__main__":
    render_chatbot_interface()
