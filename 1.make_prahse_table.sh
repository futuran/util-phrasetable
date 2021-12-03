
for type in head tail
do
    perl mosesdecoder/scripts/training/train-model.perl \
                --root-dir ./data_$type \
                --corpus ./data_$type/train_${type}_pht \
                --max-phrase-length 5 \
                --f src --e trg \
                --first-step 4 --last-step 6
done