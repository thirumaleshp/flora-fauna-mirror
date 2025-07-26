# ⚡ Quick Start Guide

Get your React + Supabase homepage running in 5 minutes!

## 📋 Prerequisites

- [ ] Node.js 16+ installed ([Download here](https://nodejs.org/))
- [ ] A Supabase account ([Sign up free](https://supabase.com))

## 🚀 5-Minute Setup

### Step 1: Install Dependencies
```bash
npm install
```

### Step 2: Set Up Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign in
2. Click "New Project"
3. Fill in your project details and wait for setup to complete
4. Go to **Settings** → **API**
5. Copy your **Project URL** and **anon public key**

### Step 3: Configure Environment

1. Rename `.env.example` to `.env`
2. Replace the placeholder values with your Supabase credentials:

```env
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

### Step 4: Set Up Database

1. In your Supabase dashboard, go to **SQL Editor**
2. Copy the contents of `setup-supabase.sql`
3. Paste and run the script
4. You should see: "Database setup completed successfully!"

### Step 5: Start Development Server

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser! 🎉

## ✅ What You Should See

- ✅ Modern homepage with navbar
- ✅ Hero section with call-to-action
- ✅ Posts section displaying data from Supabase
- ✅ Footer with links
- ✅ Responsive design that works on mobile

## 🔧 Troubleshooting

**🚫 "Connection Error" message?**
- Double-check your Supabase URL and key in `.env`
- Make sure you ran the SQL setup script
- Restart the dev server: `npm run dev`

**🚫 Blank posts section?**
- Go to Supabase → Table Editor → posts
- Make sure sample data exists
- Check browser console for errors

**🚫 Tailwind styles not working?**
- Clear cache: `rm -rf node_modules .vite && npm install`
- Restart dev server

## 🎨 Next Steps

1. **Customize branding**: Update app name in `src/components/Navbar.jsx`
2. **Add content**: Modify hero text in `src/components/Hero.jsx`
3. **Style tweaks**: Edit Tailwind classes throughout components
4. **Add features**: Check out the full README for advanced customization

## 📚 Helpful Resources

- [Full Documentation](./README.md)
- [Supabase Docs](https://supabase.com/docs)
- [React Docs](https://reactjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)

Need help? Open an issue or check the troubleshooting section in the main README!