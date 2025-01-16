import struct
from collections import Counter
from dat_modifier import DatModifier

class DataAnalyzer:
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
        
    def analyze_patterns(self):
        """分析数据模式"""
        if not self.data:
            print("请先读取文件")
            return None
            
        try:
            # 分析字节频率
            byte_freq = Counter(self.data)
            print("\n字节频率分析：")
            for byte, freq in byte_freq.most_common(10):
                print(f"  字节 0x{byte:02X}: {freq} 次")
                
            # 查找常见模式
            patterns = {}
            for i in range(len(self.data) - 4):
                pattern = self.data[i:i+4]
                patterns[pattern] = patterns.get(pattern, 0) + 1
                
            print("\n常见4字节模式：")
            for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  模式 {pattern.hex(' ')}: {count} 次")
                
        except Exception as e:
            print(f"数据分析失败: {e}")
            return None

if __name__ == "__main__":
    analyzer = DataAnalyzer('SystemData.dat')
    if analyzer.read_file():
        analyzer.analyze_patterns()