# Model Compatibility Fix

## Issue
The evaluation endpoint was using outdated model names that don't exist:
- ❌ `models/gemini-1.5-flash` - Returns 404 error
- ❌ `models/gemini-1.5-pro` - Returns 404 error

## Root Cause
Gemini API model naming has changed. The 1.5 series models are no longer available or have been renamed.

## Solution
Updated to currently available models that support `generateContent`:
- ✅ `models/gemini-2.0-flash-exp` - Latest experimental flash model
- ✅ `models/gemini-2.5-flash` - Fast, efficient model
- ✅ `models/gemini-2.5-pro` - Higher quality, detailed summaries

## Verification Method
Used Gemini API to list all available models:
```python
import google.generativeai as genai
models = genai.list_models()
for m in models:
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
```

## Files Updated
1. **app.py** - Updated `models_to_test` list in `/evaluate` endpoint
2. **EVALUATION_FEATURES.md** - Updated documentation with correct model names
3. **README.md** - Updated model list in configuration section

## Current Available Models (as of Nov 2025)
- gemini-2.5-pro (recommended for quality)
- gemini-2.5-flash (recommended for speed)
- gemini-2.0-flash-exp (experimental features)
- gemini-2.0-flash (stable version)
- gemini-flash-latest (always points to latest flash)
- gemini-pro-latest (always points to latest pro)

## Testing Status
✅ Flask server running successfully
✅ All three models support generateContent
✅ No more 404 errors expected

## Best Practices
Always verify model availability before deployment:
1. Use `genai.list_models()` to check available models
2. Filter by `'generateContent' in m.supported_generation_methods`
3. Use full model names with `models/` prefix
4. Consider using `-latest` aliases for automatic updates
