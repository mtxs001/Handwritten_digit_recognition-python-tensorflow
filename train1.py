"""
作者：漫天星沙
"""
import os
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from PIL import Image
import numpy as np

class CNN(object):
    def __init__(self):
        model = models.Sequential()
        # 第1层卷积，卷积核大小为3*3，输出通道32个，28*28为待训练图片的大小，使用relu 作为激活函数
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
        # 第二层为一个最大池化层，池化核为（2,2)
        # 最大池化的作用，是取出池化核（2,2）范围内最大的像素点代表该区域
        # 可减少数据量，降低运算量。
        model.add(layers.MaxPooling2D((2, 2)))
        # 经过一个（3,3）的卷积，输出通道变为64，也就是提取了64个特征。同样为 relu激活函数
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        # 上面通道数增大，运算量增大，此处再加一个最大池化，降低运算
        model.add(layers.MaxPooling2D((2, 2)))
        # 第3层卷积，卷积核大小为3*3，64个
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        # 将结果展平成1维的向量，为全连接层做准备
        model.add(layers.Flatten())
        # 增加一个全连接层，用来进一步特征融合
        model.add(layers.Dense(64, activation='relu'))
        # 最后添加一个全连接+softmax激活，输出10个分类，分别对应0-9 这10个数字
        model.add(layers.Dense(10, activation='softmax'))
        # 打印神经网络结构，统计参数数目
        model.summary()
        self.model = model


class DataSource(object):
    def __init__(self):
        train_images = Image.open('./test_images/a1.png').convert('L')
        train_images = np.reshape(train_images, (1, 28, 28))
        a1 = ['a2', 'a3', 'a4', 'c1', 'c2', 'c3', 'c4']

        for i in a1:
            img = Image.open('./test_images/%s.png' % (i)).convert('L')
            img = np.reshape(img, (1, 28, 28))
            train_images = np.concatenate((train_images, img), axis=0)


        train_labels = np.array([1,1,1,1,2,2,2,2])

        a5 = np.reshape(Image.open('./test_images/a5.png').convert('L'), (1, 28, 28))
        c5 = np.reshape(Image.open('./test_images/c5.png').convert('L'), (1, 28, 28))
        test_images = np.concatenate((a5, c5), axis=0)

        test_labels = np.array([1,2])

        for i in range(12):
            train_images = np.concatenate((train_images, train_images), axis=0)
            train_labels = np.concatenate((train_labels, train_labels), axis=0)
            test_images = np.concatenate((test_images, test_images), axis=0)
            test_labels = np.concatenate((test_labels, test_labels), axis=0)

        train_images = train_images[0:30000, :, :]
        train_labels = train_labels[0:30000]
        test_images = test_images[0:3000, :, :]
        test_labels = test_labels[0:3000]

        train_images = train_images.reshape((30000, 28, 28, 1))
        test_images = test_images.reshape((3000, 28, 28, 1))

        # 像素值映射到 0 - 1 之间,因为mnist数据集里面像素值都是（0～1）
        # 像素点:0-1 之间的浮点数(接近 0 越黑,接近 1 越白)
        train_images, test_images = train_images / 255.0, test_images / 255.0
        self.train_images, self.train_labels = train_images, train_labels
        self.test_images, self.test_labels = test_images, test_labels



class Train:
    def __init__(self):
        self.cnn = CNN()
        self.data = DataSource()

    def train(self):
        # check_path = '.\\ckpt\\cp-{epoch:04d}.ckpt'
        check_path = os.path.abspath(os.path.dirname(__file__)) + '\\ckpt\\cp-{epoch:04d}.ckpt'
        # period 每隔5epoch保存一次，断点续训
        # ModelCheckpoint回调与使用model.fit（）进行的训练结合使用，
        # 可以稍后加载模型或权重以从保存的状态继续训练。
        save_model_cb = tf.keras.callbacks.ModelCheckpoint(check_path, save_weights_only=True, verbose=1, period=5)
        # 编译上述构建好的神经网络模型
        # 指定优化器为 adam
        # 制定损失函数为交叉熵损失
        self.cnn.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        # 指定训练特征集和训练标签集
        self.cnn.model.fit(self.data.train_images, self.data.train_labels, epochs=5, callbacks=[save_model_cb])
        # 在测试集上进行模型评估
        test_loss, test_acc = self.cnn.model.evaluate(self.data.test_images, self.data.test_labels)
        print("准确率: %.4f，共测试了%d张图片 " % (test_acc, len(self.data.test_labels)))


if __name__ == "__main__":
    app = Train()
    app.train()
