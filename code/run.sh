#!/usr/bin/env bash

# generate features
python3 gen_candidates.py train
python3 gen_candidates.py test

# extract tru labels
python3 labels.py train
python3 labels.py test

# run classification on final M classifier trained on I tested on  J
python3 classification.py
