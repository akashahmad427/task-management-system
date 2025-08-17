# Deployment Guide - Task Management System

This guide will help you deploy your Django Task Management System to various platforms.

## 🚀 Quick Deployment Options

### Option 1: Railway (Recommended - Easiest)
**Free Tier**: Available
**Deployment Time**: 5-10 minutes

#### Steps:
1. **Go to [Railway.app](https://railway.app)**
2. **Sign up/Login** with GitHub
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**: `akashahmad427/task-management-system`
6. **Railway will automatically detect Django and deploy**

#### Environment Variables to Set:
```
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.railway.app,your-app-name.railway.app
```

### Option 2: Render (Easy - Free tier available)
**Free Tier**: Available
**Deployment Time**: 10-15 minutes

#### Steps:
1. **Go to [Render.com](https://render.com)**
2. **Sign up/Login** with GitHub
3. **Click "New +" → "Web Service"**
4. **Connect your GitHub repository**
5. **Configure:**
   - **Name**: `task-management-system`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn task_management_system.wsgi:application`

#### Environment Variables:
```
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.onrender.com,your-app-name.onrender.com
```

### Option 3: PythonAnywhere (Easy - Free tier available)
**Free Tier**: Available
**Deployment Time**: 15-20 minutes

#### Steps:
1. **Go to [PythonAnywhere.com](https://www.pythonanywhere.com)**
2. **Sign up for free account**
3. **Go to "Web" tab**
4. **Click "Add a new web app"**
5. **Choose "Django" and "Python 3.12"**
6. **Upload your code or clone from GitHub**
7. **Install requirements**: `pip install -r requirements.txt`
8. **Configure WSGI file**

## 🔧 Pre-deployment Checklist

- [x] ✅ Procfile created
- [x] ✅ requirements.txt updated with gunicorn
- [x] ✅ runtime.txt created
- [x] ✅ Environment variables configured
- [x] ✅ Static files configuration updated
- [x] ✅ DEBUG setting made configurable

## 🌐 Post-deployment Steps

### 1. Run Migrations
```bash
python manage.py migrate
```

### 2. Create Superuser
```bash
python manage.py createsuperuser
```

### 3. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 4. Test Your Application
- Visit your deployed URL
- Test user registration/login
- Test task creation/management
- Test API endpoints

## 🔒 Security Considerations

### Production Settings:
- Set `DEBUG = False`
- Use strong `SECRET_KEY`
- Configure proper `ALLOWED_HOSTS`
- Set up HTTPS (Railway/Render do this automatically)
- Use environment variables for sensitive data

### Database:
- Consider using PostgreSQL for production
- Set up database backups
- Use connection pooling for better performance

## 📱 Custom Domain (Optional)

### Railway:
1. Go to your project settings
2. Click "Custom Domains"
3. Add your domain
4. Update DNS records

### Render:
1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain
4. Update DNS records

## 🚨 Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check requirements.txt for compatibility
   - Verify Python version in runtime.txt

2. **Database Errors**:
   - Ensure migrations are run
   - Check database connection settings

3. **Static Files Not Loading**:
   - Run `collectstatic`
   - Check STATIC_ROOT configuration

4. **500 Errors**:
   - Check logs in your platform's dashboard
   - Verify environment variables are set

## 📊 Monitoring & Maintenance

### Railway:
- Built-in monitoring dashboard
- Automatic scaling
- Log viewing

### Render:
- Performance monitoring
- Log access
- Health checks

## 🎯 Recommended for Beginners: Railway

**Why Railway?**
- ✅ Automatic Django detection
- ✅ Free tier available
- ✅ Simple GitHub integration
- ✅ Automatic HTTPS
- ✅ Built-in monitoring
- ✅ Easy environment variable management

## 📞 Support

If you encounter issues:
1. Check the platform's documentation
2. Review Django deployment checklist
3. Check your application logs
4. Verify environment variables

## 🎉 Success!

Once deployed, you'll have:
- ✅ **Live application URL** (e.g., `https://your-app.railway.app`)
- ✅ **Publicly accessible** Task Management System
- ✅ **Professional deployment** for your portfolio
- ✅ **All deliverables completed** for your assignment

---

**Next Step**: Choose your preferred platform and follow the deployment steps above! 