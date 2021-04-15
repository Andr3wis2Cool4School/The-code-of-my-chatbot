'''
 * @Author: Andrew Luo 

'''

import numpy as np 
import pandas as pd
import torch 
import torch.nn as nn 
from model import seq2seq
from utils import Datapreprocss






if __name__ == '__main__':
    config = seq2seq.Config()
    config.is_cuda()
    data_content = Datapreprocss(config)
    train_data, dev_data, test_data

    
    




    
