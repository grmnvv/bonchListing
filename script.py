import os
import re
import argparse

def process_file(file_name, output_file, ignore_list, ignore_extensions):
    basename = os.path.basename(file_name)
    if basename in ignore_list or os.path.splitext(basename)[1] in ignore_extensions:
        return

    try:
        with open(file_name, 'r') as file:
            content = file.read()

            # удаляем HTML разметку
            content = re.sub(r'return\s*\(.*\)', '', content, flags=re.DOTALL)

            # Имя файла на отдельной строке
            output_file.write(f"{basename}:\n{content}\n\n")
    except Exception as e:
        print(f"Ошибка при чтении файла {file_name}. Ошибка: {str(e)}")


def process_directory(dir_path, output_file, ignore_list, ignore_extensions):
    for root, dirs, files in os.walk(dir_path):
        path_parts = root.split(os.sep)
        if any(part in ignore_list for part in path_parts):
            continue

        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, output_file, ignore_list, ignore_extensions)


def get_ignore_list_and_extensions(ignore_file_path):
    try:
        with open(ignore_file_path, 'r') as file:
            lines = file.read().splitlines()
            filenames_index = lines.index('filenames:') + 1
            extensions_index = lines.index('extensions:') + 1

            filenames = []
            while filenames_index < extensions_index - 1:
                filenames.append(lines[filenames_index].strip())
                filenames_index += 1

            extensions = []
            while extensions_index < len(lines):
                extensions.append(lines[extensions_index].strip())
                extensions_index += 1

            return filenames, extensions
    except Exception as e:
        print(f"Ошибка при чтении файла. Ошибка: {str(e)}")
        return [], []


def main(directory):
    ignore_list, ignore_extensions = get_ignore_list_and_extensions("ignore.txt")

    with open("output.txt", 'w') as output_file:
        process_directory(directory, output_file, ignore_list, ignore_extensions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process files in a directory.')
    parser.add_argument('directory', type=str, help='The directory to process.')

    args = parser.parse_args()

    main(args.directory)
