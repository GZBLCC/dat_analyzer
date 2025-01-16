from file_handler import FileHandler
import mmap

class DatModifier(FileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)
        
    def read_file(self):
        """读取.dat文件"""
        result = super().read_file()
        if result and isinstance(self.data, mmap.mmap):
            # 将内存映射文件转换为bytes对象以便修改
            self.data = bytes(self.data)
        return result
            
    def modify_data(self, offset, new_value):
        """修改指定偏移量的数据"""
        if not self.data:
            print("请先读取文件")
            return False
            
        if offset >= len(self.data):
            print("偏移量超出文件范围")
            return False
            
        # 将数据转换为字节数组以便修改
        data = bytearray(self.data)
        print(f"Before modification at offset {offset}: 0x{data[offset]:02X}")
        data[offset] = new_value
        print(f"After modification at offset {offset}: 0x{data[offset]:02X}")
        self.data = bytes(data)
        return True
        
    def save_file(self, output_path=None):
        """保存修改后的文件"""
        if not self.data:
            print("没有数据可保存")
            return False
            
        save_path = output_path or self.file_path
        try:
            with open(save_path, 'wb') as f:
                f.write(self.data)
            return True
        except Exception as e:
            print(f"保存文件失败: {e}")
            return False

def display_hex_view(data, bytes_per_line=16):
    """显示十六进制和ASCII视图"""
    for i in range(0, len(data), bytes_per_line):
        chunk = data[i:i+bytes_per_line]
        hex_str = ' '.join(f'{b:02X}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        print(f"{i:08X}  {hex_str.ljust(bytes_per_line*3)}  |{ascii_str}|")

def main():
    print("=== DAT文件修改器 ===")
    file_path = input("请输入要修改的.dat文件路径: ")
    
    modifier = DatModifier(file_path)
    
    if not modifier.read_file():
        return
        
    while True:
        print("\n文件信息：")
        print(f"文件大小: {len(modifier.data)} 字节")
        print("\n当前文件内容：")
        display_hex_view(modifier.data)
        
        print("\n操作选项：")
        print("1. 修改字节")
        print("2. 保存文件")
        print("3. 退出")
        
        choice = input("请选择操作 (1-3): ")
        
        if choice == '1':
            try:
                print("\n当前文件内容：")
                display_hex_view(modifier.data)
                
                offset = input("请输入要修改的字节位置（十六进制或十进制，例如0x10或16）：")
                offset = int(offset, 0)
                
                if offset < 0 or offset >= len(modifier.data):
                    print("错误：偏移量超出文件范围")
                    continue
                    
                current_value = modifier.data[offset]
                print(f"\n偏移量 {offset} (0x{offset:X}) 的当前值：0x{current_value:02X} ({current_value})")
                
                new_value = input("请输入新值（0-255，十六进制加0x前缀）：")
                new_value = int(new_value, 0)
                
                if not 0 <= new_value <= 255:
                    print("错误：值必须在0到255之间")
                    continue
                    
                if modifier.modify_data(offset, new_value):
                    print("修改成功")
                    print("\n修改后的内容：")
                    display_hex_view(modifier.data)
                else:
                    print("修改失败")
                    
            except ValueError:
                print("错误：请输入有效的数字")
                
        elif choice == '2':
            output_path = input("请输入保存路径（留空覆盖原文件）: ")
            if modifier.save_file(output_path or None):
                print("文件保存成功")
            else:
                print("文件保存失败")
                
        elif choice == '3':
            print("退出程序")
            break
            
        else:
            print("无效选择，请输入1-3")

if __name__ == "__main__":
    main()