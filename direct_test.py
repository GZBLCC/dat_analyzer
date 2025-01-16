from dat_modifier import DatModifier

# 创建修改器实例
modifier = DatModifier('test.dat')

# 读取文件
if modifier.read_file():
    print("文件读取成功")
    
    # 修改偏移量2的数据为0xFF
    if modifier.modify_data(2, 0xFF):
        print("数据修改成功")
        
        # 保存修改后的文件
        if modifier.save_file('direct_modified.dat'):
            print("文件保存成功")
            print("请查看direct_modified.dat文件")
        else:
            print("文件保存失败")
    else:
        print("数据修改失败")
else:
    print("文件读取失败")