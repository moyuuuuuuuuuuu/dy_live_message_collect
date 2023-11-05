import pandas, os


class Importer:
    def __init__(self):
        self.writer = pandas.ExcelWriter

    def load(self, file_path=''):
        if not os.path.exists(file_path):
            raise FileNotFoundError('File not found')
        self.dataFrame = pandas.read_excel(file_path)

    def toList(self):
        dataList = []
        for key, item in self.dataFrame.to_dict().items():
            for i in item:
                if len(dataList) < i + 1:
                    dataList.append([{key: item[i]}])
                else:
                    dataList[int(i)].append({key: item[i]})
        return dataList

    def getDataFrame(self):
        return self.dataFrame

    def getColumns(self):
        return list(self.dataFrame.columns)
