MAXLEN = 5
vocabulary = set()
with open('./word_freq_list.txt', encoding='utf-8') as f:
    for l in f.readlines():
        vocabulary.add(l.split(' ')[1])


def forward_split(text):
    split_words = []
    while text != '':
        sub_string = text[:MAXLEN]
        while sub_string != '':
            if sub_string in vocabulary or len(sub_string) == 1:
                split_words.append(sub_string)
                break
            else:
                sub_string = sub_string[:-1]
        text = text[len(sub_string):]
    return split_words


def backward_split(text):
    split_words = []
    while text != '':
        sub_string = text[-MAXLEN:]
        while sub_string != '':
            if sub_string in vocabulary or len(sub_string) == 1:
                split_words.append(sub_string)
                break
            else:
                sub_string = sub_string[1:]
        text = text[:-len(sub_string)]
    return split_words[::-1]


def contrast(forward_list, backward_list):
    forward_hit = [(1 if w in vocabulary else 0) for w in forward_list]
    backward_hit = [(1 if w in vocabulary else 0) for w in forward_list]
    forward_acc = sum(forward_hit) / len(forward_list)
    backward_acc = sum(backward_hit) / len(backward_list)
    print('正向字典词：{:.0%}'.format(forward_acc))
    print('逆向字典词：{:.0%}'.format(backward_acc))
    if forward_acc > backward_acc:
        return forward_list, forward_acc
    elif backward_acc > forward_acc:
        return backward_list, backward_acc
    else:
        forward_single = [(1 if len(w) == 1 else 0) for w in forward_list]
        backward_single = [(1 if len(w) == 1 else 0) for w in backward_list]
        print('正向单字词个数：{}'.format(sum(forward_single)))
        print('逆向单字词个数：{}'.format(sum(backward_single)))
        if sum(backward_single) < sum(forward_single):
            return backward_list, backward_acc
        elif sum(backward_single) > sum(forward_single):
            return forward_list, forward_acc
        else:
            print('正向总词数：{}'.format(len(forward_list)))
            print('逆向总词数：{}'.format(len(backward_list)))
            if len(backward_list) < len(forward_list):
                return backward_list, backward_acc
            else:
                return forward_list, forward_acc
            # TODO：根据词频确定最优分词结果


if __name__ == '__main__':
    text_string = input('请输入待分词句子：')
    forward_words_list = forward_split(text_string)
    backward_words_list = backward_split(text_string)
    better_words_list, better_acc = contrast(forward_words_list, backward_words_list)
    print('正向分词结果：{}'.format(forward_words_list))
    print('逆向分词结果：{}'.format(backward_words_list))
    print('较优分词结果：{}'.format(better_words_list))
