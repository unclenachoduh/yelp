import sys

input_file = sys.argv[1]
output_dir = sys.argv[2]

if output_dir[:-1] != "/":
    output_dir += "/"

output_name = input_file

if "/" in input_file:
    input_short = input_file.split("/")
    output_name = input_short[-1]

input_read = open(input_file)
input_text = input_read.readlines()
# input_lines = input_text.split("\n")

writeline = ''
count = 0
writefile = open(output_dir + output_name + "_tenth", "w+")
for line in input_text:
    if line != '':
        # if count == 0:
        #     print(line)

        if count % 10 == 0:
            writefile.write(line)
        count += 1

writefile.close()
