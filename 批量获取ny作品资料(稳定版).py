# encoding=utf-8
#批量获取ny作品资料
import re
import os
import time
import requests

def getnyhtml():#自动翻页获取角色所有作品html源文件,并保存
    for n in range(page):
        try:
            nyurl=f'{tempurl}{n+1}' 
            rqhtml=requests.get(url=nyurl).content
            print(f'{n+1}.{name}')
            with open(f'{n+1}.{name}.html','wb') as f:#字节流数据写入文件
                f.write(rqhtml)
            time.sleep(1) #为了规避高频访问IP封禁,加上延时
        except:
            pass

def xzfhhtml(fhcode,fhhtmlurl):#获取fh图片HTML,并保存,传入路径,保存HTML供后面解析
    try:
        #fhcode=str(fhcode)
        fhhtmlurl='https:'+fhhtmlurl
        rqfhhtml=requests.get(url=fhhtmlurl).content
        with open(f'{fhcode}.html','wb') as f:#字节流数据写入文件
            f.write(rqfhhtml)
        time.sleep(1) #为了规避高频访问IP封禁,加上延时
    except:
        pass
        
def getfhhtml():#解析html源文件,解析出番号,番号地址,并把番号HTML下载
    for n in range(page):
        with open(f'{n+1}.{name}.html',encoding='utf-8') as f:#注意编码格式
            htmldata=f.read()   
            #redata=re.findall(r'<span>(.*?)<br><date>(.*?)</date> / <date>(.*?)</date></span>',htmldata)#(名称,车牌号,日期)
            refhcode=re.findall(r'<span>.*?<br><date>(.*?)</date> / <date>.*?</date></span>',htmldata)#(番号)
            refhallhtmlurl=re.findall(r'<a class="movie-box" href="(.*?)">',htmldata)#(番号HTML地址)
            list(map(xzfhhtml,refhcode,refhallhtmlurl))
                
def xzjpg(jpgname,jpgurl):
    try:
        rqjpg=requests.get(url=jpgurl).content
        with open(f'.\\{jpgname}.jpg','wb') as f:
            f.write(rqjpg)
        time.sleep(1) #加入下载延迟
    except:
        pass
            
def getjpg():
    for n in range(page):
        with open(f'{n+1}.{name}.html',encoding='utf-8') as f:#注意编码格式
            htmldata=f.read()   
            #redata=re.findall(r'<span>(.*?)<br><date>(.*?)</date> / <date>(.*?)</date></span>',htmldata)#(名称,车牌号,日期)
            refhcode=re.findall(r'<span>.*?<br><date>(.*?)</date> / <date>.*?</date></span>',htmldata)#(番号)
            for code in refhcode:
                with open(f'{code}.html',encoding='utf-8') as f:
                    htmldata=f.read()
                    rejpgurl=re.findall(r'<a class="bigImage" href="(.*?)" title=.*?">',htmldata)
                    rejpgname=re.findall(r'<a class="bigImage" href=".*?" title="(.*?)">',htmldata)
                    rejpgname=[re.sub(r'[^\w\u4e00-\u9fa5]+','',i) for i in rejpgname] #过滤非常字母数字中文防止文件名异常保存失败
                    list(map(xzjpg,rejpgname,rejpgurl)) #注意外层套一个list使生成器被动next执行所有
                    
                    reypjpgurl=re.findall(r'<a class="sample-box" href="(.*?)" title=".*?">',htmldata)
                    reypjpgname=re.findall(r'<a class="sample-box" href=".*?" title="(.*?)">',htmldata)
                    reypjpgname=[re.sub(r'[^\w\u4e00-\u9fa5]+','',i) for i in reypjpgname] #过滤非常字母数字中文防止文件名异常保存失败
                    list(map(xzjpg,reypjpgname,reypjpgurl)) #获取剧情样图

def makefhdir(fhcode):  #新建番号文件夹，该功能暂时不用
    try:
        for i in fhcode:
            i=str(i)
        if not os.path.exists(f'.\\{name}\\{i}'):
            os.makedirs(f'.\\{name}\\{i}')
        with open(f'.\\{name}\\{name}.txt','a',encoding='utf-8') as t:#注意编码格式
            t.write(i+'\r\n')
    except:
        pass

if __name__=='__main__':

    #数据容器格式如下：[['名称',页数,URL],[...],[...].....]
    nydatalist=[['橋本',7,'https://avmoo.casa/cn/star/4125b073b60d3439/page/'],
                       ['羽咲',5,'https://avmoo.casa/cn/star/b3a61e53dff0b2fd/page/'],
                       ['夢乃',7,'https://avmoo.casa/cn/star/d494c7e9fb283e64/page/'],
                       ['夕美',3,'https://avmoo.casa/cn/star/6f8f9f07fa9b9abb/page/'],
                       ['星宫',3,'https://avmoo.casa/cn/star/febabca17e93bfba/page/'],
                       ['奥田',10,'https://avmoo.casa/cn/star/93835e007ecf8724/page/'],
                       ['架乃',4,'https://avmoo.casa/cn/star/dac941552665b010/page/'],
                       ['星野',8,'https://avmoo.casa/cn/star/8a5f280730e0cab1/page/']]
    
    for item in nydatalist:
        try:
            name=item[0]
            page=item[1]
            tempurl=item[2] 
            getnyhtml() #下载角色作品主HTML
            getfhhtml() #下载番号HTML
            getjpg() #解析番号HTML中图片地址并下载
        except:
            pass

