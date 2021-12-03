python 2.rm_stop_word.py -i ./data_head/model/phrase-table.gz \
                         -o ./data_head/model/phrase-table_rmsw.gz

python 2.rm_stop_word.py -i ./data_tail/model/phrase-table.gz \
                         -o ./data_tail/model/phrase-table_rmsw.gz