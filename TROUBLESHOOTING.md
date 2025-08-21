# Troubleshooting Guide

## Common Setup Issues

### 1. SQLAlchemy Compatibility Error
**Error:** `AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> directly inherits TypingOnly...`

**Solution:** This is a Python 3.13 + SQLAlchemy 2.0 compatibility issue. 
- The project now uses SQLAlchemy 1.4.53 (compatible version)
- Run: `pip uninstall sqlalchemy` then `pip install -r requirements.txt`
- Or use the provided `start_backend.bat` script

### 2. ChromaDB/C++ Compilation Errors
**Error:** `Building wheel for chroma-hnswlib failed`

**Solution:** Removed ChromaDB from requirements for Windows compatibility.
- Core functionality works without ChromaDB
- For production, consider using Docker or installing Visual Studio Build Tools

### 3. uvicorn Command Not Found
**Error:** `'uvicorn' is not recognized as an internal or external command`

**Solution:** 
- Activate virtual environment: `venv\Scripts\activate`
- Or use: `python -m uvicorn app.main:app --reload`
- Or use the provided `start_backend.bat` script

### 4. Python Not Found
**Error:** `Python was not found`

**Solutions:**
- Install Python from [python.org](https://python.org)
- Or install from Microsoft Store
- Ensure Python is added to PATH during installation

### 5. Module Import Errors
**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:**
- Ensure you're in the `backend` directory
- Virtual environment is activated
- All dependencies are installed

## Testing Your Setup

### Backend Test
```bash
cd backend
python test_setup.py
```

This will verify:
- ✅ All imports work
- ✅ Database can be created
- ⚠️ API keys configuration

### Manual Verification
1. **Check Python version:**
   ```bash
   python --version
   ```
   Should be Python 3.8 or higher.

2. **Check virtual environment:**
   ```bash
   where python
   ```
   Should point to your venv directory.

3. **Test FastAPI directly:**
   ```bash
   python -c "import fastapi; print('FastAPI OK')"
   ```

4. **Test database creation:**
   ```bash
   python -c "from app.database.database import engine; from app.models.models import Base; Base.metadata.create_all(bind=engine); print('Database OK')"
   ```

## API Configuration

### Gemini API Key
1. Get key from: https://makersuite.google.com/app/apikey
2. Copy `.env.example` to `.env`
3. Add: `GEMINI_API_KEY=your_key_here`

### Without API Key
The app will work in "demo mode":
- Explanations: Simple fallback text
- SVG Generation: Placeholder graphics
- Core functionality: ✅ Working

## Performance Issues

### Slow Startup
- First run downloads models (~100MB)
- Subsequent runs are faster
- Consider SSD for better performance

### Memory Usage
- Basic setup: ~200MB RAM
- With AI models: ~500MB RAM
- Minimum requirement: 4GB RAM

## Environment Verification

### Required Files Checklist
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/models.py
│   ├── database/database.py
│   └── api/
├── requirements.txt
├── test_setup.py
└── .env (copy from .env.example)
```

### Package Versions
- Python: 3.8-3.12 (avoid 3.13 for now)
- FastAPI: 0.104.1
- SQLAlchemy: 1.4.53 (not 2.0+)
- Uvicorn: 0.24.0

## Getting Help

### Debug Mode
Add to `.env`:
```
DEBUG=True
```

### Verbose Logging
```bash
python -m uvicorn app.main:app --reload --log-level debug
```

### Check API Status
Visit: http://localhost:8000/health

Expected response: `{"status": "healthy"}`

### API Documentation
Visit: http://localhost:8000/docs

## Windows-Specific Issues

### Long Path Names
If you get path-related errors:
- Move project closer to C:\ root
- Enable long path support in Windows

### Antivirus Software
Some antivirus may block:
- Virtual environment creation
- Package installation
- Local server startup

Add project folder to antivirus exclusions.

### PowerShell Execution Policy
If batch files don't work:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Still Having Issues?

1. **Delete and recreate virtual environment:**
   ```bash
   rmdir /s venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Check system requirements:**
   - Windows 10/11
   - 4GB+ RAM
   - 2GB+ free disk space
   - Internet connection for package installation

3. **Try manual setup:**
   Follow the manual steps in README.md instead of using batch files.

4. **Use alternative Python distribution:**
   - Try Anaconda instead of standard Python
   - Or use Python from Microsoft Store