/**
 * Configuration file for Flora & Fauna Frontend
 * Update these values with your actual Supabase credentials
 */

// Supabase Configuration
// Replace these with your actual Supabase project credentials
const SUPABASE_CONFIG = {
    // Your Supabase project URL (found in your Supabase dashboard)
    url: 'https://your-project-ref.supabase.co',
    
    // Your Supabase anon/public key (found in your Supabase dashboard -> Settings -> API)
    anonKey: 'your-anon-key-here',
    
    // Table name (should match your existing table)
    tableName: 'data_entries'
};

// Database Schema
// This is the expected structure of your data_entries table
const EXPECTED_SCHEMA = {
    id: 'Primary key (auto-generated)',
    entry_type: 'Text - type of entry (image, video, audio, text)',
    title: 'Text - title/name of the entry',
    content: 'Text - content/description',
    file_path: 'Text - local file path reference',
    file_url: 'Text - Supabase storage public URL',
    timestamp: 'Timestamp - when the entry was created',
    location_lat: 'Numeric - latitude coordinate',
    location_lng: 'Numeric - longitude coordinate', 
    location_name: 'Text - human-readable location name',
    metadata: 'JSON - additional metadata'
};

// Configuration Instructions
const SETUP_INSTRUCTIONS = `
To set up your Supabase connection:

1. Create a Supabase project at https://supabase.com
2. Create a table called 'data_entries' with the schema defined above
3. Set up Row Level Security (RLS) policies if needed
4. Create storage buckets for: images, videos, audios, texts
5. Get your project URL and anon key from Settings -> API
6. Update the SUPABASE_CONFIG values above
7. Open index.html in your browser

For the Streamlit integration:
- Make sure your .streamlit/secrets.toml file has the same credentials
- The frontend will automatically work with data created via the Streamlit app

Storage Buckets Required:
- images (for image files)
- videos (for video files)  
- audios (for audio files)
- texts (for text files)

Table Creation SQL:
CREATE TABLE data_entries (
    id BIGSERIAL PRIMARY KEY,
    entry_type TEXT NOT NULL,
    title TEXT,
    content TEXT,
    file_path TEXT,
    file_url TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    location_lat NUMERIC,
    location_lng NUMERIC,
    location_name TEXT,
    metadata JSONB
);
`;

// Export configuration
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        SUPABASE_CONFIG,
        EXPECTED_SCHEMA,
        SETUP_INSTRUCTIONS
    };
} else {
    // Browser environment
    window.SUPABASE_CONFIG = SUPABASE_CONFIG;
    window.EXPECTED_SCHEMA = EXPECTED_SCHEMA;
    window.SETUP_INSTRUCTIONS = SETUP_INSTRUCTIONS;
}