import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import io
from datetime import datetime

class LogViewer:
    """日志查看器"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("日志查看器")
        self.root.geometry("800x600")
        
        # 初始化日志级别
        self.log_levels = {
            'DEBUG': 0,
            'INFO': 1,
            'WARNING': 2,
            'ERROR': 3,
            'CRITICAL': 4
        }
        
        # 创建界面
        self.create_widgets()
        
        # 重定向标准输出
        self.redirect_output()
        
    def create_widgets(self):
        """创建界面组件"""
        # 工具栏
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # 日志级别过滤
        tk.Label(toolbar, text="日志级别:").pack(side=tk.LEFT, padx=5)
        self.level_var = tk.StringVar(value='INFO')
        self.level_menu = ttk.Combobox(toolbar, textvariable=self.level_var,
                                     values=list(self.log_levels.keys()))
        self.level_menu.pack(side=tk.LEFT, padx=5)
        self.level_menu.bind('<<ComboboxSelected>>', self.filter_logs)
        
        # 搜索框
        tk.Label(toolbar, text="搜索:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(toolbar)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.filter_logs)
        
        # 导出按钮
        export_btn = tk.Button(toolbar, text="导出日志", command=self.export_logs)
        export_btn.pack(side=tk.RIGHT, padx=5)
        
        # 日志显示区域
        self.log_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.configure(state='disabled')
        
    def redirect_output(self):
        """重定向标准输出"""
        class StdoutRedirector(io.StringIO):
            def __init__(self, log_viewer):
                super().__init__()
                self.log_viewer = log_viewer
                
            def write(self, message):
                self.log_viewer.append_log(message)
                
        sys.stdout = StdoutRedirector(self)
        sys.stderr = StdoutRedirector(self)
        
    def append_log(self, message):
        """添加日志"""
        self.log_text.configure(state='normal')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.configure(state='disabled')
        self.log_text.see(tk.END)
        
    def filter_logs(self, event=None):
        """过滤日志"""
        search_text = self.search_entry.get().lower()
        min_level = self.log_levels[self.level_var.get()]
        
        self.log_text.configure(state='normal')
        self.log_text.tag_remove('highlight', '1.0', tk.END)
        
        for line in self.log_text.get('1.0', tk.END).split('\n'):
            if search_text in line.lower():
                start = self.log_text.search(line, '1.0', tk.END)
                if start:
                    end = f"{start}+{len(line)}c"
                    self.log_text.tag_add('highlight', start, end)
                    
        self.log_text.tag_config('highlight', background='yellow')
        self.log_text.configure(state='disabled')
        
    def export_logs(self):
        """导出日志"""
        file_path = tk.filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.log_text.get('1.0', tk.END))
                self.append_log(f"日志已成功导出到 {file_path}\n")
            except Exception as e:
                self.append_log(f"导出日志失败: {str(e)}\n")
                
    def cleanup(self):
        """清理资源"""
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

if __name__ == "__main__":
    root = tk.Tk()
    log_viewer = LogViewer(root)
    root.mainloop()
    log_viewer.cleanup()