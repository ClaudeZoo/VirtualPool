# Author :Zhu Zichen
# Date : 2016/3/23
# mode 1 : file
# mode 2: directory
import os, sys, getopt


def get_data(input_filename):
    if os.path.exists(input_filename):
        input_file = open(input_filename, "r")
        origin_data = input_file.readlines()
        length = len(origin_data)
        result = list()
        i = 1
        for line in origin_data:
            percent = "%.2f" % ((i * 1.0 / length) * 100)
            result.append(line.strip() + " " + str(percent))
            i += 1
        input_file.close()
    else:
        print "Invalid File name."
        sys.exit()
    return '\n'.join(result)


def file_supplement(input_filename, output_filename):
    data = get_data(input_filename)
    output_file = open((output_filename), "w")
    output_file.write(data)
    output_file.close()


def directory_supplement(input_directory, output_directory):
    try:
        os.makedirs(output_directory)
    except Exception as e:
        print e
        sys.exit()

    if os.path.exists(input_directory):
        for parent, dirnames, filenames in os.walk(input_directory):
            for filename in filenames:
                output_filename = filename + "-out"
                data = get_data(os.path.join(parent, filename))
                output_filepath = os.path.join(output_directory, output_filename)
                output_file = open(output_filepath, "w")
                output_file.write(data)
                output_file.close()

    else:
        print "Invalid File name."


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "r")
    if len(args) == 1:
        input_name = args[0]
        output_name = input_name + "-out"
    elif len(args) == 2 and args[0] != args[1]:
        input_name = args[0]
        output_name = args[1]
    else:
        print "Invalid parameters."
        sys.exit()

    directory_flag = False
    for opt, value in opts:
        if opt == "-r":
            directory_flag = True
    if directory_flag:
        directory_supplement(input_name, output_name)
    else:
        file_supplement(input_name, output_name)
