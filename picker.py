import os
import argparse
import shutil


def find_and_sync_files(path, dry_run=False):
    raw_formats = ['.cr3', '.raf']  # 添加你需要支持的其他原始文件格式

    raw_files = set()
    jpg_files = set()

    # 遍历给定路径及所有子路径
    for root, dirs, files in os.walk(path):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in raw_formats:
                raw_files.add((os.path.splitext(file)[0], file_ext))  # 保持文件名和格式
            elif file_ext == '.jpg':
                jpg_files.add(os.path.splitext(file)[0])

    # 找出存在原始格式但不存在对应.jpg的文件
    to_delete = {name for name, ext in raw_files if name not in jpg_files}

    # 根据dry-run标志进行操作
    cnt = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            base_name, file_ext = os.path.splitext(file)[0], os.path.splitext(file)[1].lower()
            if (base_name, file_ext) in raw_files and base_name in to_delete:
                file_path = os.path.join(root, file)
                cnt += 1
                if dry_run:
                    print(f"Would delete: {file_path}")
                else:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
    print(f"Totally deleted {cnt} files")


def organize_files(path, dry_run):
    # 检查路径是否存在
    if not os.path.exists(path):
        print(f"Error: Path not found: {path}")
        return
    
    # 定义支持的图片文件扩展名
    supported_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.cr3', '.raf'}
    
    # 获取路径下所有文件
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    # 确定需要创建的目录
    needed_directories = set()
    for file in files:
        extension = os.path.splitext(file)[1].lower()
        if extension in supported_extensions:
            needed_directories.add(extension.lstrip('.'))

    # 创建所有需要的目录
    for directory in needed_directories:
        target_folder = os.path.join(path, directory)
        if not os.path.exists(target_folder):
            if dry_run:
                print(f"Would create directory: {target_folder}")
            else:
                try:
                    os.makedirs(target_folder)
                    print(f"Created directory: {target_folder}")
                except Exception as e:
                    print(f"Error: Failed to create directory {target_folder}: {e}")

    # 移动文件到对应的目录
    for file in files:
        extension = os.path.splitext(file)[1].lower()
        if extension in supported_extensions:
            target_folder = os.path.join(path, extension.lstrip('.'))
            target_path = os.path.join(target_folder, file)
            if dry_run:
                print(f"Would move {file} to {target_path}")
            else:
                try:
                    shutil.move(os.path.join(path, file), target_path)
                    print(f"Moved {file} to {target_path}")
                except Exception as e:
                    print(f"Error: Failed to move {file} to {target_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="File management tool")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actually changing any files.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # 创建 del 子命令
    parser_del = subparsers.add_parser('del', help='Delete .cr3 files without a corresponding .jpg file')
    parser_del.add_argument("path", help="Path to scan for .cr3 and .jpg files.")
    parser_del.set_defaults(func=find_and_sync_files)
    
    # 创建 org 子命令
    parser_org = subparsers.add_parser('org', help='Organize files by type')
    parser_org.add_argument("path", help="Path to scan and organize files.")
    parser_org.set_defaults(func=organize_files)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        # 从顶级解析器传递 dry_run 参数
        args.func(args.path, args.dry_run)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
