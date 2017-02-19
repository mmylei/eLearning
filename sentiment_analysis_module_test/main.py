import os


def read_original(file_name):
    with open(file_name, 'r') as f:
        data = []
        line = f.readline()
        while line:
            data.append([line.strip(), f.readline().strip(), f.readline().strip()])
            line = f.readline()
        return data

if __name__ == '__main__':
    original_file = 'study_groups.txt'
    inter_file = 'inter02.txt'
    data = read_original(original_file)
    counter = 0
    if inter_file in os.listdir('.'):
        with open(inter_file, 'r') as f:
            for line in f:
                counter += 1
    with open(inter_file, 'a') as f:
        for i in range(counter, len(data)):
            os.system('clear')
            print(data[i][1])
            print(data[i][2])
            type = ''
            while type not in ['1', '2', '3']:
                type = raw_input('1: judgement\n2: discuss\n3: other\n')
            f.write(data[i][1] + '\t')
            f.write(type)
            if type == '1':
                label = ''
                while label not in ['1', '2', '3']:
                    label = raw_input('1: positive\n2: negative\n3: neutral\n')
                f.write('\t' + label)
            f.write('\n')
            f.flush()
