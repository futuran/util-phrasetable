perl mosesdecoder/scripts/training/train-model.perl \
            --root-dir ./aspec.tkn.bpe.align/ \
            --corpus ./aspec.tkn.bpe.align/train_tail \
            --max-phrase-length 5 \
            --f src --e trg \
            --first-step 4 --last-step 6