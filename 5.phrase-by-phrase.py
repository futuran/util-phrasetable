import spacy
import gzip
import argparse
import csv

def phrasebyphrase(args):
    #sp_en = spacy.load("en_core_web_sm")
    #sp_ja = spacy.load("ja_core_news_sm")

    #en_sw = spacy.lang.en.stop_words.STOP_WORDS
    #ja_sw = spacy.lang.ja.stop_words.STOP_WORDS

    print('loading data...')
    with open(args.phrase) as f:
        reader = csv.reader(f)
        phrase_table = [row for row in reader]
    phrase_table = [(x[1], x[2]) for x in phrase_table[1:]]
    print(len(phrase_table))

    phrase_table = dict(phrase_table)


    print('translating phrase by phrase...')
    query = "In information technology and electron field , the application of nanotechnology to next generation semiconductors , high @-@ density information record technology , miniature integrated circuit elements , electric power saving displays using carbon nano @-@ tube , etc. can be expected ."
    #query = "This paper also describes the production procedure of this pressure g@@ age ."
    #ナノテクノロジー の 応用 として ， 情報技術 ・ 電子 分野 で は ， 次世代 半導体 ， 高密度 情報 記録 技術 ， 超小型 集積回路 素子 ， カーボンナノチューブ を 用い た 省電力 ディスプレイ など が 期待 できる 。 

    vocabs = query.split()
    sim_phrases = []
    aligns = []
    aligns_loc = 0
    for start in range(len(vocabs)):

        #for length in range(1,min(6,len(vocabs) - start + 1)):
        for length in range(min(5,len(vocabs) - start), 0, -1):
            en_phrase = " ".join(vocabs[start:start+length])
            print('\nen_phrase : {}'.format(en_phrase))

            try:
                ja_phrase = phrase_table[en_phrase.lower()]
                print('ja_phrase : {}'.format(ja_phrase))
                sim_phrases.append(ja_phrase)
                aligns_loc += 1 + len(ja_phrase.split()) # sepトークン + 長さ
                for i in range(length):
                    aligns.append('{}-{}'.format(start, len(vocabs) + aligns_loc + i - 1))
                    aligns.append('{}-{}'.format(len(vocabs) + aligns_loc + i - 1, start))
                break
            except:
                continue

    print(query + ' [sep] ' + ' [sep] '.join(sim_phrases))
    print(aligns)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--phrase')
    parser.add_argument('-o', '--output', default='out')


    args = parser.parse_args()

    phrasebyphrase(args)

main()