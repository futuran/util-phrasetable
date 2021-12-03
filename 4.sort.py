import spacy
import gzip
import argparse
import pandas as pd

def sort(args):

    print('loading data...')
    df = pd.read_csv(args.phrase)

    print('sorting data...')
    # ソート
    df.sort_values(['English','phi_ef'], ascending=[True,False])
    # 重複排除
    dfd = df.sort_values(['English','phi_ef'], ascending=[True,False]).drop_duplicates(subset=['English'])

    # 閾値を超えたもののみ
    dfd = dfd[dfd['phi_ef']>0.1]

    # 保存
    dfd.to_csv(args.output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--phrase')
    parser.add_argument('-o', '--output', default='out')

    args = parser.parse_args()

    sort(args)

main()