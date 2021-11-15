perl mosesdecoder/scripts/training/train-model.perl \
            --root-dir ./aspec.tkn.align/ \
            --corpus ./aspec.tkn.align/train \
            --model-dir ./aspec.tkn.align/model \
            --f src --e trg \
            --first-step 7 --last-step 8