import spacy
import gzip
import argparse
import re

def rm_stop_words(args):
    sp_en = spacy.load("en_core_web_sm")
    sp_ja = spacy.load("ja_core_news_sm")

    en_sw = spacy.lang.en.stop_words.STOP_WORDS
    ja_sw = spacy.lang.ja.stop_words.STOP_WORDS

    print(en_sw)
    print(ja_sw)

    # 英字の小文字 or 大文字 or スペース
    re_en = re.compile(r'[a-zA-Z\s]+')
    # ひらがな or カタカナ or 漢字
    re_ja = re.compile(r'[あ-ん\u30A1-\u30F4\u4E00-\u9FD0\s]+')


    print('loading data...')
    with gzip.open(args.input, mode='rt', encoding='utf-8') as f:
        orig_ptable = f.readlines()

    print('removeing stop_words...')
    new_ptable = []
    for sent in orig_ptable:
        # 全角スペースは特殊記号に置換
        parts = sent.strip().split('|||')

        try:
            en_vocabs = parts[0].strip()
        except:
            print('error: at English pharase')
            print(parts)
            continue
        try:
            ja_vocabs = parts[1].strip()
        except:
            print('error: at Japenese pharase')
            print(parts)
            continue
        

        # 英語のストップワードが一つでも含まれているか、フレーズがアルファベット以外から始まる/終わる場合は削除
        if set(en_vocabs.split()) & en_sw != set() or re_en.fullmatch(en_vocabs) == None:
            #not en_vocabs[0][0].isalpha() or not en_vocabs[-1][-1].isalpha()
            continue
        # 日本語のストップワードが一つでも含まれているか、フレーズが記号（上の定義を参照）から始まる/終わる場合は削除
        if set(ja_vocabs.split()) & ja_sw != set() or re_ja.fullmatch(ja_vocabs) == None:
            #ja_vocabs[0] in ja_symbol or ja_vocabs[-1] in ja_symbol:
            continue
    
        new_ptable.append(sent)

    with gzip.open(args.output, mode='wt', encoding='utf-8') as f:
        f.writelines(new_ptable)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output', default='out')

    args = parser.parse_args()
    rm_stop_words(args)

main()