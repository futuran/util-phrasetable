for type in tail head;
do
    # dev test 
    DIR=../../20211007_ASPEC_alignment-NMT/data-processing/aspec.tkn.bpe
    for tvt in dev test;
    do
        python 5.phrase-by-phrase.py -s $DIR/aspec_${tvt}.en.tkn.bpe \
                                    -t $DIR/aspec_${tvt}.ja.tkn.bpe \
                                    -p data_${type}/model/phrase-table_rmsw_max.csv \
                                    --new_src data_${type}/${tvt}_wp.src \
                                    --new_trg data_${type}/${tvt}_wp.trg \
                                    --adj data_${type}/${tvt}_wp.adj

    done

    # train
    python 5.phrase-by-phrase.py -s data_${type}/train_${type}.src \
                                -t data_${type}/train_${type}.trg \
                                -p data_${type}/model/phrase-table_rmsw_max.csv \
                                --new_src data_${type}/train_${type}_wp.src \
                                --new_trg data_${type}/train_${type}_wp.trg \
                                --adj data_${type}/train_${type}_wp.adj
done


