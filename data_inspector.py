import struct
from dat_modifier import DatModifier

class DataInspector:
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
        
    def find_keywords(self, keywords):
        """查找特定关键词"""
        if not self.data:
            print("请先读取文件")
            return None
            
        try:
            results = {}
            for keyword in keywords:
                keyword_bytes = keyword.encode('utf-8')
                offset = self.data.find(keyword_bytes)
                if offset != -1:
                    results[keyword] = {
                        'offset': offset,
                        'context': self.data[offset-32:offset+len(keyword_bytes)+32].hex(' '),
                        'raw_data': self.data[offset-32:offset+len(keyword_bytes)+32]
                    }
            return results
        except Exception as e:
            print(f"关键词查找失败: {e}")
            return None
            
    def display_keywords(self, keywords):
        """显示找到的关键词信息"""
        results = self.find_keywords(keywords)
        if results:
            print("\n找到的关键词：")
            for keyword, info in results.items():
                print(f"  关键词: {keyword}")
                print(f"    偏移: 0x{info['offset']:08X}")
                print(f"    上下文: {info['context']}")
        else:
            print("未找到指定的关键词")
            
    def analyze_data_structures(self, chunk_size=1024*1024):
        """分析潜在的数据结构，采用分块处理"""
        if not self.data:
            return None
            
        try:
            result = []
            array_candidates = []
            
            # 分块处理数据
            for chunk_start in range(0, len(self.data), chunk_size):
                chunk_end = min(chunk_start + chunk_size + 8, len(self.data))
                chunk = self.data[chunk_start:chunk_end]
                
                # 查找可能的数组结构
                for i in range(0, len(chunk) - 8):
                    count = struct.unpack('>I', chunk[i:i+4])[0]
                    size = struct.unpack('>I', chunk[i+4:i+8])[0]
                    if 0 < count < 1000 and 0 < size < 1000:
                        array_candidates.append({
                            'offset': chunk_start + i,
                            'count': count,
                            'size': size
                        })
                        
            # 对结果进行去重和排序
            array_candidates = sorted(
                {c['offset']: c for c in array_candidates}.values(),
                key=lambda x: x['offset']
            )
            
            if array_candidates:
                result.append("找到可能的数组结构：")
                for candidate in array_candidates[:5]:  # 显示前5个
                    result.append(f"  偏移: 0x{candidate['offset']:08X}")
                    result.append(f"    元素数量: {candidate['count']}")
                    result.append(f"    元素大小: {candidate['size']} 字节")
            else:
                result.append("未找到明显的数组结构")
                
            return '\n'.join(result)
        except Exception as e:
            print(f"数据结构分析失败: {e}")
            return None

if __name__ == "__main__":
    inspector = DataInspector('SystemData.dat')
    if inspector.read_file():
        inspector.display_keywords(['HashVer1.4', 'Kill'])
        inspector.analyze_data_structures()