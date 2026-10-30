"""Virtual File System"""

import posixpath
import zipfile


class VFS:
    """Class of VFS based on zip archive"""

    def __init__(self, zip_path: str):
        self.zip_path = zip_path
        self.pwd = "/"
        self.dirs = {"/"}
        self.files = set()

        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                for name in zf.namelist():
                    is_dir = name.endswith("/")
                    parts = name.strip("/").split("/")

                    current = ""
                    for i, part in enumerate(parts):
                        if not part:
                            continue

                        current += "/" + part

                        if i == len(parts) - 1 and not is_dir:
                            self.files.add(current)
                        else:
                            self.dirs.add(current)

        except (FileNotFoundError, zipfile.BadZipFile):
            print(f"emulator: cannot open VFS archive '{zip_path}'")

    def ls(self) -> list[str]:
        """return list of files and directoryes"""
        items = set()
        prefix = self.pwd if self.pwd == "/" else self.pwd + "/"

        for path in self.dirs.union(self.files):
            if path.startswith(prefix) and path != self.pwd:
                relative = path[len(prefix) :]
                child = relative.split("/")[0]
                items.add(child)

        return sorted(list(items))

    def cd(self, path: str) -> bool:
        """change directory, return True"""
        if path.startswith("/"):
            new_pwd = posixpath.normpath(path)
        else:
            new_pwd = posixpath.normpath(posixpath.join(self.pwd, path))

        if new_pwd in self.dirs:
            self.pwd = new_pwd
            return True
        elif new_pwd in self.files:
            print(f"cd: not a directory: {path}")
            return False
        else:
            print(f"cd: no such file or directory: {path}")
            return False

    def read_file(self, filename: str) -> list[str] | None:
        """Read text file from zip and return its lines."""
        if filename.startswith("/"):
            target = posixpath.normpath(filename)
        else:
            target = posixpath.normpath(posixpath.join(self.pwd, filename))

        if target not in self.files:
            print(f"tail: cannot open '{filename}' for reading: No such file")
            return None

        zip_target = target.lstrip("/")
        try:
            with zipfile.ZipFile(self.zip_path, "r") as zf:
                with zf.open(zip_target) as f:
                    content = f.read().decode("utf-8")
                    return content.splitlines()
        except Exception as e:
            print(f"tail: error reading file: {e}")
            return None

    def rmdir(self, target_dir: str) -> bool:
        """Remove empty directory from VFS."""
        if target_dir.startswith("/"):
            target = posixpath.normpath(target_dir)
        else:
            target = posixpath.normpath(posixpath.join(self.pwd, target_dir))

        if target not in self.dirs:
            print(f"rmdir: failed to remove '{target_dir}': No such file or directory")
            return False

        if target == "/":
            print(
                f"rmdir: failed to remove '{target_dir}': Cannot remove root directory"
            )
            return False

        if target == self.pwd or self.pwd.startswith(target + "/"):
            print(f"rmdir: failed to remove '{target_dir}': Device or resource busy")
            return False

        prefix = target + "/"

        for f in self.files:
            if f.startswith(prefix):
                print(f"rmdir: failed to remove '{target_dir}': Directory not empty")
                return False

        for d in self.dirs:
            if d.startswith(prefix) and d != target:
                print(f"rmdir: failed to remove '{target_dir}': Directory not empty")
                return False

        self.dirs.remove(target)
        return True
