"""Virtual File System"""

import posixpath
import zipfile


class VFS:
    """Class of VFS based on zip archive"""

    def __init__(self, zip_path: str):
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
