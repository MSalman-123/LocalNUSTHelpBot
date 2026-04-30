# NUST Help Bot - Intelligent Assistant System

A sophisticated AI-powered chatbot system for NUST (National University of Sciences and Technology) that provides intelligent responses to student and faculty queries using advanced document retrieval and natural language processing.

## 🚀 Quick Start

### One-Click Launch:
**Simply run:**
```bash
START_NUST_BOT.bat
```

This automated launcher handles:
- ✅ Ollama AI backend installation (if needed)
- ✅ DeepSeek-R1:1.5B model download (if needed)
- ✅ Vector database initialization
- ✅ Web server startup
- ✅ Automatic browser launch

## 📦 What's Included

- ✅ **Standalone Executable** (`dist/NUST_HELP_BOT.exe`) - Works on any Windows PC
- ✅ **Portable Python** - Self-contained, no system installation needed
- ✅ **Ollama Setup** - Automated AI backend installation
- ✅ **AI Model** - Uses DeepSeek-R1:1.5B for intelligent responses

## 🎯 Features

- **🤖 Intelligent Q&A** - Advanced question answering using RAG (Retrieval-Augmented Generation)
- **🎨 Modern Web Interface** - Professional Streamlit UI with NUST branding
- **🧠 AI-Powered** - DeepSeek-R1:1.5B model for context-aware responses
- **📚 Document Intelligence** - ChromaDB vector search across NUST documents
- **🔄 Real-time Processing** - Instant responses with conversation logging
- **💻 Self-Contained** - No external dependencies or Python installation required

## 📋 System Requirements

- **Operating System**: Windows 10/11 (x64)
- **Memory**: 4GB RAM minimum (8GB recommended for optimal performance)
- **Storage**: 2GB free disk space (for AI model and databases)
- **Network**: Internet connection required for first-time setup only
- **Processor**: Modern CPU with multi-core support

## 🔧 Installation & Setup

### Automated Setup (Recommended):
1. **Launch**: Run `START_NUST_BOT.bat`
2. **Follow Prompts**: Automatic installation of Ollama and AI model
3. **Access**: Application opens at http://localhost:8501
4. **Browser**: Auto-launches for immediate use

## 📁 Project Architecture

```
NUST_Help_Bot/
├── 📄 Core Files
│   ├── app.py                     # Main Streamlit application
│   ├── START_NUST_BOT.bat         # Automated launcher script
│   └── requirements.txt           # Python dependencies
├── 🤖 AI Components
│   ├── query_data.py              # RAG query implementation
│   ├── db_utils.py                # Database utilities
│   ├── populate_database.py       # Document processing
│   └── get_embedding_function.py  # Text embedding function
├── 📚 Data & Knowledge
│   ├── data/                      # Source documents (PDFs)
│   ├── chroma_FAQs/              # Vector database (FAQs)
│   ├── chroma_Handbook/          # Vector database (Handbook)
│   └── chat_logs.db              # Conversation history
├── 🖥️ Distribution
│   ├── dist/NUST_HELP_BOT.exe    # Standalone executable
│   └── portable_python/          # Embedded Python runtime
└── 🎨 Assets
    ├── nust_logo.png             # Application logo
    └── nust_logo.ico             # Windows icon
```

## 🎮 User Guide

### Getting Started:
1. **Launch Application**: Run `START_NUST_BOT.bat`
2. **Select Program**: Choose your academic program from dropdown
3. **Ask Questions**: Type queries about admissions, courses, facilities, etc.
4. **Receive Answers**: Get context-aware responses from NUST documents
5. **Continue Conversation**: Maintain session for follow-up questions

### Query Examples:
- "What are the admission requirements for engineering programs?"
- "Where is the library located and what are its hours?"
- "How do I apply for scholarships?"
- "What research facilities are available at NUST?"

## 🔧 Troubleshooting

### Common Issues & Solutions:

**🔌 Ollama Not Found**
- Solution: Run `START_NUST_BOT.bat` - auto-installs Ollama
- Manual: Download from https://ollama.com/download

**🌐 Connection Error**
- Check: `ollama serve` in terminal
- Verify: `ollama list` (should show deepseek-r1:1.5b)

**🚪 Server Not Starting**
- Ensure port 8501 is available
- Restart the application
- Check Windows Firewall settings

**📄 Document Processing Issues**
- Verify PDF files exist in `data/` folders
- Check file permissions
- Re-run application to rebuild vector database

## � Distribution & Deployment

### Complete Package Distribution:
1. **Package**: Copy entire project folder
2. **Deploy**: Recipient runs `START_NUST_BOT.bat`
3. **Result**: Fully automated setup and launch

### Minimal Distribution:
1. **Prerequisites**: Install Ollama from https://ollama.com/download
2. **Model Setup**: `ollama pull deepseek-r1:1.5b`
3. **Launch**: Run `NUST_HELP_BOT.exe` from `dist/` folder

## 🏗️ Technical Architecture

### Core Technologies:
- **Frontend**: Streamlit 1.13+ (Modern web UI framework)
- **Backend**: Python 3.11 with LangChain ecosystem
- **AI Engine**: DeepSeek-R1:1.5B via Ollama (1.1B parameters)
- **Vector Database**: ChromaDB for semantic document search
- **Embeddings**: Custom text embedding functions
- **Document Processing**: PyPDF for PDF parsing and chunking

### System Integration:
- **RAG Pipeline**: Retrieval-Augmented Generation for context awareness
- **Vector Search**: Semantic similarity across document corpus
- **Conversation Logging**: SQLite database for interaction history
- **Automated Setup**: Batch scripts for dependency management

## 📞 Support & Maintenance

### Quick Diagnostics:
```bash
# Check Ollama status
ollama list

# Verify model installation
ollama show deepseek-r1:1.5b

# Check server status
curl http://localhost:11434/api/tags
```

### Performance Optimization:
- **Memory Management**: Automatic garbage collection
- **Database Caching**: Persistent vector stores
- **Model Loading**: Efficient AI model initialization

---

**🏛️ Developed at High Performance Computing Lab, NUST-SEECS**  
**📅 Version 1.0 - Production Ready**  
**🔧 Maintained by NUST AI Research Team**
