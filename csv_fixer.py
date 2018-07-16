#
# xmlFixer
#
import sys
import codecs
import os


def csv_fixer(in_file_name, in_encoding, out_file_name, out_encoding, separator):
    print('csv_fixer 0.1')
    print('--------------------------------------')
    print('in_file_name :', in_file_name)
    print('in_encoding  :', in_encoding)
    print('out_file_name:', out_file_name)
    print('out_encoding :', out_encoding)
    print('separator    :', separator)
    print('--------------------------------------')

    stash_line = ''
    stash_count = ''

    # open-close
    if os.path.isfile(out_file_name):
        os.remove(out_file_name)
    with open(out_file_name, 'x', encoding=out_encoding) as fo:
        with codecs.open(in_file_name, 'r', encoding=in_encoding) as fi:
            # header
            head_line = line_strip_rn(fi.readline())
            fo.writelines(head_line + '\r\n')
            cols = line_strip_rn(head_line).split(separator)
            cols_count = len(cols)
            print('* ', cols_count, cols)

            while True:
                # read line
                line = fi.readline()
                if not line: break
                line = line_strip_rn(line)  # cleans 1 rn
                # campos
                line_fields = line.split(separator)
                line_fields_count = len(line_fields)
                if line_fields_count != cols_count:
                    print("LINEA ROTA!", line_fields_count, line_fields)
                    if not stash_line:
                        stash_line = line
                        stash_count = line_fields_count
                        print("Stashed! >> ", stash_line)
                        continue
                    else:
                        line = stash_line + line
                        print("Recovered stash, now ", stash_line + separator + line)
                        stash_line = False
                        stash_count = False
                        print("Recovered stash, now ", line_fields_count + stash_count)
                        print(line)
                line = line_strip_lows(line)  # strips lows
                fo.writelines(line + '\r\n')
        fi.close()
    fo.close()

    print('--------------------------------------')
    print('READY.')


def line_strip_rn(line):
    return line.strip('\r').strip('\n')


def line_strip_lows(line):
    sal = ''
    for n in range(0, len(line) - 1):
        if ord(line[n]) < 32:
            sal += ' '
        else:
            sal += line[n]
    return sal


if __name__ == "__main__":
    csv_fixer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
