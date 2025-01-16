import struct
import mmap
from typing import Optional, Dict, Any

class FileHandler:
    """通用文件处理类"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: Optional[bytes] = None
        
    def read_file(self, chunk_size: int = 1024*1024) -> bool:
        """读取文件内容，支持大文件分块读取"""
        try:
            import mmap
            with open(self.file_path, 'rb') as f:
                # 使用内存映射文件
                self.data = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            return True
        except Exception as e:
            print(f"文件读取失败: {e}")
            return False
            
    def cleanup(self):
        """清理内存映射资源"""
        if hasattr(self, 'data') and self.data:
            self.data.close()
            
    def write_file(self, data: bytes) -> bool:
        """写入文件内容"""
        try:
            with open(self.file_path, 'wb') as f:
                f.write(data)
            return True
        except Exception as e:
            print(f"文件写入失败: {e}")
            return False
            
    def parse_header(self) -> Optional[Dict[str, Any]]:
        """解析文件头"""
        if not self.data or len(self.data) < 32:
            return None
            
        try:
            header = {
                'magic': self.data[:12].decode('ascii', errors='ignore').strip('\x00'),
                'version': struct.unpack('>I', self.data[12:16])[0],
                'file_size': struct.unpack('>I', self.data[16:20])[0],
                'timestamp': struct.unpack('>I', self.data[20:24])[0]
            }
            return header
        except Exception as e:
            print(f"文件头解析失败: {e}")
            return None
            
    def find_keyword(self, keyword: str) -> Optional[int]:
        """查找关键词"""
        if not self.data:
            return None
            
        try:
            keyword_bytes = keyword.encode('utf-8')
            return self.data.find(keyword_bytes)
        except Exception as e:
            print(f"关键词查找失败: {e}")
            return None
            
    def extract_strings(self, min_length: int = 4) -> Optional[list]:
        """提取可打印字符串"""
        if not self.data:
            return None
            
        try:
            strings = []
            current_string = ""
            
            for byte in self.data:
                if 32 <= byte <= 126:  # 可打印ASCII范围
                    current_string += chr(byte)
                else:
                    if len(current_string) >= min_length:
                        strings.append(current_string)
                    current_string = ""
                    
            if len(current_string) >= min_length:
                strings.append(current_string)
                
            return strings
        except Exception as e:
            print(f"字符串提取失败: {e}")
            return None
            
    def hex_dump(self, bytes_per_line: int = 16) -> Optional[str]:
        """生成十六进制转储"""
        if not self.data:
            return None
            
        try:
            result = ""
            for i in range(0, len(self.data), bytes_per_line):
                chunk = self.data[i:i+bytes_per_line]
                hex_str = ' '.join(f'{b:02X}' for b in chunk)
                ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
                result += f"{i:08X}  {hex_str.ljust(bytes_per_line*3)}  |{ascii_str}|\n"
            return result
        except Exception as e:
            print(f"生成十六进制转储失败: {e}")
            return None
            
    def analyze_file(self) -> Optional[dict]:
        """分析文件内容"""
        if not self.data:
            return None
            
        try:
            analysis = {
                'file_size': len(self.data),
                'is_text': self.is_text_file(),
                'strings': self.extract_strings(),
                'hex_dump': self.hex_dump()
            }
            return analysis
        except Exception as e:
            print(f"文件分析失败: {e}")
            return None
            
    def is_text_file(self) -> bool:
        """判断是否为文本文件"""
        if not self.data:
            return False
            
        try:
            text_chars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
            return bool(self.data.translate(None, text_chars))
        except Exception as e:
            print(f"判断文件类型失败: {e}")
            return False