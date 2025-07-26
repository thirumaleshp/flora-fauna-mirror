import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'

/**
 * Custom hook to fetch posts from Supabase
 * Assumes you have a 'posts' table with columns: id, title, content, created_at
 * 
 * To create the posts table in your Supabase database, run this SQL:
 * 
 * CREATE TABLE posts (
 *   id SERIAL PRIMARY KEY,
 *   title VARCHAR(255) NOT NULL,
 *   content TEXT,
 *   created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
 * );
 * 
 * -- Insert some sample data
 * INSERT INTO posts (title, content) VALUES
 * ('Welcome to our homepage', 'This is our first post showcasing the Supabase integration.'),
 * ('React + Supabase = Amazing', 'Building modern web apps has never been easier with this powerful combination.'),
 * ('Getting Started Guide', 'Follow our comprehensive guide to set up your own project like this one.');
 */

export const usePosts = () => {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true)
        setError(null)
        
        const { data, error } = await supabase
          .from('posts')
          .select('*')
          .order('created_at', { ascending: false })

        if (error) {
          throw error
        }

        setPosts(data || [])
      } catch (err) {
        console.error('Error fetching posts:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchPosts()
  }, [])

  return { posts, loading, error }
}