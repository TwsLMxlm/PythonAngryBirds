import os

# 读取文件夹中特定类型文件的数量
def count_files_in_directory(directory, file_extension):
    count = 0
    for file_name in os.listdir(directory):
        # 检查文件是否以指定扩展名结尾
        if file_name.endswith(file_extension):
            count += 1
    print(f"关卡数量：{count}")
    return count