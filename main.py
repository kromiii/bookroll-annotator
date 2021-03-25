from preprocessing import empty_directories
from mark_and_memos_from_log import extract_mark_and_memo
from draw_image import annotate_pdf
import argparse

def main(isscore):
  empty_directories()
  extract_mark_and_memo(isscore)
  annotate_pdf(isscore)
  print("done!")
  return

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--score', default=False)
  args = parser.parse_args()

  main(args.score) 