import os
import time
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from collections import defaultdict

class NeoDocumentExplorer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NEO Explorer 2025")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')
        self.set_custom_theme()
        
        # In-memory index
        self.file_index = defaultdict(list)
        self.folder_index = defaultdict(list)
        
        self.documents_path = Path.home() / 'Documents'
        self.create_gui()
        self.scan_documents()

    def set_custom_theme(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Color palette
        self.bg_color = '#0a0a0a'
        self.fg_color = '#ffffff'
        self.accent_color = '#00ff9d'
        self.secondary_color = '#1a1a1a'
        self.hover_color = '#2a2a2a'
        
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.fg_color, font=('Segoe UI', 10))
        style.configure('TButton', background=self.secondary_color, foreground=self.fg_color,
                        borderwidth=0, font=('Segoe UI', 10))
        style.map('TButton', background=[('active', self.hover_color), ('!disabled', self.secondary_color)])
        style.configure('TEntry', fieldbackground=self.secondary_color, foreground=self.fg_color,
                        insertcolor=self.fg_color, borderwidth=0)
        style.configure('Treeview', background=self.secondary_color, foreground=self.fg_color,
                        fieldbackground=self.secondary_color, borderwidth=0, font=('Segoe UI', 10))
        style.configure('Treeview.Heading', background=self.bg_color, foreground=self.accent_color,
                        font=('Segoe UI Semibold', 11))
        style.map('Treeview', background=[('selected', self.accent_color)], foreground=[('selected', self.bg_color)])

    def scan_documents(self):
        start_time = time.time()
        self.file_index.clear()
        self.folder_index.clear()
        self.status_var.set("🛸 Scanning documents...")
        
        for entry in Path(self.documents_path).rglob('*'):
            try:
                if entry.is_file():
                    self.file_index[entry.name.lower()].append(str(entry))
                elif entry.is_dir():
                    self.folder_index[entry.name.lower()].append(str(entry))
            except PermissionError:
                continue
        
        scan_time = time.time() - start_time
        self.status_var.set(f"✅ Scan complete | {len(self.file_index)} files | {len(self.folder_index)} folders | {scan_time:.2f}s")

    def create_gui(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="NEO EXPLORER", font=('Segoe UI Light', 24), 
                foreground=self.accent_color).pack(side=tk.LEFT)
        
        # Search section
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.search_items())
        
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, style='TEntry')
        self.search_entry.pack(fill=tk.X, ipady=8)
        self.search_entry.bind('<Return>', self.search_items)
        
        # Results section
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_tree = ttk.Treeview(results_frame, columns=('Type', 'Path', 'Modified'), selectmode='browse')
        vsb = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        hsb = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.results_tree.heading('#0', text='Name', anchor=tk.W)
        self.results_tree.heading('Type', text='Type', anchor=tk.W)
        self.results_tree.heading('Path', text='Path', anchor=tk.W)
        self.results_tree.heading('Modified', text='Modified', anchor=tk.W)
        
        self.results_tree.column('#0', width=300, stretch=tk.NO)
        self.results_tree.column('Type', width=120, stretch=tk.NO)
        self.results_tree.column('Path', width=400)
        self.results_tree.column('Modified', width=180, stretch=tk.NO)
        
        self.results_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                             font=('Segoe UI', 9), foreground='#666666')
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Context menu
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=self.secondary_color, 
                                  fg=self.fg_color, bd=0, activebackground=self.accent_color,
                                  activeforeground=self.bg_color)
        self.context_menu.add_command(label="Open", command=self.open_item)
        self.context_menu.add_command(label="Reveal in Explorer", command=self.reveal_item)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Copy Path", command=self.copy_path)
        
        # Bindings
        self.results_tree.bind("<Double-1>", self.open_item)
        self.results_tree.bind("<Return>", self.open_item)
        self.results_tree.bind("<Button-3>", self.show_context_menu)
        self.root.bind("<Control-r>", lambda e: self.scan_documents())

    def search_items(self, event=None):
        search_term = self.search_var.get().lower()
        self.results_tree.delete(*self.results_tree.get_children())
        
        results = []
        
        # Search folders
        for name, paths in self.folder_index.items():
            if search_term in name:
                for path in paths:
                    p = Path(path)
                    results.append(('📁', p.name, 'Folder', p.parent, p.stat().st_mtime))
        
        # Search files
        for name, paths in self.file_index.items():
            if search_term in name:
                for path in paths:
                    p = Path(path)
                    results.append(('📄', p.name, p.suffix[1:].upper() + ' File', p.parent, p.stat().st_mtime))
        
        # Add items with corrected syntax
        for item in sorted(results, key=lambda x: x[1]):
            self.results_tree.insert(
                '', 
                'end', 
                text=f" {item[0]}  {item[1]}",
                values=(item[2], str(item[3]), time.strftime('%Y-%m-%d %H:%M', time.localtime(item[4]))),
                tags=(item[0],)
            )

    def open_item(self, event=None):
        selected_item = self.results_tree.selection()
        if selected_item:
            path = Path(self.results_tree.item(selected_item)['values'][1]) / \
                  self.results_tree.item(selected_item)['text'].split('  ')[-1]
            try:
                if path.is_file():
                    os.startfile(path)
                elif path.is_dir():
                    os.startfile(path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open item:\n{str(e)}")

    def reveal_item(self):
        selected_item = self.results_tree.selection()
        if selected_item:
            path = Path(self.results_tree.item(selected_item)['values'][1])
            try:
                os.startfile(path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not reveal location:\n{str(e)}")

    def copy_path(self):
        selected_item = self.results_tree.selection()
        if selected_item:
            full_path = Path(self.results_tree.item(selected_item)['values'][1]) / \
                       self.results_tree.item(selected_item)['text'].split('  ')[-1]
            self.root.clipboard_clear()
            self.root.clipboard_append(str(full_path))

    def show_context_menu(self, event):
        item = self.results_tree.identify_row(event.y)
        if item:
            self.results_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    explorer = NeoDocumentExplorer()
    explorer.run()