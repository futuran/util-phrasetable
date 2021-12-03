import argparse
import csv
import gzip

def gz_to_csv(args):
    print('loading data...')
    with gzip.open(args.phrase, mode='rt', encoding='utf-8') as f:
        ptable = f.readlines()

    ptable_csv = [['English','Japanese','phi_fe','lex_fe','phi_ef','lex_ef','Alignment','Counts']]
    for line in ptable:
        tmp = line.strip().split('|||')
        out_tmp = []
        out_tmp.append(tmp[0].strip())  # English Phrase
        out_tmp.append(tmp[1].strip())  # Japanese Phrase
        for x in tmp[2].strip().split():# 確率
            out_tmp.append(x)
        out_tmp.append(tmp[3].strip())
        out_tmp.append(tmp[4].strip())
        ptable_csv.append(out_tmp)

    with open(args.output+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(ptable_csv)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--phrase')
    parser.add_argument('-o', '--output', default='out')

    args = parser.parse_args()

    gz_to_csv(args)

main()