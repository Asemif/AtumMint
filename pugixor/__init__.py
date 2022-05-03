import pugixor

def PugiSplit(string):
    return string.split('=')

class XorDocumentRead:
    def __init__(self, file_name):
        self.file = open(file_name, encoding="UTF-8")
        self.file_nameCode = file_name
        self.text = self.file.read().split('\n')
    def getAllObjectNames(self):
        result = []
        for x in range(0, len(self.text)):
            try:
                if self.text[x][0] == '[' and not self.text[x][1] == '/':
                    result.append(self.text[x][1:len(self.text[x])-1])
            except:
                pass

        return result
    def getObject(self, object_name):
        result = []
        txtfind = '[' + object_name + ']'
        txtfind2 = "[/" + object_name + ']'
        txtnum = 0
        txtnum2 = 0
        for x in range(0, len(self.text)):
            if self.text[x] == txtfind:
                txtnum = x
            if self.text[x] == txtfind2:
                txtnum2 = x

        for line in self.text[txtnum+1:txtnum2]:
            if not line == '':
                result.append(line[0:-1].split('='))

        return result
    def getFileExtension(self):
        return self.file_nameCode[self.file_nameCode.find('.')+1:]

class XorDocumentWrite:
    def __init__(self, file_name):
        self.file = open(file_name, 'a')
        self.file_nameCode = file_name
    def saveFile(self):
        self.file.close()
    def createObject(self, object_name, parametrs):
        self.file.write('['+object_name+']\n')
        for param in parametrs:
            self.file.write(param+';\n')
        self.file.write("[/" + object_name + ']\n')
    def createEnter(self):
        self.file.write('\n')
    def close(self):
        self.file.close()
    def clear(self):
        open(self.file_nameCode, 'w').write('')