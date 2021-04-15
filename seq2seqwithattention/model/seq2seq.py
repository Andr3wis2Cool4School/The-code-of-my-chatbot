'''
 * @Author: Andrew Luo 

'''


import torch 
import torch.nn as nn 


class Config(object):
    '''
    model config
    '''
    def __init__(self):
        self.model_name = 'seq2seqwithattention'
        self.save_path = 'save_dir/' + self.model_name + 'ckpt'
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.train_data = '../data/train.csv'
        self.test_data = '../data/test.csv'
        self.dev_data = '../data/dev.csv'
        self.data_path = '../data'
        self.embedding_path = '../data/glove.840B.300d.txt'

    '''
    see the gpu is available
    more in main.py
    '''
    def is_cuda(self):
        print('Cuda Status on System is {}'.format(torch.cuda.is_available()))

        


        