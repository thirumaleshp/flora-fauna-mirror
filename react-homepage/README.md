# React + Supabase Modern Homepage

A beautiful, modern, and responsive homepage built with React, Vite, Tailwind CSS, and Supabase. This project demonstrates best practices for building modern web applications with real-time database integration.

## 🚀 Features

- **Modern React**: Built with React 18 and functional components
- **Lightning Fast**: Powered by Vite for instant development and optimized builds
- **Responsive Design**: Mobile-first design using Tailwind CSS
- **Database Integration**: Real-time data fetching from Supabase
- **Modern UI**: Clean, professional design with smooth animations
- **SEO Friendly**: Semantic HTML structure
- **Accessible**: Built with accessibility best practices

## 🛠️ Tech Stack

- **Frontend**: React 18, Vite
- **Styling**: Tailwind CSS
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Ready for Vercel, Netlify, or any static hosting

## 📋 Prerequisites

Before you begin, ensure you have:

- Node.js 16+ installed
- A Supabase account (free tier available)
- Basic knowledge of React and JavaScript

## 🚀 Quick Start

### 1. Clone and Install

```bash
# Clone the repository
git clone <your-repo-url>
cd react-homepage

# Install dependencies
npm install
```

### 2. Set Up Supabase

1. Go to [Supabase](https://supabase.com) and create a new project
2. Wait for the database to be set up
3. Go to Settings > API in your Supabase dashboard
4. Copy your project URL and anon key

### 3. Create Environment File

Create a `.env` file in the root directory:

```env
VITE_SUPABASE_URL=your_supabase_project_url_here
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

### 4. Set Up Database Table

In your Supabase SQL editor, run this query to create the posts table:

```sql
-- Create posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  content TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert sample data
INSERT INTO posts (title, content) VALUES
('Welcome to our homepage', 'This is our first post showcasing the Supabase integration.'),
('React + Supabase = Amazing', 'Building modern web apps has never been easier with this powerful combination.'),
('Getting Started Guide', 'Follow our comprehensive guide to set up your own project like this one.');

-- Enable Row Level Security (optional, for production)
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Create a policy to allow public read access
CREATE POLICY "Posts are publicly readable" ON posts
  FOR SELECT USING (true);
```

### 5. Run the Development Server

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) to view the application.

## 📁 Project Structure

```
react-homepage/
├── src/
│   ├── components/          # React components
│   │   ├── Navbar.jsx      # Navigation bar
│   │   ├── Hero.jsx        # Hero section
│   │   ├── PostsSection.jsx # Posts display
│   │   └── Footer.jsx      # Footer
│   ├── hooks/              # Custom React hooks
│   │   └── usePosts.js     # Hook for fetching posts
│   ├── lib/                # Utility libraries
│   │   └── supabase.js     # Supabase client configuration
│   ├── App.jsx             # Main App component
│   ├── main.jsx           # Application entry point
│   └── index.css          # Global styles
├── .env.example           # Environment variables template
├── package.json
└── README.md
```

## 🎨 Customization

### Change App Name and Branding

1. Update the app name in `src/components/Navbar.jsx`:
```jsx
<h1 className="text-2xl font-bold text-gray-800">
  Your App Name
</h1>
```

2. Update the footer in `src/components/Footer.jsx`:
```jsx
<h3 className="text-2xl font-bold mb-4">Your App Name</h3>
```

### Modify Hero Content

Edit `src/components/Hero.jsx` to customize:
- Headlines and descriptions
- Call-to-action buttons
- Feature cards

### Style Customization

The project uses Tailwind CSS. You can customize:
- Colors: Edit the color classes throughout components
- Typography: Modify font sizes and weights
- Spacing: Adjust padding and margin classes
- Add custom styles in `src/index.css`

## 🔧 Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint
```

## 🚀 Deployment

### Deploy to Vercel

1. Push your code to GitHub
2. Import your repository in Vercel
3. Add environment variables in Vercel dashboard:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
4. Deploy!

### Deploy to Netlify

1. Build the project: `npm run build`
2. Upload the `dist` folder to Netlify
3. Set environment variables in Netlify dashboard

## 📚 Learning Resources

- [React Documentation](https://reactjs.org/docs)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Supabase Documentation](https://supabase.com/docs)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Environment Variables Not Loading**
- Make sure your `.env` file is in the root directory
- Restart the development server after adding variables
- Ensure variables start with `VITE_`

**Supabase Connection Error**
- Verify your Supabase URL and anon key
- Check if your Supabase project is active
- Ensure the posts table exists

**Tailwind Styles Not Working**
- Verify Tailwind CSS is properly configured
- Check `tailwind.config.js` content paths
- Ensure `@tailwind` directives are in `src/index.css`

**Build Errors**
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Update dependencies: `npm update`
- Check for TypeScript errors if using TS

Need more help? Check the [issues page](https://github.com/your-repo/issues) or create a new issue.
