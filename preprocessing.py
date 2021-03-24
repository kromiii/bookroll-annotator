import os
import shutil

def empty_directories():
  empty_directory("output_pdfs")
  empty_directory("temp/imgs")
  empty_directory("temp/output_csv")

def empty_directory(target_dir):
  shutil.rmtree(target_dir)
  os.mkdir(target_dir)
  with open(target_dir + '/.keep', 'w') as f:
      f.write('')