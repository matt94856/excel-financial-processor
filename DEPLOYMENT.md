# Deployment Guide

This guide will help you deploy the Excel Financial Processor to GitHub and Netlify.

## Prerequisites

- GitHub account
- Netlify account (free)
- Git installed on your computer

## Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in
2. **Click "New repository"** (green button)
3. **Repository settings:**
   - Name: `excel-financial-processor`
   - Description: `Professional Excel file processor for estimates and financial statements`
   - Visibility: Public (for free Netlify hosting)
   - Initialize with README: ❌ (we already have files)
4. **Click "Create repository"**

## Step 2: Upload Files to GitHub

### Option A: Using GitHub Web Interface (Easiest)

1. **Download all project files** to your computer
2. **Go to your new repository** on GitHub
3. **Click "uploading an existing file"**
4. **Drag and drop all files** from your project folder
5. **Commit message:** `Initial commit - Excel Financial Processor`
6. **Click "Commit changes"**

### Option B: Using Git Command Line

```bash
# Navigate to your project folder
cd /path/to/your/excel/project

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Excel Financial Processor"

# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/excel-financial-processor.git

# Push to GitHub
git push -u origin main
```

## Step 3: Deploy to Netlify

1. **Go to [netlify.com](https://netlify.com)** and sign in
2. **Click "New site from Git"**
3. **Choose "GitHub"** as your Git provider
4. **Authorize Netlify** to access your GitHub account
5. **Select your repository:** `excel-financial-processor`
6. **Build settings:**
   - Build command: `npm run build`
   - Publish directory: `frontend/build`
   - Functions directory: `netlify/functions`
7. **Click "Deploy site"**

## Step 4: Configure Environment Variables (Optional)

If you need environment variables:

1. **Go to your Netlify site dashboard**
2. **Click "Site settings"**
3. **Click "Environment variables"**
4. **Add any required variables**

## Step 5: Test Your Deployment

1. **Wait for deployment to complete** (usually 2-5 minutes)
2. **Visit your Netlify URL** (e.g., `https://your-site-name.netlify.app`)
3. **Test file upload** with a sample Excel file
4. **Verify downloads work**

## Troubleshooting

### Build Fails
- Check the build logs in Netlify dashboard
- Ensure all dependencies are in `package.json`
- Verify Node.js version compatibility

### API Calls Fail
- Check that Netlify functions are properly configured
- Verify CORS settings in function code
- Check browser console for errors

### File Upload Issues
- Ensure file size limits are appropriate
- Check multipart form handling in functions
- Verify file type validation

## File Structure for Deployment

```
excel-financial-processor/
├── .gitignore
├── netlify.toml
├── package.json
├── requirements-netlify.txt
├── DEPLOYMENT.md
├── README.md
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
└── netlify/
    └── functions/
        └── upload.py
```

## Custom Domain (Optional)

1. **Go to your Netlify site settings**
2. **Click "Domain management"**
3. **Add custom domain**
4. **Follow DNS configuration instructions**

## Monitoring and Analytics

- **Netlify Analytics:** Built-in traffic analytics
- **Function logs:** Monitor serverless function performance
- **Error tracking:** Check Netlify dashboard for errors

## Updates and Maintenance

To update your deployed site:

1. **Make changes locally**
2. **Commit and push to GitHub**
3. **Netlify automatically rebuilds and deploys**

## Support

- **Netlify Docs:** [docs.netlify.com](https://docs.netlify.com)
- **GitHub Docs:** [docs.github.com](https://docs.github.com)
- **Project Issues:** Create issues in your GitHub repository
