from main import read_original




def read_inter(file_name):
    with open(file_name, 'r') as f:
        data = {}
        for line in f:
            args = line.strip().split('\t')
            data[args[0]] = args[1:]
        return data

if __name__ == '__main__':
    judge_map = {
        'Positive': '1',
        'Negative': '2',
        'Neutral': '3'
    }
    original_file = 'NewChina.txt'
    inter_file = 'inter.txt'
    origin = read_original(original_file)
    inter = read_inter(inter_file)
    temp = map(lambda x: inter[x[1]][0], origin)
    num_judge = temp.count('1')
    num_discuss = temp.count('2')
    num_other = temp.count('3')
    judge_correct = map(lambda x: 1 if inter[x[1]][0] == '1' and inter[x[1]][1] == judge_map[x[2]] else 0, origin)\
        .count(1)
    temp = map(lambda x: judge_map[x[2]] if inter[x[1]][0] == '2' else 0, origin)
    discuss_pos = temp.count('1')
    discuss_neg = temp.count('2')
    discuss_neu = temp.count('3')
    print('total num: {0}, judge: {1}, discuss: {2}, correct judge: {3}, discuss_positive: {4},'
          ' discuss_negative: {5}, discuss_neutral: {6}'
          .format(len(origin), num_judge, num_discuss, judge_correct, discuss_pos, discuss_neg, discuss_neu))
