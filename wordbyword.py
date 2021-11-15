import spacy
import gzip
import argparse

def wordbyword(args):
    #sp_en = spacy.load("en_core_web_sm")
    #sp_ja = spacy.load("ja_core_news_sm")

    #en_sw = spacy.lang.en.stop_words.STOP_WORDS
    #ja_sw = spacy.lang.ja.stop_words.STOP_WORDS

    #print(en_sw)
    #print(ja_sw)

    #ja_symbol = set(['、', '。', '！', '？', '，', '（', '）','・','：', '；', '「', '」', '『', '』', '　', '＊'])


    print('loading data...')
    with gzip.open(args.phrase, mode='rt', encoding='utf-8') as f:
        ptable = f.readlines()

    ptable = [line.strip().split(' ||| ') for line in ptable]
    pdict = dict((line[0], line[1]) for line in ptable)
    print(ptable[0])
    print(pdict["information"])

    print('translating word by word...')

    query = "In information technology and electron field , the application of nanotechnology to next generation semiconductors , high @-@ density information record technology , miniature integrated circuit elements , electric power saving displays using carbon nano @-@ tube , etc. can be expected ."
    #ナノテクノロジー の 応用 として ， 情報技術 ・ 電子 分野 で は ， 次世代 半導体 ， 高密度 情報 記録 技術 ， 超小型 集積回路 素子 ， カーボンナノチューブ を 用い た 省電力 ディスプレイ など が 期待 できる 。 

    for start in range(len(query.split())):
        for length in range(1,6):
            en_phrase = query.lower().split()[start:start+length]
            print('\nen_phrase:{}'.format(en_phrase))
            if ' '.join(en_phrase) in pdict:
                print('ja_phrase:{}'.format(pdict[' '.join(en_phrase)]))


    #with gzip.open(args.output, mode='wt', encoding='utf-8') as f:
    #    f.writelines(new_ptable)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--phrase')
    #parser.add_argument('-o', '--output', default='out')


    args = parser.parse_args()

    wordbyword(args)

main()