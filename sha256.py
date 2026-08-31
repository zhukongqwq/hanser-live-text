#!/usr/bin/env python3

import os
import sys
import json
import hashlib
import argparse


def sha256_file(filepath: str, blocksize: int = 65536) -> str:
    """计算文件的 SHA256 哈希值（分块读取，避免大文件内存溢出）"""
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(blocksize), b''):
            sha.update(chunk)
    return sha.hexdigest()


def main():
    root = os.path.abspath("data")
    print(root)
    if not os.path.isdir(root):
        print(f"错误: '{root}' 不是有效的目录", file=sys.stderr)
        sys.exit(1)

    result = {}
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, f"{root}\\..").replace(os.sep, '/')
            try:
                sha = sha256_file(full_path)
                result[rel_path] = sha
            except Exception as e:
                # 如果某个文件无法读取（权限、损坏等），打印警告并跳过
                print(f"警告: 无法计算 {rel_path}: {e}", file=sys.stderr)
                continue

    with open("list.json", 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ 已生成 list.json，包含 {len(result)} 个文件的 SHA256 值")


if __name__ == '__main__':
    main()