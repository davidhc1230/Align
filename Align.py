#
#!/usr/bin/python
# -*- coding: utf-8 -*-
import unicodedata
#######定義權形轉半形及計算#######
def full2half(x): #全形轉半形
    new_x = '' #定義一個空的字串
    for char in x: #以迴圈讀取字串中的字元
        if unicodedata.east_asian_width(char) == 'F': #若字元為全形字，則全形轉半形
            char = chr(ord(char) - 65248) #全形轉半形
        new_x += char #將轉換的字元補回原位置
    return new_x

def CJK_count(x): #計算CJK(如Chinese、Japanese、Korean)字元數
    counter = 0 #計算字原數
    for char in x: #以迴圈讀取字串中的字元
        if unicodedata.east_asian_width(char) in ('W'): #若字元為CJK字元，則計算字元數
            counter += 1
    return counter

input_lrc = input('決定靠左對齊(L)、靠右對齊(R)或置中(C)，請輸入L或R或C: ')

#######開啟欲對齊的檔案，檔名固定為LeftOrRight.txt,逐行讀取此檔案，並轉為list#######
                  #######encoding設utf-8則可讀取全形字元#######                   

data = [line.strip() for line in open('Align_input.txt', 'r', encoding='utf-8')] #開啟並讀取欲進行排版的資料(或文字)
output = open('Align_output.txt', 'w', encoding='utf-8') #開啟名為LeftOrRight_output.txt的檔案，存放輸出結果

num_list = []
for i in data: #逐行計算
    i = i.replace('　', '').replace('\t', '') #先將全形空格及tab鍵刪除
    i = full2half(i) #再將全形轉半形
    len_i = len(i) #計算所有(包含CJK字元)字元數
    cjk = CJK_count(i) #計算CJK字元數
    num = len_i+cjk #因為CJK字元佔據兩格的位置，因此需計算所有字元數，再加上CJK字元數
    num_list.append(num)
    max_num = max(num_list) #求出文件中佔據格數最多的那行佔據了多少格

for i in data: #進行文件改寫
    i = i.replace('　', '').replace('\t', '')
    i = full2half(i)
    cjk = CJK_count(i)
    mm = max_num-cjk #佔據格數最多減去CJK字元數，即對齊全部內容所需的格數
    if input_lrc == 'R':
        align_result = '{:>{}s}'.format(i, mm) #依據最長的字串長度，決定靠右對齊
    elif input_lrc == 'L':
        align_result = '{:<{}s}'.format(i, mm) #依據最長的字串長度，決定靠左對齊
    elif input_lrc == 'C':
        align_result = '{:^{}s}'.format(i, mm) #依據最長的字串長度，決定靠左對齊
    else:
        print('輸入錯誤！請重新輸入！')
        break
    output.write(align_result + '\r') #將對齊的結果寫入檔案中，並換行
output.close() #關閉寫入的檔案