import { usePosts } from '../hooks/usePosts'

const PostsSection = () => {
  const { posts, loading, error } = usePosts()

  if (loading) {
    return (
      <section id="posts" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-12">
              Latest Posts
            </h2>
            <div className="flex justify-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
            <p className="mt-4 text-gray-600">Loading posts from Supabase...</p>
          </div>
        </div>
      </section>
    )
  }

  if (error) {
    return (
      <section id="posts" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-12">
              Latest Posts
            </h2>
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
              <div className="flex items-center">
                <svg className="w-6 h-6 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L2.732 14.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
                <div>
                  <h3 className="text-red-800 font-semibold">Connection Error</h3>
                  <p className="text-red-600 text-sm mt-1">{error}</p>
                </div>
              </div>
              <div className="mt-4 text-sm text-gray-600">
                <p>Make sure you have:</p>
                <ul className="list-disc list-inside mt-2 text-left">
                  <li>Created a .env file with your Supabase credentials</li>
                  <li>Created a 'posts' table in your Supabase database</li>
                  <li>Added some sample data to the posts table</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>
    )
  }

  return (
    <section id="posts" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Latest Posts
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Explore our latest content fetched directly from our Supabase database
          </p>
        </div>

        {posts.length === 0 ? (
          <div className="text-center">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-8 max-w-md mx-auto">
              <svg className="w-12 h-12 text-blue-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No Posts Found</h3>
              <p className="text-gray-600 mb-4">
                Your posts table is empty. Add some sample data to see posts here!
              </p>
              <div className="text-sm text-left bg-white p-4 rounded border">
                <p className="font-semibold mb-2">Run this SQL in your Supabase dashboard:</p>
                <code className="text-xs text-gray-700 block">
                  INSERT INTO posts (title, content) VALUES<br/>
                  ('Welcome Post', 'This is your first post!'),<br/>
                  ('Another Post', 'Here's some more content.');
                </code>
              </div>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {posts.map((post) => (
              <article key={post.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
                <div className="p-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-3 line-clamp-2">
                    {post.title}
                  </h3>
                  <p className="text-gray-600 mb-4 line-clamp-3">
                    {post.content}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">
                      {new Date(post.created_at).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </span>
                    <button className="text-blue-600 hover:text-blue-800 font-medium text-sm transition-colors">
                      Read More →
                    </button>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}

        {/* Connection Status */}
        <div className="mt-12 text-center">
          <div className="inline-flex items-center bg-green-50 border border-green-200 rounded-lg px-4 py-2">
            <svg className="w-4 h-4 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
            </svg>
            <span className="text-green-800 text-sm font-medium">Connected to Supabase</span>
          </div>
        </div>
      </div>
    </section>
  )
}

export default PostsSection