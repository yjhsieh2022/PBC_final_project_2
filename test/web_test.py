def create_template(r_trans_num):
    # 儲存html碼
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\web_test1.html', mode='r', encoding='utf-8') as begin:
        Begin_Lines = begin.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\web_test2.html', mode='r', encoding='utf-8') as middle:
        Middle_Lines = middle.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\web_test3.html', mode='r', encoding='utf-8') as end:
        End_Lines = end.readlines()

    # 寫進template
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\web_test.html', mode='w', encoding='utf-8') as combination:
        combination.writelines(Begin_Lines)
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\web_test.html', mode='a', encoding='utf-8') as combination:
        for i in range(r_trans_num):
            combination.writelines(Middle_Lines)
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\web_test.html', mode='a', encoding='utf-8') as combination:
        combination.writelines(End_Lines)
    return none