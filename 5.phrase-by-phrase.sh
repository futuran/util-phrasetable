for type in tail;
do

    python 5.phrase-by-phrase.py -s data_${type}/train_${type}.src \
                                -t data_${type}/train_${type}.trg \
                                -p data_${type}/model/phrase-table_rmsw_max.csv \
                                --new_src data_${type}/train_${type}_wp.src \
                                --new_trg data_${type}/train_${type}_wp.trg \
                                --adj data_${type}/train_${type}_wp.adj

done