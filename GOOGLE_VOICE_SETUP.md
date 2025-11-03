# 🎤 GOOGLE CLOUD VOICE SETUP

## ✅ **Google Cloud TTS is Now Integrated!**

Your AI Assistant now uses **Google Cloud Text-to-Speech** for ULTRA NATURAL human voice! 🚀

---

## 🎯 **Current Status**

### Voice Priority:
1. **Google Cloud TTS** ← **PRIMARY** (Ultra natural, human-like!)
   - **English:** `en-US-Neural2-F` (Most natural female voice)
   - **Urdu:** `ur-PK-Wavenet-A` (Natural Urdu voice)
2. **pyttsx3** ← Offline fallback (Windows SAPI)
3. **gTTS** ← Last resort (basic Google TTS)

---

## 📋 **Two Options:**

### **Option 1: Use Without Setup (Current)**
Your assistant will automatically use **pyttsx3** or **gTTS** as fallback voices. These work well but are not as natural as Google Cloud TTS.

**No action needed** - it's already working! ✅

---

### **Option 2: Enable Google Cloud TTS (Best Quality)**

To get the **BEST** ultra-natural human voice, follow these steps:

#### **Step 1: Create Google Cloud Account**
1. Go to: https://console.cloud.google.com
2. Sign in or create a free account
3. **Free Tier**: 1 million characters/month FREE! (More than enough)

#### **Step 2: Enable Text-to-Speech API**
1. Go to: https://console.cloud.google.com/apis/library/texttospeech.googleapis.com
2. Click **"Enable"**

#### **Step 3: Create Service Account & Download Credentials**
1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click **"Create Service Account"**
3. Name: `jarvis-tts` (or any name)
4. Click **"Create and Continue"**
5. Role: **"Cloud Text-to-Speech User"**
6. Click **"Done"**
7. Click on the service account you just created
8. Go to **"Keys"** tab
9. Click **"Add Key" → "Create New Key" → "JSON"**
10. **Save the JSON file** as `google-credentials.json` in your project folder:
    ```
    C:\Users\Anas Raheem\Desktop\AI Desktop Assistant\google-credentials.json
    ```

#### **Step 4: Set Environment Variable**
**Option A: PowerShell (Temporary)**
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Anas Raheem\Desktop\AI Desktop Assistant\google-credentials.json"
python app.py
```

**Option B: Add to .env file (Recommended)**
Edit your `.env` file and add:
```
GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Anas Raheem\Desktop\AI Desktop Assistant\google-credentials.json
```

Then update `app.py` to load it:
```python
from dotenv import load_dotenv
import os
load_dotenv()

# Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
```

#### **Step 5: Restart Flask Server**
```powershell
cd "C:\Users\Anas Raheem\Desktop\AI Desktop Assistant"
python app.py
```

You should see:
```
🎤 Google Cloud TTS initialized as PRIMARY engine (Ultra Natural Voice!)
```

---

## 🎤 **Voice Quality Comparison**

| Engine | Quality | Speed | Languages | Cost |
|--------|---------|-------|-----------|------|
| **Google Cloud TTS** | ⭐⭐⭐⭐⭐ | Fast | 40+ | Free (1M chars/month) |
| pyttsx3 | ⭐⭐⭐ | Fast | English | Free |
| gTTS | ⭐⭐⭐ | Medium | 100+ | Free |

---

## 🔊 **Available Voices**

### English (Ultra Natural):
- `en-US-Neural2-F` - Natural female voice (BEST!)
- `en-US-Neural2-A` - Natural male voice
- `en-US-Wavenet-F` - High quality female
- `en-GB-Neural2-A` - British accent

### Urdu (Natural):
- `ur-PK-Wavenet-A` - Natural Urdu voice (BEST!)

You can change the voice in `voice_module.py` → `_speak_google_tts()` method.

---

## 🐛 **Troubleshooting**

### ❌ "Google Cloud TTS not configured"
- Make sure you've completed **Step 4** (set `GOOGLE_APPLICATION_CREDENTIALS`)
- Verify the JSON file path is correct
- The system will automatically fall back to pyttsx3/gTTS

### ❌ "Permission denied" or "API not enabled"
- Make sure you enabled the **Text-to-Speech API** (Step 2)
- Make sure the service account has the **"Cloud Text-to-Speech User"** role

### ❌ "Quota exceeded"
- Free tier: 1 million characters/month
- Upgrade to paid plan if needed

---

## 💡 **Tips**

- **Without Google Cloud:** Your assistant still works great with pyttsx3!
- **With Google Cloud:** You get the MOST NATURAL human-like voice available!
- **Cost:** Free tier is more than enough for personal use
- **Privacy:** Audio is processed by Google Cloud (online)

---

## 🎯 **Next Steps**

1. **Try it now** - It's already working with fallback voices! ✅
2. **Want best quality?** - Follow the setup steps above
3. **Questions?** - Check the logs for voice engine status

---

**Enjoy your ULTRA NATURAL AI Assistant voice! 🎤✨**

