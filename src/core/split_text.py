import re
import regex
import MeCab
import demoji
import util.logger.loggingUtil as lu

# markdown記法などの化粧を除き、空行を詰める
def remove_markdown_decorations(text):
    # 見出し（# や ## を削除）
    text = re.sub(r'(?m)^(#+)\s*', '', text)

    # 太字（**太字** を削除）
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)

    # 斜体（*斜体* を削除）
    text = re.sub(r'\*(.*?)\*', r'\1', text)

    # コード（`コード` を削除）
    text = re.sub(r'`(.*?)`', r'\1', text)

    # リスト（- や 数字付きリストを保持）
    text = re.sub(r'(?m)^\s*[-]+\s+', '', text)  # 箇条書きリスト
    text = re.sub(r'(?m)^\s*(\d+\.)\s+', r'\1 ', text)  # 番号付きリスト

    # リンクを「リンク」だけにする
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)

    # 引用を「引用　元のテキスト」の形式に変換
    text = re.sub(r'(?m)^>\s*(.*)', r'引用 \1', text)

    # 絵文字のみを削除
    text = demoji.replace(string=text, repl="")

    # 改行の整形
    text = re.sub(r'\n+', '\n', text).strip()

    return text

APPENDED_MAX_LEN = 30

# 30文字以下の短い文をまとめる
def merge_text_lines(text):
    # テキストを行ごとに分割
    lines = text.splitlines()
    result = []
    i = 0
    
    while i < len(lines):
        current_line = lines[i]
        
        # 次の行と結合し、APPENDED_MAX_LENに達するまで繰り返す
        while len(current_line) <= APPENDED_MAX_LEN and i + 1 < len(lines):
            current_line += lines[i + 1]
            i += 1
        
        result.append(current_line)
        i += 1  # 次の行へ進む

    return result

# 句点で分割する関数
def split_by_ku(text):
    sentences = regex.split(r'(?<=。)', text)
    return [sentence for sentence in sentences if sentence]

# MeCabを使って形態素解析で分割する関数
def split_sentence_by_mecab(sentence):
    mecab = MeCab.Tagger()
    node = mecab.parseToNode(sentence)
    
    words = []
    while node:
        surface = node.surface
        if surface:
            words.append(surface)
        node = node.next
    
    middle = len(words) // 2
    for i in range(middle, len(words)):
        if '助詞' in mecab.parse(words[i]):
            return ''.join(words[:i+1]), ''.join(words[i+1:])
    
    return ''.join(words[:middle]), ''.join(words[middle:])

# 最大50文字まで許容する変数
MAX_TXT_LEN = 50

# 読点・句点・空白または形態素に基づいて分割する関数
def split_by_touten_and_mecab(sentence):
    if len(sentence) <= MAX_TXT_LEN:
        return [sentence]
    
    mid_index = len(sentence) // 2
    search_range = 10  # 中央から前後10文字以内

    closest_punct = -1
    # 分割対象の記号を読点、句点、空白に変更
    for offset in range(-search_range, search_range + 1):
        if 0 <= mid_index + offset < len(sentence):
            char = sentence[mid_index + offset]
            if char in '、。 ':
                closest_punct = mid_index + offset
                break

    if closest_punct == -1:
        # 読点、句点、空白が見つからなければ形態素解析で分割
        first_part, second_part = split_sentence_by_mecab(sentence)
    else:
        # 分割対象記号が見つかった場合、そこで分割
        first_part = sentence[:closest_punct + 1]
        second_part = sentence[closest_punct + 1:]

    # 再帰的に処理
    return split_by_touten_and_mecab(first_part) + split_by_touten_and_mecab(second_part)

# テキストを50文字以下に分割、分割方法は句読点と空白、句読点分割ができない場合形態素で分割
def split_by_kuten_touten_mecab(text):
    result = []
    current_line = ""

    for i, line in enumerate(text):
        # 一行が50文字以下だった場合は次の行と結合
        if len(current_line) + len(line.strip()) <= MAX_TXT_LEN:
            if current_line:
                current_line += ' ' + line.strip()
            else:
                current_line = line.strip()
            continue  # 次の行の処理に進む

        # 50文字以上の場合、その行を処理結果として格納
        if current_line:
            result.extend(split_by_touten_and_mecab(current_line))
            current_line = ""

        sentences = split_by_ku(line)
        for sentence in sentences:
            result.extend(split_by_touten_and_mecab(sentence))

    # 最後に残った行を追加（もしあれば）
    if current_line:
        result.extend(split_by_touten_and_mecab(current_line))

    return result


MIN_TXT_LEN = 20

# 念のため短い文があった場合は次の行と結合し、最終的なテキストを生成
def correct_split_sentences(input):
    tmp = None
    result = []
    
    for check_sentence in input:
        if tmp is not None:
            tmp += check_sentence
            result.append(tmp)
            if len(check_sentence) > MIN_TXT_LEN:
                tmp = None
        else:
            if len(check_sentence) <= MIN_TXT_LEN:
                tmp = check_sentence
            else:
                result.append(check_sentence)
                tmp = None

    # 最後のtmpが残っている場合にresultに追加
    if tmp is not None:
        result.append(tmp)
    
    return result

@lu.loggingAOP("テキストを音声ファイルとして適切な長さに分割")
def split_text(text):

    print("---------------------------------------------------------------")
    print("# オリジナルテキスト")
    print("---------------------------------------------------------------")
    print(text)

    print("---------------------------------------------------------------")
    print("# markdown記法などの化粧を除き、空行を詰める")
    print("---------------------------------------------------------------")
    stuffed_text = remove_markdown_decorations(text)
    print(stuffed_text)

    print("---------------------------------------------------------------")
    print("# 30文字以下の短い文をまとめる")
    print("---------------------------------------------------------------")
    merged_text = merge_text_lines(stuffed_text)
    for line_text in merged_text:
        print(line_text)

    print("---------------------------------------------------------------")
    print("# テキストを50文字以下に分割、分割方法は句読点と空白、句読点分割ができない場合形態素で分割")
    print("---------------------------------------------------------------")

    split_result = split_by_kuten_touten_mecab(merged_text)
    for line_text in split_result:
        print(line_text)

    print("---------------------------------------------------------------")
    print("# 念のため短い文があった場合は次の行と結合し、最終的なテキストを生成")
    print("---------------------------------------------------------------")

    correct_result = correct_split_sentences(split_result)
    for sentence in correct_result:
        print(sentence)

    return correct_result
