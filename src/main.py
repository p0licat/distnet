import re
import sys
import subprocess
import os.path as osp

from tcp_structs import FileTCP

# TODO: refactor
def os_filesystem_check(directory, files_list, filetype_pattern):

    passed = True

    class CHECK_RESULTS:
        OK      = '\033[92m OK \033[0m'
        FAIL    = '\033[91m FAIL \033[0m'


    cdirpath     = directory.rstrip('/') + '/'

    flist_format = []
    for file_name in files_list:
        flist_format.append(cdirpath + file_name.strip('/'))

    # directory check, don't check files if this fails
    sys.stdout.write('Checking path: ' + cdirpath.ljust(24) + ' ... ')
    if not osp.exists(cdirpath):
        sys.stdout.write(CHECK_RESULTS.FAIL + '\n')
        sys.stderr.write('Path ' + cdirpath + ' does not exist or not accessible. Check OS.\n')
        return not passed
    elif not osp.isdir(cdirpath):
        sys.stdout.write(CHECK_RESULTS.FAIL + '\n')
        sys.stderr.write('Path ' + cdirpath + ' is not a directory. \n')
        return not passed
    else:
        sys.stdout.write(CHECK_RESULTS.OK + '\n')

    # iterate files_list, continue on verification fail with `continue` kw
    # files_list will all be checked under cdirpath
    for file in flist_format:
        cfile_path = file
        r_status = CHECK_RESULTS.OK


        # file in question
        sys.stdout.write('Checking file: ' + cfile_path.ljust(24) + ' ... ')

        # check file exists
        if not osp.exists(cfile_path):
            passed = False
            r_status = CHECK_RESULTS.FAIL
            sys.stdout.write(r_status + '\n')
            sys.stderr.write('File ' + cfile_path + ' does not exist. Is this Linux? ...\n')
            continue

        # is file type
        if not osp.isfile(cfile_path):
            passed = False
            r_status = CHECK_RESULTS.FAIL
            sys.stdout.write(r_status + '\n')
            sys.stderr.write('Check filesystem integrity. Wrong file type of ' + cfile_path + ' ...')
            continue

        # file type matches pattern
        p = subprocess.Popen(['file', cfile_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        subp_out, subp_err = p.communicate()

        if (subp_err != ''):
            passed = False
            r_status = CHECK_RESULTS.FAIL
            sys.stdout.write(r_status + '\n')
            sys.stderr.write('There were errors verifying type of ' + cfile_path + ' ... \n' + subp_err + '\n')
            continue

        pattern_filetype = re.compile(r': empty$') # TODO: pattern
        regex_result = pattern_filetype.search(subp_out)
        if not regex_result:
            passed = False
            r_status = CHECK_RESULTS.FAIL
            sys.stdout.write(r_status + '\n')
            sys.stderr.write('File type of ' + cfile_path + ' does not correspond. \n')
            continue

        # depth level 0, no if statement passed
        sys.stdout.write(r_status + '\n')

    return passed


def main():
    if os_filesystem_check(directory='/proc/net///', files_list=[
        '/tcp',
        '//tcp6',
        'udp',
        'udp6'
    ], filetype_pattern=': empty$'):
        with open('/proc/net/tcp', 'r') as ftcp:
            print(ftcp.read())
        with open('/proc/net/tcp6', 'r') as ftcp:
            print(ftcp.read())

    ftcp = FileTCP('/proc/net/tcp')
    ftcp.read_tcp_struct()
    ftcp.print_entries()

    sys.stdout.write("Done.\n")
    exit(0)

if __name__ == '__main__':
    main()
