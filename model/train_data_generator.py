import numpy as np
import keras
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical

class DataGenerator(keras.utils.Sequence):
    def __init__(self, samples_data, batch_size=64, shuffle=True, vocab_size=17, word_maxlen=78, label_len=2):
        self.samples_data = samples_data
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.sendin = []
        self.vocab_size = vocab_size
        self.word_maxlen = word_maxlen
        self.label_len = label_len
        self.indexes = None
        self.on_epoch_end()
        self.d = {'aa': 1, 'at': 2, 'ac': 3, 'ag': 4, 'ad': -1,
                  'tt': 5, 'ta': 6, 'tc': 7, 'tg': 8, 'td': -1,
                  'cc': 9, 'ca': 10, 'ct': 11, 'cg': 12, 'cd': -1,
                  'gg': 13, 'ga': 14, 'gc': 15, 'gt': 16, 'gd': -1,
                  }


    def __len__(self):
        ## 每一轮训练包含多少个batch
        return int(np.floor(len(self.samples_data) / self.batch_size))

    ## 每训练完打乱一次样本
    def on_epoch_end(self):
        ## 为每一个样本赋一个索引值
        self.indexes = np.arange(len(self.samples_data))
        if self.shuffle:
            ## 打乱所有样本的索引值
            np.random.shuffle(self.indexes)

    def __getitem__(self, index):
        # print('index', index)
        if (index + 1) * self.batch_size < len(self.samples_data):
            idx = self.indexes[index*self.batch_size : (index + 1)*self.batch_size]
            # print('idx', idx)
            ## 存放每个batch送入网络的索引值
            # self.sendin.append((idx))

            X, y = self.__data_generation(idx)

            return X, y

    def __str_to_int(self, s):
        r = self.d[s]
        return r

    def __data_generation(self, idx):
        ## 处理数据
        # X = np.empty((self.batch_size, self.word_maxlen))
        # y = np.empty((self.batch_size, self.label_len))
        batch_data = []
        label_data = []
        for i, item in enumerate(idx):
            sample = self.samples_data[item]
            info = sample[0]
            self.sendin.append(info)
            ref = sample[1][0]
            seq = list(sample[1][1])
            data = [ref + i for i in seq]
            i_data = [self.__str_to_int(i) for i in data]
            # print('i_data', i_data)
            # print('data', data)
            # tmp = ", ".join(i_data)
            # print('tmp', tmp)
            batch_data.append(i_data)
            # print('batch_data', batch_data)
            label = sample[2]
            if label == (0, 0):
                label = 0
                label_data.append(label)
            elif label == (0, 1):
                label = 1
                label_data.append(label)
            elif label == (1, 1):
                label = 1
                label_data.append(label)
            elif label == (1, 2):
                label = 1
                label_data.append(label)

            # print(label)
            # print('label_data', label_data)

        # encoded_docs = [one_hot(d, self.vocab_size) for d in batch_data]
        # print('en_docs shape', encoded_docs.shape)
        padded_docs = pad_sequences(batch_data, maxlen=self.word_maxlen, padding='post')
        # print('padded_docs shape', padded_docs.shape)
        label_data = to_categorical(label_data, num_classes=self.label_len)
        # print('padded_docs', padded_docs)
        # print('label_data', label_data)
        X = np.array(padded_docs)
        y = np.array(label_data)
        return X, y


    def get_sendin_content(self):
        return self.sendin