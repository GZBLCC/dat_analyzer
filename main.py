import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from file_handler import FileHandler
from dat_modifier import DatModifier
from dat_parser import DatParser
from data_analyzer import DataAnalyzer
from data_extractor import DataExtractor
from data_inspector import DataInspector
from log_viewer import LogViewer

class DatAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DAT 文件分析器 v1.1")
        self.root.protocol("WM_DELETE_WINDOW", self.cleanup)
        self.root.geometry("900x650")
        
        # 设置默认字体和样式
        self.default_font = ('Microsoft YaHei', 10)
        self.root.option_add('*Font', self.default_font)
        self.root.option_add('*TButton*Padding', 5)
        self.root.option_add('*TButton*Relief', 'raised')
        
        # 初始化状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var,
                                 bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 设置主题
        style = ttk.Style()
        style.theme_use('clam')
        
        # 初始化变量
        self.file_path = tk.StringVar()
        self.current_file = None
        
        # 创建界面布局
        self.create_widgets()
        
    def create_widgets(self):
        # 顶部工具栏
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # 文件操作按钮
        open_btn = tk.Button(toolbar, text="打开文件", command=self.open_file)
        open_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 日志查看器按钮
        log_btn = tk.Button(toolbar, text="查看日志", command=self.show_log_viewer)
        log_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 文件路径显示
        file_path_label = tk.Label(toolbar, textvariable=self.file_path)
        file_path_label.pack(side=tk.LEFT, padx=10)
        
        # 主内容区域
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 功能选项卡
        self.notebook = tk.ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建各个功能标签页
        self.create_file_info_tab()
        self.create_keyword_tab()
        self.create_structure_tab()
        self.create_extract_tab()
        
    def create_file_info_tab(self):
        """创建文件信息标签页"""
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="文件信息")
        
        # 文件基本信息显示
        info_frame = tk.LabelFrame(tab, text="文件基本信息")
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 分析按钮
        analyze_btn = tk.Button(info_frame, text="分析文件", command=self.analyze_file)
        analyze_btn.pack(side=tk.TOP, pady=5)
        
        self.file_info_text = scrolledtext.ScrolledText(info_frame, height=10)
        self.file_info_text.pack(fill=tk.BOTH, expand=True)
        
    def analyze_file(self):
        """分析文件内容"""
        if not self.current_file:
            return
            
        analysis = self.current_file.analyze_file()
        if analysis:
            info = f"文件大小: {analysis['file_size']} 字节\n"
            info += f"文件类型: {'文本文件' if analysis['is_text'] else '二进制文件'}\n"
            info += f"\n可打印字符串:\n"
            info += '\n'.join(analysis['strings']) if analysis['strings'] else "无"
            info += f"\n\n十六进制转储:\n{analysis['hex_dump']}"
            
            self.file_info_text.delete(1.0, tk.END)
            self.file_info_text.insert(tk.END, info)
        
    def create_keyword_tab(self):
        """创建关键词分析标签页"""
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="关键词分析")
        
        # 关键词输入和分析
        keyword_frame = tk.LabelFrame(tab, text="关键词搜索")
        keyword_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(keyword_frame, text="输入关键词:").pack(side=tk.LEFT)
        self.keyword_entry = tk.Entry(keyword_frame)
        self.keyword_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        search_btn = tk.Button(keyword_frame, text="搜索", command=self.search_keywords)
        search_btn.pack(side=tk.RIGHT)
        
        # 结果显示区域
        result_frame = tk.LabelFrame(tab, text="搜索结果")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.keyword_result_text = scrolledtext.ScrolledText(result_frame)
        self.keyword_result_text.pack(fill=tk.BOTH, expand=True)
        
    def create_structure_tab(self):
        """创建数据结构分析标签页"""
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="结构分析")
        
        # 分析按钮
        analyze_btn = tk.Button(tab, text="分析数据结构", command=self.analyze_structure)
        analyze_btn.pack(pady=5)
        
        # 结果显示区域
        result_frame = tk.LabelFrame(tab, text="分析结果")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.structure_result_text = scrolledtext.ScrolledText(result_frame)
        self.structure_result_text.pack(fill=tk.BOTH, expand=True)
        
    def create_extract_tab(self):
        """创建数据提取标签页"""
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text="数据提取")
        
        # 提取选项
        options_frame = tk.LabelFrame(tab, text="提取选项")
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(options_frame, text="最小字符串长度:").pack(side=tk.LEFT)
        self.min_length_entry = tk.Entry(options_frame, width=5)
        self.min_length_entry.pack(side=tk.LEFT, padx=5)
        self.min_length_entry.insert(0, "4")
        
        extract_btn = tk.Button(options_frame, text="提取字符串", command=self.extract_strings)
        extract_btn.pack(side=tk.RIGHT)
        
        # 结果显示区域
        result_frame = tk.LabelFrame(tab, text="提取结果")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.extract_result_text = scrolledtext.ScrolledText(result_frame)
        self.extract_result_text.pack(fill=tk.BOTH, expand=True)
        
    def open_file(self):
        """打开文件并显示基本信息"""
        try:
            self.status_var.set("正在打开文件...")
            self.root.update()
            
            file_types = [
                ("所有文件", "*.*"),
                ("DAT 文件", "*.dat"),
                ("二进制文件", "*.bin"),
                ("文本文件", "*.txt"),
                ("日志文件", "*.log")
            ]
            file_path = filedialog.askopenfilename(filetypes=file_types)
            if file_path:
                self.file_path.set(file_path)
                self.current_file = DatModifier(file_path)
                
                # 显示加载进度
                self.status_var.set("正在加载文件...")
                self.root.update()
                
                if self.current_file.read_file():
                    self.show_file_info()
                    self.status_var.set(f"成功加载文件: {file_path}")
                else:
                    self.status_var.set("文件加载失败")
                    tk.messagebox.showerror("错误", "无法读取文件内容")
        except Exception as e:
            self.status_var.set("发生错误")
            tk.messagebox.showerror("错误", f"文件操作出错: {str(e)}")
        finally:
            self.root.update()
                
    def show_file_info(self):
        """显示文件基本信息"""
        if self.current_file:
            header = self.current_file.parse_header()
            if header:
                info = f"文件标识符: {header['magic']}\n"
                info += f"版本号: {header['version']}\n"
                info += f"文件大小: {header['file_size']} 字节\n"
                info += f"创建时间戳: {header['timestamp']}\n"
                self.file_info_text.delete(1.0, tk.END)
                self.file_info_text.insert(tk.END, info)
            else:
                self.file_info_text.delete(1.0, tk.END)
                self.file_info_text.insert(tk.END, "无法解析文件头")
                
    def search_keywords(self):
        """搜索关键词"""
        if not self.current_file:
            return
            
        keyword = self.keyword_entry.get()
        if keyword:
            inspector = DataInspector(self.file_path.get())
            if inspector.read_file():
                results = inspector.find_keywords([keyword])
                if results:
                    self.keyword_result_text.delete(1.0, tk.END)
                    for keyword, info in results.items():
                        self.keyword_result_text.insert(tk.END, f"关键词: {keyword}\n")
                        self.keyword_result_text.insert(tk.END, f"偏移: 0x{info['offset']:08X}\n")
                        self.keyword_result_text.insert(tk.END, f"上下文: {info['context']}\n\n")
                        
    def analyze_structure(self):
        """分析数据结构"""
        if not self.current_file:
            return
            
        inspector = DataInspector(self.file_path.get())
        if inspector.read_file():
            result = inspector.analyze_data_structures()
            self.structure_result_text.delete(1.0, tk.END)
            if result:
                self.structure_result_text.insert(tk.END, result)
            else:
                self.structure_result_text.insert(tk.END, "数据结构分析失败")
            
    def extract_strings(self):
        """提取字符串"""
        if not self.current_file:
            return
            
        try:
            min_length = int(self.min_length_entry.get())
            extractor = DataExtractor(self.file_path.get())
            if extractor.read_file():
                strings = extractor.extract_strings(min_length)
                if strings:
                    self.extract_result_text.delete(1.0, tk.END)
                    for s in strings:
                        self.extract_result_text.insert(tk.END, f"{s}\n")
        except ValueError:
            pass
            
    def show_log_viewer(self):
        """显示日志查看器"""
        log_window = tk.Toplevel(self.root)
        log_window.title("日志查看器")
        log_window.geometry("800x600")
        LogViewer(log_window)
        
    def cleanup(self):
        """清理资源"""
        if hasattr(self, 'current_file') and self.current_file:
            self.current_file.cleanup()
        self.root.destroy()
            
if __name__ == "__main__":
    root = tk.Tk()
    app = DatAnalyzerApp(root)
    root.mainloop()