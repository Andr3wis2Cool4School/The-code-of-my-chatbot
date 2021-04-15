'''
 * @Author: Andrew Luo 

'''


import pandas as pd 
import torch
import torchtext
from torchtext.data.utils import get_tokenizer
from torchtext.legacy import data 
from model import seq2seq



class Datapreprocss(object):
    def __init__(self, config):
        '''
        Using train_test_split
        1. train, test+dev = 0.6 + 0.4
        2. test + dev = 0.5 + 0.5 

        overall = train, test, dev => 0.6, 0.2, 0.2
        '''
        self.TEXT = data.Field(sequential=True, tokenize=get_tokenizer('basic_english', lower=True))
        self.LABEL = data.Field(sequential=True, tokenize=get_tokenizer('basic english', lower=True))
    
    def get_data(self, data_path):
        train_data, dev_data, test_data = data.TabularDataset.splits(
            path=data_path,
            train='train.csv',
            validation='dev.csv', 
            test='test.csv',
            format='csv',
            skip_header=True,
            fields=[('Text', TEXT), ('Label'), LABEL]
        )

        print('Number of training examples: {}'.format(len(train_data)))
        print('Number of dev examples: {}'.format(len(dev_data)))
        print('Number of testing examples: {}'.format(len(test_data)))

        return train_data, dev_data, test_data

    def _build_vocab(self, train_data, embedding_path):
        self.TEXT.build_vocab(train_data, vectors=torchtext.vocab.Vectors(embedding_path), max_size=20000, min_freq=10)
        self.LABEL.build_vocab(train_data, vectors=torchtext.vocab.Vectors(embedding_path), max_size=20000, min_freq=10)
        
        print(f"Unique tokens in TEXT vocabulary: {len(TEXT.vocab)}")
        print(f"Unique tokens in LABEL vocabulary: {len(LABEL.vocab)}")

        return self.TEXT.vocab, self.LABEL.vocab

    def iter_text_data(self, batch_size, device, train_data, dev_data, test_data):
        train_iterator, dev_iterator, test_iterator = data.BucketIterator.splits((train_data, dev_data, test_data), 
                                                                                 sort_key=lambda x:len(x.self.TEXT),
                                                                                 batch_size=batch_size,
                                                                                 device=device)
    
        return train_iterator, dev_iterator, test_iterator










