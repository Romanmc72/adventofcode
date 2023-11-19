#!/usr/bin/env python3
"""
Part 1
------
Reconstruct the filesystem using the terminal history

Find out *ALL* directories that are <= 100,000 bytes
and total their bytes together.

Part 2
------
Find the one directory to delete that is a small as possible that will
free up 30,000,000b of the total available 70,000,000b space on the device

Kinda hate this code, but it "works"
"""
import os
from typing import List

from input import get_data


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def __str__(self) -> str:
        return f"{self.name} (file size={self.size})"

    def __repr__(self) -> str:
        return self.name


class Directory:
    def __init__(
        self,
        name: str,
        files: list[File] = None,
        directories: list = None,
        size: int = 0,
    ):
        self.name = name
        self.files = files or []
        self.directories = directories or []
        self.size = size

    def ls(self) -> None:
        for file in self.files:
            print(file)
        for directory in self.directories:
            print(directory)

    def __str__(self) -> str:
        return f"{self.name} (dir)"

    def __repr__(self) -> str:
        return self.name


class FileSystem:
    def __init__(self):
        self.pwd = [Directory(name="/")]

    @property
    def current_directory(self):
        return self.pwd[-1]

    def cd(self, directory_name):
        if directory_name == "/":
            self.pwd = [self.pwd[0]]
            return None
        for directory in self.current_directory.directories:
            if directory.name == directory_name:
                self.pwd.append(directory)
                return None
        raise ValueError(f"Directory {directory_name} not found!")

    def cd_back(self):
        if len(self.pwd) <= 1:
            pass
        else:
            self.pwd.pop()

    def ls(self):
        self.current_directory.ls()

    def sum_up_all_directories(
        self,
        threshold: int,
        directory: Directory = None,
        parent: str = None,
        less_than: bool = True,
    ):
        if not directory:
            self.running_total = 0
            self.candidates = []
            directory = self.pwd[0]
        file_sizes = sum([f.size for f in directory.files])
        sub_directory_sizes = 0
        for sub_directory in directory.directories:
            sub_directory_sizes += self.sum_up_all_directories(
                threshold=threshold,
                directory=sub_directory,
                parent=os.path.join(parent or "", directory.name),
            )
        total_size = file_sizes + sub_directory_sizes
        directory.size = total_size
        if less_than:
            if total_size <= threshold:
                self.running_total += total_size
                self.candidates.append(directory)
        else:
            if total_size >= threshold:
                self.running_total += total_size
                self.candidates.append(directory)
        return file_sizes + sub_directory_sizes


def parse_directories(instructions: List[str]) -> FileSystem:
    filesystem = FileSystem()
    ls_ing = False
    for instruction in instructions:
        if instruction.startswith("$"):
            ls_ing = False
            command = instruction.split("$ ")[1]
            if command.startswith("cd"):
                directory_name = command.split(" ")[-1]
                if directory_name == "..":
                    filesystem.cd_back()
                else:
                    filesystem.cd(directory_name)
            elif command == "ls":
                ls_ing = True
            else:
                raise ValueError(f"What did you even run? Unrecognized {instruction}")
        else:
            if ls_ing:
                identifier, name = instruction.split(" ")
                if name in set(
                    [f.name for f in filesystem.current_directory.files]
                    + [f.name for f in filesystem.current_directory.directories]
                ):
                    print(
                        f"WARNING: File {name} is already in directory {os.path.join(*filesystem.pwd)}"
                    )
                try:
                    file_size = int(identifier)
                    filesystem.current_directory.files.append(File(name, file_size))
                except ValueError:
                    if identifier == "dir":
                        filesystem.current_directory.directories.append(Directory(name))
                    else:
                        raise ValueError(
                            f"This is neither file nor directory {instruction}"
                        )
            else:
                print(f"What even is this? {instruction}")
    return filesystem


def main(threshold, free_space=30000000, available_space=70000000):
    instructions = get_data()
    filesystem = parse_directories(instructions)
    filesystem.sum_up_all_directories(threshold)
    print(f"Directories within the threshold are totaled to {filesystem.running_total}")
    total_fs = filesystem.sum_up_all_directories(available_space)
    print(f"Total occupied space {total_fs}")
    currently_free_space = available_space - total_fs
    additional_free_space_needed = free_space - currently_free_space
    print(f"Additional Free space needed {additional_free_space_needed}")
    filesystem.sum_up_all_directories(additional_free_space_needed, less_than=False)
    wtf = []
    for d in filesystem.candidates:
        if d.size >= additional_free_space_needed:
            wtf.append(d)
    wtf.sort(key=lambda d: d.size * -1)
    print(f"Delete this one! {wtf}")


def main1(threshold):
    instructions = get_data()
    filesystem = parse_directories(instructions)
    filesystem.sum_up_all_directories(threshold)
    print(f"Directories within the threshold are totaled to {filesystem.running_total}")


def main2(free_space, available_space):
    instructions = get_data()
    filesystem = parse_directories(instructions)
    total_fs = filesystem.sum_up_all_directories(available_space, less_than=False)
    print(f"Total occupied space {total_fs}")
    currently_free_space = available_space - total_fs
    additional_free_space_needed = free_space - currently_free_space
    print(f"Additional Free space needed {additional_free_space_needed}")
    filesystem.candidates.sort(key=lambda d: d.size)
    for d in filesystem.candidates:
        if d.size >= additional_free_space_needed:
            print(f"Delete this one! {d.size}")
            break


if __name__ == "__main__":
    main1(100000)
    main2(30000000, 70000000)
