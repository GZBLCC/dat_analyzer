from file_handler import FileHandler

class DatParser(FileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)
        
    def parse_header(self):
        """解析文件头"""
        if not self.data:
            print("请先读取文件")
            return None
            
        # 解析文件头
        header = {}
        try:
            # 读取文件标识符
            header['magic'] = self.data[:12].decode('ascii', errors='ignore')
            
            # 读取版本号
            header['version'] = struct.unpack('>I', self.data[12:16])[0]
            
            # 读取文件大小
            header['file_size'] = struct.unpack('>I', self.data[16:20])[0]
            
            # 读取创建时间戳
            header['timestamp'] = struct.unpack('>I', self.data[20:24])[0]
            
            return header
        except Exception as e:
            print(f"解析文件头失败: {e}")
            return None
            
    def display_header(self):
        """显示文件头信息"""
        header = self.parse_header()
        if header:
            print("文件头信息：")
            print(f"  文件标识符: {header['magic']}")
            print(f"  版本号: {header['version']}")
            print(f"  文件大小: {header['file_size']} 字节")
            print(f"  创建时间戳: {header['timestamp']}")
        else:
            print("无法解析文件头")
            
    def parse_data_sections(self):
        """解析数据段"""
        if not self.data:
            print("请先读取文件")
            return None
            
        try:
            # 跳过文件头（32字节）
            offset = 32
            sections = []
            
            # 读取段数量
            num_sections = struct.unpack('>I', self.data[offset:offset+4])[0]
            offset += 4
            
            for _ in range(num_sections):
                # 读取段类型
                section_type = struct.unpack('>I', self.data[offset:offset+4])[0]
                offset += 4
                
                # 读取段大小
                section_size = struct.unpack('>I', self.data[offset:offset+4])[0]
                offset += 4
                
                # 保存段信息
                sections.append({
                    'type': section_type,
                    'size': section_size,
                    'offset': offset
                })
                
                # 跳到下一段
                offset += section_size
                
            return sections
        except Exception as e:
            print(f"解析数据段失败: {e}")
            return None
            
    def display_sections(self):
        """显示数据段信息"""
        sections = self.parse_data_sections()
        if sections:
            print("\n数据段信息：")
            for i, section in enumerate(sections):
                print(f"  段 {i+1}:")
                print(f"    类型: 0x{section['type']:08X}")
                print(f"    大小: {section['size']} 字节")
                print(f"    偏移: 0x{section['offset']:08X}")
        else:
            print("无法解析数据段")

if __name__ == "__main__":
    parser = DatParser('SystemData.dat')
    if parser.read_file():
        parser.display_header()