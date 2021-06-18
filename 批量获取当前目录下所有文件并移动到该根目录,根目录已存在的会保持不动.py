# encoding=utf-8
#批量获取当前目录下所有文件并移动到该根目录,根目录已存在的会保持不动
import os
import shutil

class findPath:
    def __init__(self):
        self.fileList = []
        
    def gci(self, filepath):
        files = os.listdir(filepath)
        for fi in files:
            fi_d = os.path.join(filepath, fi)
            if os.path.isdir(fi_d):
                self.gci(fi_d)
            else:
                self.fileList.append(fi_d)

    def getAllPaths(self, filepath):
        self.gci(filepath)
        return self.fileList

rootdir='.\\pic\\'
run=findPath()
filelist=list(run.getAllPaths(rootdir))
for i in filelist:
    print(i)
    try:shutil.move(i,rootdir)
    except:pass