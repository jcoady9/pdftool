#! python3

import argparse
import os.path
import string

from PyPDF2 import PdfMerger


def only_has_certain_chars(arg_string):
    valid_chars = string.digits + ',-'
    for c in arg_string:
        if c not in valid_chars:
            return False
    return True


def parse_file_args(file_args):
    files = []
    for arg in file_args:
        _, ext = os.path.splitext(arg)
        if ext != '':
            if ext == '.pdf':
                files.append([arg])
            else:
                raise AttributeError('File \'{}\' must be pdf!!!'.format(arg))
        elif only_has_certain_chars(arg):
            if len(files) <= 0:
                raise AttributeError('\'{}\' is not a file!!!'.format(arg))
            files[-1].append(arg)
    return files


def parse_ranges(pages_str):
    sections = pages_str.split(',')
    if len(sections) == 1:
        return tuple([int(sections[0])])
    ranges = []
    for section in sections:
        copy_range = section.split('-')
        range_len = len(copy_range)
        if range_len in [1, 2]:
            ranges.append(tuple(map(int, copy_range)))
        else:
            raise ValueError('Too many \'-\'. Invalid Range!!!')
    return ranges


# TODO: Refactor Me.
def merge(files):
    merger = PdfMerger()
    for file, page_ranges in files:
        if page_ranges:
            print(page_ranges)
            for page_rage in page_ranges:
                if len(page_rage) == 2:
                    merger.append(fileobj=file, pages=(page_rage[0]-1, page_rage[1]))
                elif len(page_rage) == 1:
                    merger.append(fileobj=file, pages=(page_rage[0]-1, page_rage[0]))
        else:
            merger.append(file)
    merger.write('result.pdf')
    merger.close()


# TODO: Implement Me.
def split(file):
    pass


def main():
    parser = argparse.ArgumentParser(description='A tool for modifying pdf files.')
    parser.add_argument('--merge', nargs='+', type=str, help='merge one or more pdf files')
    parser.add_argument('--split', nargs='+', type=str, help='split a pdf into two or more files')
    args = parser.parse_args()

    if args.merge:
        files = parse_file_args(args.merge)
        for f in files:
            if len(f) == 2:
                f[1] = parse_ranges(f[1])
            else:
                f.append(None)
        merge(files)

    if args.split:
        # To be Implemented...
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
