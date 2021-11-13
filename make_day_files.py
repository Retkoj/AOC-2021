import sys
from pathlib import Path


def make_day_files(file_name: str):
    """
    Create ./src/[file_name].py file and ./data/[file_name].txt file
    The .py file is created with the template provided in ./stub.py

    :param file_name: Name of the .py and .txt files to be created
    """
    file_path = Path().cwd() / 'src' / (file_name + '.py')
    if file_path.exists():
        print('{} already exists'.format(file_path))
    else:
        with open(str(file_path), 'w+') as f:
            with open(str(Path().cwd() / 'stub.py'), 'r') as stub:
                f.writelines(stub.readlines())
                print('Created file {}'.format(file_path))

    input_file = Path().cwd() / 'data' / (file_name + '.txt')
    with open(str(input_file), 'w+') as i:
        i.write('')
        print('Created input file: {}'.format(input_file))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Give filename')
    else:
        name = sys.argv[1]
        make_day_files(name)
