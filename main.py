import os
import time
import sys

def get_files_with_absolute_paths(directory, count = 5):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            try:
                atime = os.path.getatime(filepath)
                size = os.path.getsize(filepath)
                abs_path = os.path.abspath(filepath)
                files.append((filepath, abs_path, atime, size))
            except (FileNotFoundError, PermissionError):
                continue
    
    files.sort(key=lambda x: x[2])
    return files[:count]

def bytes_to_human_readable(size):
    """
    Convert a size in bytes to a human-readable format.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"  # case size is larger than TB

def display_files(files):
    """
    Display file information in a user-friendly format.
    """
    print("\nCele mai vechi fișiere accesate:")
    count = 1
    for filepath, abs_path, atime, size in files:
        print(f"{count}")
        print(f"Path: {filepath}")
        print(f"Absolute Path: {abs_path}")
        print(f"Last Access Time: {time.ctime(atime)}")
        print(f"Size: {bytes_to_human_readable(size)}")
        print("-" * 40)
        count += 1

def delete_files(files):
    """
    Ask user which files to delete.
    """
    while True:
        try:
            choice = input("Introduceți numerele fișierelor de șters (separate prin virgulă), 'all' pentru a sterge toate fisierele listate sau 'q' pentru a ieși: ").strip()
            if choice.lower() == 'q':
                print("Ieșire fără a șterge fișiere.")
                break
            elif choice.lower() == 'all':
                for file in files:
                    os.remove(file[0])
                    print(f"Fișier șters: {file[0]}")
                break
            indices = list(map(int, choice.split(',')))
            for index in indices:
                if 1 <= index <= len(files):
                    os.remove(files[index - 1][0])
                    print(f"Fișier șters: {files[index - 1][0]}")
                else:
                    print(f"Număr invalid: {index}")
        except ValueError:
            print("Intrare invalidă. Asigurați-vă că introduceți numere valide.")
        except FileNotFoundError:
            print("Fișierul nu mai există deja.")
        else:
            break

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Utilizare: python script.py <cale_director> [-c <numar_fisiere>]")
        return
    
    directory = sys.argv[1]
    count = 5  # default value
    
    if len(sys.argv) == 4 and sys.argv[2] == '-c':
        try:
            count = int(sys.argv[3])
        except ValueError:
            print("Valoarea pentru -c trebuie să fie un număr întreg.")
            return
    
    if not os.path.isdir(directory):
        print(f"Director invalid: {directory}")
        return
    
    try:
        oldest_files = get_files_with_absolute_paths(directory, count)
        if not oldest_files:
            print("Nu s-au găsit fișiere.")
            return

        display_files(oldest_files)
        delete_files(oldest_files)
    except Exception as e:
        print(f"Eroare: {e}")

if __name__ == "__main__":
    main()