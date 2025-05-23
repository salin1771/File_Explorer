# NEO File Explorer 🚀

![image](https://github.com/user-attachments/assets/c79921c2-1b99-4d35-90d3-a94ce115226b)


A modern, high-performance file explorer with a sleek dark theme and lightning-fast search capabilities. Designed for power users who value efficiency and aesthetics.

## ✨ Features

- **Cyberpunk UI**  
  Dark theme with neon accents and clean layout
- **Instant Search**  
  Find files/folders across your entire system in milliseconds
- **Smart Preview**  
  Quick access to file metadata and directory info
- **Cross-Platform**  
  Works on Windows 10/11 
- **Lightweight**  
  Uses <1% CPU during idle, ~50MB RAM usage
- **Advanced Features**
  - Multi-window support
  - Custom keyboard shortcuts
  - File operations history
  - Emoji-based visual cues
 
![image](https://github.com/user-attachments/assets/e152ef86-b50e-4241-8106-6b7e1cf4cf41)


## 🚀 Installation

### For End Users
1. Download latest release from MY GitHub Repo
2. Run `NEOExplorer_Setup.exe`
3. Follow installation wizard
4. Launch from Start Menu or Desktop shortcut

### For Developers
```bash
# Clone repository
git clone https://github.com/salin1771/neo-explorer.git
cd neo-explorer

# Install dependencies
pip install -r requirements.txt

# Run application
python neo_explorer.py
```

## 📖 Usage

1. **Search**  
   Start typing to instantly find files/folders
2. **Navigate**  
   Use ↑/↓ arrows or mouse
3. **Quick Actions**
   - Double-click: Open file/folder
   - Right-click: Context menu (Open Location, Copy Path)
   - Ctrl+R: Refresh index
4. **Hotkeys**
   - Ctrl+F: Focus search
   - Ctrl+Q: Quit
   - Ctrl+Shift+M: Toggle metadata panel

## 🔧 Building from Source

### Requirements
- Python 3.10+
- Tkinter
- pywin32 (Windows only)

```bash
# Create executable
pip install pyinstaller
pyinstaller --noconsole --onefile --icon=assets/icon.ico neo_explorer.py

# Output will be in dist/ folder
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request


## 🙏 Acknowledgements

- Inspired by Windows 11 File Explorer
- Built with Python & Tkinter
- Icons from [Flaticon](https://www.flaticon.com)
