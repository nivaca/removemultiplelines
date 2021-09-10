import os
import re

directory: str = ''  # local directory
extensions: list[str] = ['.org']
makebackup: bool = True


def get_files() -> list[str]:
    files: list[str] = []
    allfilenames = os.listdir(directory + '.')
    for fi in allfilenames:
        ext = os.path.splitext(fi)[1]
        # check if file of proper extension
        if ext.lower() in extensions:
            files.append(fi)
    # returns a lists of file objects
    return files


def removemultiplelines(fn: str) -> bool:
    changed = False
    with open(fn) as orig:
        out = orig.read()
        patternlist: list[tuple[str, str]] = [
            (r' +\n', r'\n'),
            (r'\n{3,}', r'\n\n'),
            (r'\n{2,}$', r'\n')
        ]
        for pat in patternlist:
            if re.search(pat[0], out):
                out = re.sub(pat[0], pat[1], out)
                changed = True
        if not changed:
            return False
        tmpfn = f"{fn}.tmp"
        with open(tmpfn, mode="w") as tmpf:
            tmpf.write(out)
        if makebackup:
            os.rename(fn, f"{fn}.bak")
        else:
            os.remove(fn)
        os.rename(tmpfn, fn)
        return True


def main():
    files = get_files()
    count = 0
    for fn in files:
        print(f"Processing {fn}...")
        if removemultiplelines(fn):
            print(f"  Removed multiple lines in: {fn}...")
            count += 1
        else:
            print(f"  Skipped: {fn}...")

    print(f"Removed multiple lines in {count} file(s)")


if __name__ == "__main__":
    main()
