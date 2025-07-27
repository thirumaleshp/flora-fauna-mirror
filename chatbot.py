"""
Flora & Fauna Chatbot - Stage 2
Database-powered conversational AI for flora and fauna queries
"""

# Import required modules with error handling
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    import warnings
    warnings.warn("pandas not available - chatbot functionality will be limited")

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
        
    def load_database_content(self) -> Optional[object]:
        """Load and cache database content for faster queries"""
        try:
            if not SUPABASE_AVAILABLE or not PANDAS_AVAILABLE:
                return None
                
            current_time = datetime.now()
            
            # Cache data for 5 minutes to improve performance
            if (self.db_cache is None or 
                self.last_cache_update is None or 
                (current_time - self.last_cache_update).seconds > 300):
                
                self.db_cache = supabase_manager.get_all_data()
                self.last_cache_update = current_time
                
            return self.db_cache
            
        except Exception:
            return None
    
    def extract_keywords(self, query: str) -> List[str]:
        """Extract relevant keywords from user query with multilingual support"""
        # Remove common words and extract meaningful terms
        stop_words = {
            # English stop words
            'the', 'is', 'at', 'which', 'on', 'what', 'where', 'when', 'how', 'why', 'who', 
            'a', 'an', 'and', 'or', 'but', 'in', 'of', 'to', 'for', 'with', 'by', 'me', 'show',
            'tell', 'about', 'from', 'all', 'any', 'some', 'data', 'information',
            # Telugu common words (basic ones)
            'అని', 'కి', 'ను', 'లో', 'నా', 'మా', 'వాళ్ళ', 'గురించి', 'చెప్పు'
        }
        
        # Clean and split query - preserve Telugu characters
        query_clean = re.sub(r'[^\w\s\u0C00-\u0C7F]', ' ', query.lower())
        words = [word.strip() for word in query_clean.split() if len(word.strip()) > 1]
        
        # Filter out stop words
        keywords = [word for word in words if word not in stop_words]
        
        # Add the full query for exact matching
        keywords.append(query.lower().strip())
        
        # Enhanced bilingual keyword mapping
        query_variations = []
        query_lower = query.lower()
        
        # Plant/tree translations
        plant_translations = {
            'jammi': ['jammi', 'జమ్మి', 'prosopis', 'cineraria', 'shami', 'khejri'],
            'జమ్మి': ['jammi', 'జమ్మి', 'prosopis', 'cineraria', 'shami', 'khejri'],
            'prosopis': ['jammi', 'జమ్మి', 'prosopis', 'cineraria'],
            'shami': ['jammi', 'జమ్మి', 'shami', 'prosopis'],
            'neem': ['neem', 'వేప', 'vepa', 'azadirachta', 'indica', 'margosa'],
            'వేప': ['neem', 'వేప', 'vepa', 'azadirachta', 'indica', 'margosa'],
            'vepa': ['neem', 'వేప', 'vepa', 'azadirachta', 'indica'],
            'azadirachta': ['neem', 'వేప', 'azadirachta', 'indica'],
            'banyan': ['banyan', 'మర్రి', 'marri', 'ficus', 'benghalensis', 'vat', 'bargad'],
            'మర్రి': ['banyan', 'మర్రి', 'marri', 'ficus', 'benghalensis'],
            'marri': ['banyan', 'మర్రి', 'marri', 'ficus'],
            'peepal': ['peepal', 'రావి', 'ravi', 'ficus', 'religiosa', 'bodhi'],
            'రావి': ['peepal', 'రావి', 'ravi', 'ficus', 'religiosa'],
            'bodhi': ['peepal', 'రావి', 'bodhi', 'ficus', 'religiosa'],
            'mango': ['mango', 'మామిడి', 'mamidi', 'mangifera', 'indica', 'aam'],
            'మామిడి': ['mango', 'మామిడి', 'mamidi', 'mangifera', 'indica'],
            'mamidi': ['mango', 'మామిడి', 'mamidi', 'mangifera'],
            'coconut': ['coconut', 'కొబ్బరి', 'kobbari', 'cocos', 'nucifera', 'nariyal'],
            'కొబ్బరి': ['coconut', 'కొబ్బరి', 'kobbari', 'cocos', 'nucifera'],
            'kobbari': ['coconut', 'కొబ్బరి', 'kobbari', 'cocos'],
        }
        
        # Add plant-specific translations
        for word in keywords:
            if word in plant_translations:
                query_variations.extend(plant_translations[word])
        
        # Generic tree/plant keywords with translations
        tree_keywords = ['చెట్టు', 'tree', 'plant', 'వృక్షం', 'మొక్క']
        if any(keyword in query_lower for keyword in tree_keywords):
            query_variations.extend(tree_keywords)
        
        # Media request keywords with translations
        media_keywords = {
            'image': ['image', 'images', 'photo', 'picture', 'చిత్రం', 'ఫోటో'],
            'images': ['image', 'images', 'photo', 'picture', 'చిత్రాలు', 'ఫోటోలు'],
            'photo': ['image', 'images', 'photo', 'picture', 'చిత్రం', 'ఫోటో'],
            'picture': ['image', 'images', 'photo', 'picture', 'చిత్రం', 'ఫోటో'],
            'చిత్రం': ['image', 'images', 'photo', 'picture', 'చిత్రం', 'ఫోటో'],
            'ఫోటో': ['image', 'images', 'photo', 'picture', 'చిత్రం', 'ఫోటో'],
            'video': ['video', 'videos', 'వీడియో'],
            'వీడియో': ['video', 'videos', 'వీడియో'],
            'audio': ['audio', 'sound', 'recording', 'ఆడియో', 'శబ్దం'],
            'ఆడియో': ['audio', 'sound', 'recording', 'ఆడియో', 'శబ్దం'],
        }
        
        for word in keywords:
            if word in media_keywords:
                query_variations.extend(media_keywords[word])
        
        # Location translations
        location_keywords = {
            'mumbai': ['mumbai', 'bombay', 'ముంబై'],
            'ముంబై': ['mumbai', 'bombay', 'ముంబై'],
            'delhi': ['delhi', 'దిల్లీ'],
            'దిల్లీ': ['delhi', 'దిల్లీ'],
            'bangalore': ['bangalore', 'bengaluru', 'బెంగళూరు'],
            'బెంగళూరు': ['bangalore', 'bengaluru', 'బెంగళూరు'],
            'hyderabad': ['hyderabad', 'హైదరాబాద్'],
            'హైదరాబాద్': ['hyderabad', 'హైదరాబాద్'],
        }
        
        for word in keywords:
            if word in location_keywords:
                query_variations.extend(location_keywords[word])
        
        # Common action verbs in both languages
        action_keywords = {
            'show': ['show', 'display', 'చూపించు', 'తెలియజేయి'],
            'చూపించు': ['show', 'display', 'చూపించు'],
            'tell': ['tell', 'చెప్పు', 'తెలియజేయి'],
            'చెప్పు': ['tell', 'చెప్పు', 'తెలియజేయి'],
        }
        
        for word in keywords:
            if word in action_keywords:
                query_variations.extend(action_keywords[word])
        
        keywords.extend(query_variations)
        
        return list(set(keywords))  # Remove duplicates
    
    def search_database(self, query: str, keywords: List[str]) -> Dict:
        """Search database for relevant content with improved matching"""
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
        for idx, row in df.iterrows():
            relevance_score = 0
            matched_fields = []
            matched_content = []
            
            # Create searchable text from all fields
            all_text_fields = []
            for col in search_columns:
                if col in row and pd.notna(row[col]) and str(row[col]).strip():
                    all_text_fields.append(str(row[col]))
            
            combined_text = " ".join(all_text_fields).lower()
            
            # Check each keyword with enhanced matching
            for keyword in keywords:
                keyword_lower = keyword.lower()
                
                # Exact match gets highest score
                if keyword_lower in combined_text:
                    relevance_score += 5
                    matched_content.append(f"Found '{keyword}' in record")
                
                # Check individual columns for more specific matches
                for col in search_columns:
                    if col in row and pd.notna(row[col]):
                        content = str(row[col]).lower()
                        if keyword_lower in content:
                            relevance_score += 2
                            if col not in matched_fields:
                                matched_fields.append(col)
                
                # Enhanced partial matching for bilingual content
                if len(keyword_lower) > 2:
                    # Word boundary matching
                    for text_chunk in combined_text.split():
                        # Exact word match
                        if keyword_lower == text_chunk:
                            relevance_score += 4
                        # Partial match (contains)
                        elif keyword_lower in text_chunk or text_chunk in keyword_lower:
                            relevance_score += 1
                    
                    # Fuzzy matching for transliterations (e.g., jammi/జమ్మి)
                    # Check if any word in the text sounds similar or is a transliteration
                    for text_word in combined_text.split():
                        if len(text_word) > 2:
                            # Simple similarity check based on common characters
                            common_chars = set(keyword_lower) & set(text_word)
                            if len(common_chars) >= min(3, len(keyword_lower) - 1):
                                relevance_score += 1
            
            # Boost score if multiple keywords match
            if len([k for k in keywords if k.lower() in combined_text]) > 1:
                relevance_score += 2
            
            # Give extra boost to media files if user is asking for images/videos/audio (bilingual)
            entry_type = row.get('entry_type', '')
            if entry_type in ['image', 'video', 'audio']:
                # Check if user is asking for media in English or Telugu
                media_request_keywords = [
                    'image', 'images', 'photo', 'picture', 'చిత్రం', 'చిత్రాలు', 'ఫోటో', 'ఫోటోలు',
                    'video', 'videos', 'వీడియో', 'వీడియోలు',
                    'audio', 'sound', 'recording', 'ఆడియో', 'శబ్దం'
                ]
                for media_keyword in media_request_keywords:
                    if media_keyword in query.lower():
                        relevance_score += 10  # Big boost for media files when user asks for media
                        break
            
            # If relevant, add to results
            if relevance_score > 0:
                result_item = {
                    'relevance': relevance_score,
                    'data': row.to_dict(),
                    'matched_fields': matched_fields,
                    'matched_content': matched_content,
                    'type': row.get('entry_type', 'unknown'),
                    'title': row.get('title', 'Unknown'),
                    'description': row.get('description', 'No description'),
                    'content': row.get('content', 'No content'),
                    'location': f"{row.get('city', 'Unknown')}, {row.get('country', 'Unknown')}",
                    'timestamp': row.get('timestamp', 'Unknown'),
                    'combined_text': combined_text[:200] + "..." if len(combined_text) > 200 else combined_text
                }
                results.append(result_item)
        
        # Sort by relevance score
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        return {
            'found_items': len(results),
            'results': results[:10],  # Limit to top 10 results
            'total_items': len(df),
            'keywords_used': keywords,
            'message': f"Found {len(results)} relevant items from {len(df)} total records."
        }
    
    def generate_response_with_media(self, query: str, search_results: Dict) -> Dict:
        """Generate natural language response with media files based on search results"""
        
        if search_results['found_items'] == 0:
            return {
                'text_response': f"""
🤖 **Flora & Fauna Assistant**: I couldn't find any information about '{query}' in our database.

💡 **Suggestions:**
- Try using simpler keywords (e.g., 'jammi', 'tree', 'plant')
- Ask about specific locations, species, or data types
- Try English keywords if you used Telugu, or vice versa
""",
                'media_files': []
            }

        results = search_results['results']
        
        # Find the most relevant result that actually matches the query
        best_match = None
        query_lower = query.lower().strip()
        
        # Look for the best matching result
        for result in results:
            content = result.get('content', '').lower()
            description = result.get('description', '').lower()
            title = result.get('title', '').lower()
            
            # Check if this result specifically mentions what user asked about
            combined_text = f"{title} {description} {content}"
            
            # Score based on direct keyword matches
            relevance_score = 0
            for keyword in query_lower.split():
                if len(keyword) > 2:  # Skip very short words
                    if keyword in combined_text:
                        relevance_score += len(keyword)  # Longer matches get higher scores
            
            if relevance_score > 0:
                result['calculated_relevance'] = relevance_score
                if best_match is None or relevance_score > best_match.get('calculated_relevance', 0):
                    best_match = result
        
        # If no specific match found, use the first result
        if best_match is None:
            best_match = results[0]
        
        # Collect media files from relevant results
        media_files = []
        
        for result in results:
            result_data = result.get('data', {})
            entry_type = result_data.get('entry_type', '')
            file_url = result_data.get('file_url', '')
            title = result_data.get('title', 'Unknown')
            description = result.get('description', '')
            
            if file_url and entry_type in ['image', 'video', 'audio']:
                is_relevant = False
                
                # Check title and description for relevance
                combined_media_text = f"{title.lower()} {description.lower()}"
                for keyword in query_lower.split():
                    if len(keyword) > 2 and keyword in combined_media_text:
                        is_relevant = True
                        break
                
                # Check for plant/tree specific keywords
                tree_keywords = [
                    'jammi', 'జమ్మి', 'prosopis', 'shami',
                    'neem', 'వేప', 'vepa', 'azadirachta',
                    'banyan', 'మర్రి', 'marri', 'ficus',
                    'mango', 'మామిడి', 'mamidi',
                    'coconut', 'కొబ్బరి', 'kobbari',
                    'tree', 'చెట్టు', 'plant', 'వృక్షం', 'మొక్క'
                ]
                for tree_keyword in tree_keywords:
                    if tree_keyword in combined_media_text:
                        is_relevant = True
                        break
                
                # Include if relevant or in top 5 results
                if is_relevant or results.index(result) < 5:
                    media_info = {
                        'type': entry_type,
                        'url': file_url,
                        'title': title,
                        'description': description[:100] + "..." if len(description) > 100 else description,
                        'relevance': result.get('relevance', 0)
                    }
                    media_files.append(media_info)
        
        # Sort media files by relevance
        media_files.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        
        # Generate response from the best match
        content = best_match.get('content', '')
        description = best_match.get('description', '')
        
        response_parts = []
        
        if description and description != 'No description':
            clean_description = description.strip()
            if clean_description:
                response_parts.append(clean_description)
        
        if content and content != 'No content' and content != description:
            clean_content = content.strip()
            if clean_content:
                response_parts.append(clean_content)
        
        # If no content, try other results
        if not response_parts:
            for result in results[:2]:
                alt_description = result.get('description', '')
                alt_content = result.get('content', '')
                
                if alt_description and alt_description != 'No description':
                    response_parts.append(alt_description.strip())
                    break
                elif alt_content and alt_content != 'No content':
                    response_parts.append(alt_content.strip())
                    break
        
        # Generate final response
        if response_parts:
            text_response = '\n\n'.join(response_parts)
            if len(text_response) > 1500:
                text_response = text_response[:1500] + "..."
        else:
            text_response = "🤖 **Flora & Fauna Assistant**: I found records, but no detailed information is available for your query."
        
        return {
            'text_response': text_response,
            'media_files': media_files
        }
    
    def generate_response(self, query: str, search_results: Dict) -> str:
        """Generate natural language response based on search results (backward compatibility)"""
        response_data = self.generate_response_with_media(query, search_results)
        return response_data['text_response']
    
    def process_query_with_media(self, user_query: str) -> Dict:
        """Main method to process user queries and generate responses with media files"""
        if not user_query or len(user_query.strip()) < 3:
            return {
                'text_response': "🤖 Please ask me a question about the flora and fauna data!",
                'media_files': []
            }
        
        # Extract keywords and search database
        keywords = self.extract_keywords(user_query)
        search_results = self.search_database(user_query, keywords)
        
        # Generate response with media
        response_data = self.generate_response_with_media(user_query, search_results)
        
        # Store conversation
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'query': user_query,
            'keywords': keywords,
            'results_found': search_results['found_items'],
            'text_response': response_data['text_response'],
            'media_count': len(response_data['media_files'])
        })
        
        # Limit conversation history
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-25:]
        
        return response_data
    
    def process_query(self, user_query: str) -> str:
        """Main method to process user queries and generate responses"""
        if not user_query or len(user_query.strip()) < 3:
            return "🤖 Please ask me a question about the flora and fauna data!"
        
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

def render_media_files(media_files: list):
    """Render media files in the Streamlit interface"""
    import streamlit as st
    
    if not media_files:
        return
    
    st.markdown("### 📁 Related Media Files")
    
    # Group media by type
    media_by_type = {
        'image': [],
        'video': [],
        'audio': []
    }
    
    for media in media_files:
        media_type = media.get('type', 'unknown')
        if media_type in media_by_type:
            media_by_type[media_type].append(media)
    
    # Display images
    if media_by_type['image']:
        st.markdown("#### 🖼️ Images")
        cols = st.columns(min(3, len(media_by_type['image'])))
        for i, img in enumerate(media_by_type['image']):
            with cols[i % 3]:
                try:
                    st.image(img['url'], caption=img['title'], use_column_width=True)
                    if img['description']:
                        st.caption(img['description'])
                except Exception:
                    st.error(f"❌ Could not display image: {img['title']}")
                    st.markdown(f"🔗 [View directly]({img['url']})")
    
    # Display videos
    if media_by_type['video']:
        st.markdown("#### 🎥 Videos")
        for video in media_by_type['video']:
            try:
                st.video(video['url'])
                st.markdown(f"**{video['title']}**")
                if video['description']:
                    st.caption(video['description'])
            except Exception:
                st.error(f"❌ Could not display video: {video['title']}")
                st.markdown(f"🔗 [Download video]({video['url']})")
    
    # Display audio
    if media_by_type['audio']:
        st.markdown("#### 🎵 Audio")
        for audio in media_by_type['audio']:
            try:
                st.audio(audio['url'])
                st.markdown(f"**{audio['title']}**")
                if audio['description']:
                    st.caption(audio['description'])
            except Exception:
                st.error(f"❌ Could not play audio: {audio['title']}")
                st.markdown(f"🔗 [Download audio]({audio['url']})")

def render_chatbot_interface():
    """Render the chatbot interface in Streamlit"""
    
    # Import streamlit only when needed for UI rendering
    import streamlit as st
    
    st.header("🤖 Flora & Fauna AI Assistant")
    st.markdown("*Ask me anything about your collected flora and fauna data!*")
    
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
        if 'chatbot_response_data' not in st.session_state:
            st.session_state.chatbot_response_data = None
            
        chatbot = st.session_state.flora_chatbot
        
    except Exception as e:
        st.error(f"❌ Failed to initialize chatbot: {str(e)}")
        st.markdown("Please refresh the page and try again.")
        return
    
    # Chat interface
    with st.container():
        st.markdown("### 💬 Ask Your Question")
        
        # Query input
        query = st.text_input(
            "Your question:",
            value=st.session_state.get('chatbot_query', ''),
            placeholder="e.g., 'Show me images from Mumbai' or 'జమ్మి చెట్టు చిత్రాలు'",
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
                    response_data = chatbot.process_query_with_media(query)
                    st.session_state.chatbot_response_data = response_data
                    st.session_state.chatbot_query = ""
                except Exception as e:
                    st.error(f"❌ Error processing query: {str(e)}")
                    st.session_state.chatbot_response_data = {
                        'text_response': "Sorry, I encountered an error while processing your query. Please try again or rephrase your question.",
                        'media_files': []
                    }
        
        if clear_button:
            try:
                st.session_state.chatbot_query = ""
                st.session_state.chatbot_response_data = None
                st.rerun()
            except Exception as e:
                st.error(f"Error clearing chat: {str(e)}")
    
    # Display response with media
    try:
        if st.session_state.get('chatbot_response_data'):
            response_data = st.session_state.chatbot_response_data
            
            st.markdown("---")
            st.markdown("### 🤖 Assistant Response")
            st.markdown(response_data['text_response'])
            
            # Display related media files
            if response_data.get('media_files'):
                render_media_files(response_data['media_files'])
                
    except Exception as e:
        st.error(f"Error displaying response: {str(e)}")
    
    # Conversation history (collapsible)
    try:
        if chatbot.conversation_history:
            with st.expander(f"📜 Conversation History ({len(chatbot.conversation_history)} queries)"):
                for i, conv in enumerate(reversed(chatbot.conversation_history[-10:]), 1):
                    st.markdown(f"**{i}. Q:** {conv['query']}")
                    results_found = conv.get('results_found', 0)
                    media_count = conv.get('media_count', 0)
                    st.markdown(f"**A:** Found {results_found} results ({media_count} media files)")
                    st.caption(f"Asked: {conv['timestamp'][:19]}")
                    st.markdown("---")
    except Exception as e:
        st.warning(f"Error displaying conversation history: {str(e)}")

if __name__ == "__main__":
    render_chatbot_interface()
