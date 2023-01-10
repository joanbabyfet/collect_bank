from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def main():
    try:
        url = 'http://web.thu.edu.tw/s932954/www/ruten/banklist.htm' # 银行代码一览表
        resp = requests.get(url)
        resp.encoding = 'utf-8' # 使用与网页相对应的编码格式, 避免乱码
        soup = BeautifulSoup(resp.text, 'html.parser') # 通过html dom解析器采集数据
        
        ret = soup.find('div', id='bankDiv')
        items = ret.select('tr')
        
        type_bgcolor_maps = { # 类型与色码映射
            '#ecc8da': "銀行", 
            "#ffff99": "信合社", 
            "#cfeaac": "農會", 
            "#99ccff": "漁會", 
            "#ffcc00": "郵局"
        }
        data = []
        for index in range(len(items)): # 通过索引遍历
            if index == 0: continue # 第1行为栏目略过
            tds         = items[index].find_all('td')
            
            for td_index in range(0, len(tds), 2): # 从0开始, 增量2, 所以会生成0, 2, 4, 6
                bank_id     = tds[td_index].get_text(strip=True) # 代号, strip干掉字符串首尾空白
                bank_name   = tds[td_index + 1].get_text(strip=True) # 金融机构
                bgcolor     = tds[td_index + 1].get("bgcolor")

                if bgcolor in type_bgcolor_maps: # 检测该键名是否存在
                    bank_type   = type_bgcolor_maps[bgcolor]
                else:
                    bank_type = ''

                if bank_id != '' and bank_name != '' and bank_type != '': # 检测代号,名称,类型都有值才写入
                    data.append([bank_id, bank_name, bank_type])
        
        col_1 = []
        col_2 = []
        col_3 = []
        for index in range(len(data)):
            col_1.append(data[index][0])
            col_2.append(data[index][1])
            col_3.append(data[index][2])

        headers  = ['代号', '金融机构', '类型']
        export_data = {} # 组装数据, 类型为字典
        export_data[headers[0]] = col_1
        export_data[headers[1]] = col_2
        export_data[headers[2]] = col_3
        df = pd.DataFrame(export_data)
        filename = 'bank_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.csv' # 导出文件名
        df.to_csv(filename, index=False, header=True, encoding='utf-8-sig') # utf-8-sig 解决csv乱码
        print('导出csv成功')
    except:
        print('导出csv失败')

if __name__ == '__main__': # 主入口
    main()