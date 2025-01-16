import struct
from dat_modifier import DatModifier

class DataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        
    def read_file(self):
        """读取.dat文件"""
        modifier = DatModifier(self.file_path)
        if modifier.read_file():
            self.data = modifier.data
            return True
        return False
        
    def extract_strings(self, min_length=4):
        """提取可打印字符串"""
        if not self.data:
            print("请先读取文件")
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
            
    def display_strings(self, min_length=4):
        """显示提取的字符串"""
        strings = self.extract_strings(min_length)
        if strings:
            print("\n提取的字符串：")
            for s in strings:
                print(f"  {s}")
        else:
            print("未找到符合条件的字符串")

if __name__ == "__main__":
    extractor = DataExtractor('SystemData.dat')
    if extractor.read_file():
        extractor.display_strings()