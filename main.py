from mark_and_memos_from_log import extract_mark_and_memo
from draw_image import annotate_pdf

def main():
  extract_mark_and_memo()
  annotate_pdf()
  print("done!")
  return

if __name__ == "__main__":
  main() 