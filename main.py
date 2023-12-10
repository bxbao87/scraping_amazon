import pandas as pd
import math
import subprocess
import os

input_file = "input/testing.xlsx"
column_name = "Asin Advertised"
sheet_name = "Sheet1"
output_folder = "output/"
num = 2

def createFolder(path = r"amazon/"):
    print("Creating folder...")

    if not os.path.exists(path):
        os.makedirs(path)

    return path

df = pd.ExcelFile(input_file).parse(sheet_name)
res = df[column_name].tolist()

n = len(res)
m = math.ceil(n / num)
print("Total asins", n)
print("Total processes", m)

def func(partition):
  args = ["D:\\application\\anaconda3\\envs\\huy\\python.exe", "script.py", "-i", input_file, "-s", sheet_name, "-o", output_folder, "-p", str(partition), "-n", str(num)]
  subprocess.Popen(args)

if __name__ == "__main__":
    createFolder(output_folder)

    for i in range(m):
        print("process ", i)
        func(i)