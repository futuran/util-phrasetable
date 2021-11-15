import spacy
import gzip
import argparse

def rm_stop_words(args):
    sp_en = spacy.load("en_core_web_sm")
    sp_ja = spacy.load("ja_core_news_sm")

    en_sw = spacy.lang.en.stop_words.STOP_WORDS
    ja_sw = spacy.lang.ja.stop_words.STOP_WORDS

    print(en_sw)
    print(ja_sw)

    ja_symbol = set(['、', '。', '！', '？', '，', '（', '）','・','：', '；', '「', '」', '『', '』', '　', '＊'])


    print('loading data...')
    #with open(args.input, mode='rt', encoding='utf-8') as f:
    #    orig_ptable = f.readlines()
    with gzip.open(args.input, mode='rt', encoding='utf-8') as f:
        orig_ptable = f.readlines()

    print('rmoveing stop_words...')

    new_ptable = []
    for sent in orig_ptable:
        # 全角スペースは特殊記号に置換
        parts = sent.strip().replace('　', '＊').split('|||')

        try:
            en_vocabs = parts[0].strip().split()
        except:
            print('error: at English pharase')
            print(parts)
            continue
        

        try:
            ja_vocabs = parts[1].strip().split()
        except:
            print('error: at Japenese pharase')
            print(parts)
            continue
        

        # 英語のストップワードが一つでも含まれているか、フレーズがアルファベット以外から始まる場合は削除
        if set(en_vocabs) & en_sw != set() or not en_vocabs[0][0].isalpha() or not en_vocabs[-1][-1].isalpha():
            continue
        # 日本語のストップワードが一つでも含まれているか、フレーズが記号（上の定義を参照）から始まる場合は削除
        if set(ja_vocabs) & ja_sw != set() or ja_vocabs[0] in ja_symbol or ja_vocabs[-1] in ja_symbol:
            continue
    
        new_ptable.append(sent)


    #with open(args.output, 'w') as f:
    #    f.writelines(new_ptable)
    with gzip.open(args.output, mode='wt', encoding='utf-8') as f:
        f.writelines(new_ptable)





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output', default='out')


    args = parser.parse_args()

    rm_stop_words(args)

main()