import os
import jieba
import pickle

from _cffi_backend import string
from sklearn.datasets._base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
from .Tools import readfile, readbunchobj, writebunchobj


script_dir = os.path.dirname(__file__)

def divide_word():

    file_path = os.path.join(script_dir, 'test.txt')  # 替换成实际文件路径
    dict_file = os.path.join(script_dir, 'dict.txt')
    jieba.load_userdict(dict_file)

    with open(file_path, "rb") as fp:
        content = fp.read()
        content = content.replace('\r\n'.encode('utf-8'), ''.encode('utf-8')).strip()  # 删除换行
        content = content.replace(' '.encode('utf-8'), ''.encode('utf-8')).strip()  # 删除空行、多余的空格
        content_seg = jieba.cut(content)  # 为文件内容分词

        with open(file_path, 'wb') as file:
            file.write(' '.join(content_seg).encode('utf-8'))


def bunching():
    def readfile(path):
        with open(path, "rb") as fp:
            content = fp.read()
        return content

    def corpus2Bunch(wordbag_path, test_text_path):
        # 创建一个Bunch实例
        bunch = Bunch(target_name=["Unknown"], label=["Unknown"], filenames=[test_text_path],
                      contents=[readfile(test_text_path)])

        # 将bunch存储到wordbag_path路径中
        with open(wordbag_path, "wb") as file_obj:
            pickle.dump(bunch, file_obj)
        # print("构建文本对象结束！！！")

    test_text_path = os.path.join(script_dir, 'test.txt') # 替换成你的预测文本路径
    wordbag_path = os.path.join(script_dir, 'test_set.dat')  # Bunch存储路径

    corpus2Bunch(wordbag_path, test_text_path)


def vectoring():
    def vector_space(stopword_path, bunch_path, space_path, train_tfidf_path=None):
        stpwrdlst = readfile(stopword_path).splitlines()
        bunch = readbunchobj(bunch_path)
        tfidfspace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[],
                           vocabulary={})

        if train_tfidf_path is not None:
            trainbunch = readbunchobj(train_tfidf_path)
            tfidfspace.vocabulary = trainbunch.vocabulary
            vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5,
                                         vocabulary=trainbunch.vocabulary)
            '''
            #.stop_words=list类型,直接过滤指定的停用词。
            # sublinear_tf:，计算tf值采用亚线性策略。比如，我们以前算tf是词频，现在用1+log(tf)来充当词频。
            #max_df,过滤出现在超过max_df=0.5比例的句子中的词语,当他在全文档出现的频次过多>50%时我们认为他太过常见而不具备代表性
            # .vocabulary: dict类型,只使用特定的词汇，为了避免在测试集中出现训练集中没有出现的词汇而造成困扰所以一般会用这个，但是如果训练集足够大可以不用
            '''
            tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)

        else:
            vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5)
            '''
            #.stop_words=list类型,直接过滤指定的停用词。
            # sublinear_tf:，计算tf值采用亚线性策略。比如，我们以前算tf是词频，现在用1+log(tf)来充当词频。
            # max_df,过滤出现在超过max_df=0.5比例的句子中的词语,当他在全文档出现的频次过多>50%时我们认为他太过常见而不具备代表性
            '''
            tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)
            tfidfspace.vocabulary = vectorizer.vocabulary_

        writebunchobj(space_path, tfidfspace)
        # print("if-idf词向量空间实例创建成功！！！")

    stopword_path = os.path.join(script_dir, 'hit_stopwords.txt')
    bunch_path = os.path.join(script_dir,"test_set.dat")
    space_path = os.path.join(script_dir,"testspace.dat")
    train_tfidf_path = os.path.join(script_dir, "tfdifspace.dat")
    # 对测试文本进行TF-IDF向量化
    vector_space(stopword_path, bunch_path, space_path, train_tfidf_path)


def obtaining():
    model_filename =os.path.join(script_dir,"text-classifier.pkl")

    with open(model_filename, 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    testpath = os.path.join(script_dir,"testspace.dat")
    test_set = readbunchobj(testpath)
    # 使用模型进行预测
    predicted = loaded_model.predict(test_set.tdm)
    # print(predicted)
    return predicted[0]

def get(art):
    file_path = os.path.join(script_dir, 'test.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(art)

    divide_word()
    bunching()
    vectoring()
    type = obtaining()
    return type
