def create_template(routes_num, r_trans_num, API_Result, ticket):
# 中間變數先填好
    # 儲存中間的html碼
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\web_test21.html', mode='r', encoding='utf-8') as html_21:
        html_21_Lines = html_21.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\web_test22.html', mode='r', encoding='utf-8') as html_22:
        html_22_Lines = html_22.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\web_test23.html', mode='r', encoding='utf-8') as html_23:
        html_23_Lines = html_23.readlines()
    # 寫進中間的template
    Change_22_Lines = html_22_Lines
    Change_23_Lines = html_23_Lines
    for route_num in range(routes_num):
        if route_num == 0:  # 如果是重新來過，要覆寫
            with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\Web\\official\\templates\\web_test2.html', mode='w', encoding='utf-8') as html_2:
                html_2.writelines(html_21_Lines)
        else:
            with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\Web\\official\\templates\\web_test2.html', mode='a', encoding='utf-8') as html_2:
                html_2.writelines(html_21_Lines)
        for tran_num in range(r_trans_num):  # 幾種交通工具複製幾次
            with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\Web\\official\\templates\\web_test2.html', mode='a', encoding='utf-8') as html_2:
                for line in Change_22_Lines:
                    line = line.replace("startstation", str(API_Result[route_num][tran_num][3]))
                    line = line.replace("endstation", str(API_Result[route_num][tran_num][4]))
                    line = line.replace("starttime", str(API_Result[route_num][tran_num][6]))
                    line = line.replace("transtype", str(API_Result[route_num][tran_num][1] + API_Result[route_num][tran_num][2]))
                    line = line.replace("endtime",str(API_Result[route_num][tran_num][8]))
                    html_2.write(line)
        with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\Web\\official\\templates\\web_test2.html', mode='a', encoding='utf-8') as html_2:
            for line in Change_23_Lines:
                line = line.replace("pricetype", str(Price[route_num][tran_num][1][ticket][0]))
                line = line.replace("price", "$ 最低總價")
                line = line.replace("route1", "route"+str(route_num+1))
                html_2.write(line)

    # 儲存html碼
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\Web\\official\\templates\\web_test1.html', mode='r', encoding='utf-8') as begin:
        Begin_Lines = begin.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\Web\\official\\templates\\web_test2.html', mode='r', encoding='utf-8') as middle:
        Middle_Lines = middle.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\Web\\official\\templates\\web_test3.html', mode='r', encoding='utf-8') as end:
        End_Lines = end.readlines()

    # 寫進template
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\Web\\official\\templates\\web_test.html', mode='w', encoding='utf-8') as combination:
        combination.writelines(Begin_Lines)
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\Web\\official\\templates\\web_test.html', mode='a', encoding='utf-8') as combination:
        combination.writelines(Middle_Lines)
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\Web\\official\\templates\\web_test.html', mode='a', encoding='utf-8') as combination:
        combination.writelines(End_Lines)
    return None


API_Result = [[['HEAVY_RAIL', '自強號', '271', '松山車站', '台北車站', '2020/01/01', '下午12:35', '2020/01/01', '下午12:42'], ['HEAVY_RAIL', '高鐵', '639', '台北車站', '高鐵台南站', '2020/01/01', '下午12:46', '2020/01/01', '下午2:32'], ['HEAVY_RAIL', ' 復興/區間', '3744', '沙崙車站', '台南車站', '2020/01/01', '下午2:47', '2020/01/01', '下午3:10']]]
Price = [[['台鐵', (['全票', 23, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 12, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])],['高鐵', [['全票', {'標準車廂': 1350, '商務車廂': 2230, '自由座': 1305}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 675, '商務車廂': 1115, '自由座': 650}, 'https://irs.thsrc.com.tw/IMINT/']]],['台鐵', (['全票', 25, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 13, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]]]
routes_num = len(API_Result)
r_trans_num = len(API_Result[0])
ticket = 1  # 半票

create_template(routes_num, r_trans_num, API_Result, ticket)