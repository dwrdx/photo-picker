import os
import argparse

def find_and_sync_files(path, dry_run=False):
    cr3_files = set()
    jpg_files = set()

    # 遍历给定路径及所有子路径
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith('.cr3'):
                cr3_files.add(os.path.splitext(file)[0])
            elif file.lower().endswith('.jpg'):
                jpg_files.add(os.path.splitext(file)[0])

    # 找出存在.cr3但不存在对应.jpg的文件
    to_delete = cr3_files - jpg_files

    # 根据dry-run标志进行操作
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[0] in to_delete and file.lower().endswith('.cr3'):
                file_path = os.path.join(root, file)
                if dry_run:
                    print(f"Would delete: {file_path}")
                else:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Sync .cr3 files with .jpg files by deleting .cr3 files without a corresponding .jpg file.")
    parser.add_argument("path", help="Path to scan for .cr3 and .jpg files.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actually deleting any files.")

    args = parser.parse_args()
    find_and_sync_files(args.path, args.dry_run)

if __name__ == "__main__":
    main()
