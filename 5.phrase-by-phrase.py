import spacy
import gzip
import argparse
import csv

import itertools
import numpy as np

# coo形式を利用するため
import scipy

# ヒートマップの描画のため
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import japanize_matplotlib  # 日本語フォントのため
import seaborn as sns


def draw_heatmap(att_mat, name_index, axis_name):
    '''
    ヒートマップ作成関数
    Parameters
    ------------
    att_mat
        アテンション行列
    axis_name : list
        軸名。x軸・y軸ともに共通。
    '''
    plt.figure(figsize = (int(len(axis_name)/3), int(len(axis_name)/3)))

    sns.heatmap(att_mat, square=True, xticklabels=axis_name, yticklabels=axis_name, linewidths=1)
    plt.savefig('./heatmap/heatmap_{}.png'.format(name_index))
    plt.close()


class EphraseToJphrase:
    def __init__(self, en_phrase, en_vocab_ids, ja_phrase, ja_phrase_id):

        self.en_phrase = [en_phrase]
        self.en_vocab_ids = [en_vocab_ids]

        self.ja_phrase = ja_phrase
        self.ja_phrase_id = ja_phrase_id

        self.ja_phrase_length = len(self.ja_phrase.split())


class AllPhrase:
    def __init__(self, en_sentence) -> None:
        self.en_sentence = en_sentence
        self.sentence_id = -1
        self.phrases = []
        self.phrase_num = 0

        self.adj_weight = [] 
        self.adj_row = []
        self.adj_col = []

    def convert_to_coo(self, size):
        self.adj_coo = scipy.sparse.coo_matrix((self.adj_weight,(self.adj_row, self.adj_col)), 
                                                shape=(size,size))


    def add_phrase(self, en_phrase, en_vocab_ids, ja_phrase):
        ja_phrases = [x.ja_phrase for x in self.phrases]
        if ja_phrase in ja_phrases:
            phrase_num = ja_phrases.index(ja_phrase)
            self.phrases[phrase_num].en_phrase.append(en_phrase)
            self.phrases[phrase_num].en_vocab_ids.append(en_vocab_ids)

        else:
            self.phrases.append(EphraseToJphrase(en_phrase, en_vocab_ids, ja_phrase, self.phrase_num))
            self.phrase_num += 1

    def print_all(self):
        print(f'{self.en_sentence=}')
        print(f'{self.sentence_id=}')
        print(f'{self.phrase_num=}')

        for phrase in self.phrases:
            print('\n')
            print(f'{phrase.en_phrase=}')
            print(f'{phrase.en_vocab_ids=}')

            print(f'{phrase.ja_phrase=}')
            print(f'{phrase.ja_phrase_id=}')
            print(f'{phrase.ja_phrase_length=}')

    def merge(self):
        self.input_sentence = self.en_sentence + ' [sep] '
        #self.input_sentence += ' '.join([x.ja_phrase for x in self.phrases])
        #print(self.input_sentence)

        input_adj = []
        ja_start_loc = len(self.en_sentence.split()) + 1

        for phrase in self.phrases:

            if ja_start_loc + phrase.ja_phrase_length > 250:
                break

            self.input_sentence += ' {}'.format(phrase.ja_phrase)

            en_loc = set(list(itertools.chain.from_iterable(phrase.en_vocab_ids)))
            ja_loc = set([ x for x in range(ja_start_loc, ja_start_loc + phrase.ja_phrase_length) ])

            # 日本語-英語フレーズ間でのアテンションを追加
            for one_ja_loc in ja_loc:
                for one_en_loc in en_loc:
                    self.adj_weight.append(1)
                    self.adj_row.append(one_en_loc)
                    self.adj_col.append(one_ja_loc)


                    self.adj_weight.append(1)
                    self.adj_row.append(one_ja_loc)
                    self.adj_col.append(one_en_loc)

            # 英語フレーズ間のセルフアテンション（対角成分以外）を追加
            for one_ja_loc1 in ja_loc:
                for one_ja_loc2 in ja_loc:
                    if one_ja_loc1 != one_ja_loc2:
                        self.adj_weight.append(1)
                        self.adj_row.append(one_ja_loc1)
                        self.adj_col.append(one_ja_loc2)

            ja_start_loc += phrase.ja_phrase_length


        self.convert_to_coo(size=len(self.input_sentence.split()))

    def mold_adj(self):
        adjs = []
        for row, col in zip(self.adj_row, self.adj_col):
            adjs.append('{}-{}'.format(row, col))

        return ' '.join(adjs)


    def draw_heatmap(self, name_index):
        '''
            ヒートマップ作成関数
            表示時に英文内のセルフアテンションと対角成分のアテンション、sepトークンへのアテンションを追加
        '''

        in_len = len(self.input_sentence.split())
        en_len = len(self.en_sentence.split())

        tmp = self.adj_coo.toarray()

        # 英文内のセルフアテンションを追加
        tmp[:en_len, :en_len] = np.ones((en_len,en_len))

        # adjの対角成分を1に
        for i in range(in_len):
            tmp[i,i] = 1

        # sepトークンのアテンションを追加
        tmp[:, en_len] = np.ones(in_len)
        tmp[en_len, :] = np.ones(in_len)

        draw_heatmap(tmp, name_index, axis_name=self.input_sentence.split())


def phrasebyphrase(args):

    print('loading aspec data...')
    with open(args.src) as f:
        src_list = f.readlines()
    src_size = len(src_list)

    with open(args.trg) as f:
        trg_list = f.readlines()

    print('loading phrase table...')
    with open(args.phrase) as f:
        reader = csv.reader(f)
        phrase_table = [row for row in reader]
    phrase_table = [(x[1], x[2]) for x in phrase_table[1:]]
    print(' # of phrase table = {}'.format(len(phrase_table)))

    phrase_table = dict(phrase_table)

    print('translating phrase by phrase...')
    #query = "In information technology and electron field , the application of nanotechnology to next generation semiconductors , high @-@ density information record technology , miniature integrated circuit elements , electric power saving displays using carbon nano @-@ tube , etc. can be expected ."
    #query = "This paper also describes the production procedure of this pressure g@@ age ."
    #ナノテクノロジー の 応用 として ， 情報技術 ・ 電子 分野 で は ， 次世代 半導体 ， 高密度 情報 記録 技術 ， 超小型 集積回路 素子 ， カーボンナノチューブ を 用い た 省電力 ディスプレイ など が 期待 できる 。 

    new_src_list = []
    new_trg_list = []
    adj_list = []

    for i, (query, trg) in enumerate(zip(src_list, trg_list)):

        query = query.strip()

        en_vocabs = query.split()
        allphrase = AllPhrase(query) # EphraseToJphraseクラスのリスト

        for start in range(len(en_vocabs)):
            for length in range(min(5,len(en_vocabs) - start), 0, -1):
                en_phrase = " ".join(en_vocabs[start:start+length])

                if en_phrase.lower() in phrase_table:
                    ja_phrase = phrase_table[en_phrase.lower()]

                    #print('\nen_phrase: {}\nja_phrase : {}'.format(en_phrase,ja_phrase))
                    allphrase.add_phrase(en_phrase, [ x for x in range(start, start + length)], ja_phrase)

                else:
                    continue

        allphrase.merge()
        #allphrase.draw_heatmap()


        if len(allphrase.input_sentence.split()) <= 250:
            new_src_list.append(allphrase.input_sentence + '\n')
            new_trg_list.append(trg)
            adj_list.append(allphrase.mold_adj() + '\n')


        if i%10000 == 0:
            print('No. {} / {}'.format(i, src_size))
            allphrase.draw_heatmap(i)

        # 確認用
        if len(allphrase.input_sentence.split()) > 250:
            print(f'{i=}')
            print(f'{len(allphrase.input_sentence.split())=}')

        #if i == 30000:
        #    break

    with open(args.new_src, 'w') as f:
        f.writelines(new_src_list)
    with open(args.new_trg, 'w') as f:
        f.writelines(new_trg_list)
    with open(args.adj, 'w') as f:
        f.writelines(adj_list)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src')
    parser.add_argument('-t', '--trg')
    parser.add_argument('-p', '--phrase')


    parser.add_argument('--new_src')
    parser.add_argument('--new_trg')
    parser.add_argument('--adj', default='adj_out')


    args = parser.parse_args()

    phrasebyphrase(args)
    
main()


i=666887