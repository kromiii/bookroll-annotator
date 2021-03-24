# %%
from pdf2image import convert_from_path
from pathlib import Path
import pandas as pd
import os
import glob
import re

from matplotlib.pyplot import imshow
import numpy as np
%matplotlib inline

from PIL import ImageFont, ImageDraw, Image
import img2pdf
# %%
#PDFs : 元となるPDFのパス，PDFのファイル名は，marks,memosのファイル名と同じ
#marks : markerのデータ
#memos : memoのデータ
#font_memo_n : フォントの場所
#fontsize : フォントサイズ
#root_dir : 出力フォルダ

pdfs = glob.glob("pdfs/*.pdf")
marks = pd.read_csv("output_csv/marks_temp.csv")
memos = pd.read_csv("output_csv/memos_temp.csv")
font_memo_n = "/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf"
fontsize=35
root_fol = "imgs/"
# %%
###関数群

##改行を変換（httpをうまく処理）するプログラムを用意
def text_okuri(tex, words):
    tex = " ".join(tex.split(";:::nl:::;"))
    tex0 = tex.split("http")
    textlist = [tex0[0]]
    if len(tex0)>1:
        for ii in range(1,len(tex0)):
            uu = re.split("[ 　)）]",tex0[ii])
            if len(uu)==1: textlist+=["http"+tex0[ii]]
            else: textlist+=["http"+uu[0], tex0[ii].replace(uu[0],"")]
    text0 = ""
    for te in textlist:
        if te[:4]=="http": text0+="\n"+te+"\n"
        else: text0 += "\n".join(["\n".join([text00[i: i+words] for i in range(0, len(text00), words)]) for text00 in te.split(";:::nl:::;")])
    return text0.replace("\n\n","\n")
# %%
##画像の周りにmarginを足す
def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result
# %%
##テキストをimageに出す
def add_text_to_image(img, text, font_path, font_size, font_color, height, width, max_length):
    position = (width, height)
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img)
    if draw.textsize(text, font=font)[0] > max_length:
        while draw.textsize(text + '…', font=font)[0] > max_length:
            text = text[:-1]
        text = text + '…'
    draw.text(position, text, font_color, font=font)
    return img

# %%
##濁音，半濁音の調整
def daku(temp):
    for c in 'かきくけこさしすせそたちつてとはひふへほカキクケコサシスセソタチツテトハヒフヘホ':
        temp=temp.replace(c +'\u3099', chr(ord(c)+1))
    temp = temp.replace('ウ\u3099', 'ヴ')
    for c in 'はひふへほハヒフヘホ':
        temp=temp.replace(c +'\u309a', chr(ord(c)+2))
    return temp
# %%
##imgsに，PDFの画像を保存

pdfnames = [p000.replace(".pdf","").split("/")[-1] for p000 in pdfs]

imgs={}
for i_pdf, pdf in enumerate(pdfs):
    pdf_path = Path(pdf)

    # PDF -> Image に変換（150dpi）
    pages = convert_from_path(str(pdf_path), 150)
    imgs[pdfnames[i_pdf]] = pages
    print(pdfnames[i_pdf])
    print("ページ数", len(pages))
# %%
##実行部分

pi=0
for fna in pdfnames:
    ###名前の，濁音，半濁点の調整．
    if not os.path.exists(root_fol+fna): os.mkdir(root_fol+fna)
    fna0 = daku(fna)
    newimgs=[]
    for pno in range(len(imgs[fna])):
        pi+=1
        print(fna, "p.", pno)
        siz = imgs[fna][pno].size
        if siz[0]>siz[1]:
            im_new = add_margin(imgs[fna][pno].convert('RGBA'), 0, 0, siz[1], 0, (255, 255, 255))
            siz_new = (siz[0], 2*siz[1])
        if siz[0]<=siz[1]:
            im_new = add_margin(imgs[fna][pno].convert('RGBA'), 0, siz[0], 0, 0, (255, 255, 255))
            siz_new = (2*siz[0], siz[1])
    #    imshow(im_new)
    #    imshow()
        memos0 = memos[(memos.contentsname==fna0) & (memos.page_no==pno+1)]
        marks0 = marks[(marks.contentsname==fna0) & (marks.page_no==pno+1)]
        print("画像サイズ:", siz, "memoの数:", len(memos0), "markerの数:", len(marks0))
        memo_n, memo_line=1,1
        words = int(0.9*siz[0]/fontsize)
        for i in memos0.index:
    #        print(i)
            desc0=[int(n) for n in memos.at[i,"desc"].split("-")]
    #        print(desc0)
            xpos = siz[0] * desc0[0]/desc0[2]
            ypos = siz[1] * desc0[1]/desc0[3]
    #        print(xpos,ypos, memos.at[i,"text"])
            text0 = text_okuri(memos.at[i,"text"], words)
            lines = len(text0.split("\n"))
            im_new = add_text_to_image(im_new, "("+str(memo_n)+")", font_memo_n, 50,
                                       (150, 0, 0), ypos, xpos, siz[0])
            if siz[0]>siz[1]:
                im_new = add_text_to_image(im_new, "("+str(memo_n)+") "+text0, font_memo_n, fontsize,
                               (0, 0, 0), siz[1]+fontsize*memo_line+memo_n*4, 100, siz[0])
            elif siz[0]<=siz[1]:
                im_new = add_text_to_image(im_new, "("+str(memo_n)+") "+text0, font_memo_n, fontsize,
                                           (0, 0, 0), fontsize*memo_line+memo_n*4, siz[0], siz[0])
            memo_n+=1
            memo_line += lines
        for i in marks0.index:
            pos0 = [int(n) for n in marks.at[i, "positiontype"].split(",")]
            col0 = [int(n) for n in marks.at[i,"color"].lstrip("rgb(").rstrip(")").split(",")]
    #        print(pos0, col0)
            xst = siz[0] * pos0[0] / pos0[4]
            yst = siz[1] * pos0[1] / pos0[5]
            xsiz = siz[0] * pos0[2] / pos0[4]
            ysiz = siz[1] * pos0[3] / pos0[5]
    #        print(i,xst,yst,xsiz,ysiz)
            rect = Image.new('RGBA', im_new.size)
            draw = ImageDraw.Draw(rect)
            draw.rectangle((xst, yst, xsiz+xst, ysiz+yst), fill=(col0[0],col0[1],col0[2],12)) # 128
            im_new = Image.alpha_composite(im_new,rect)
        im_new.resize((int(siz_new[0]/2),int(siz_new[1]/2))).convert("RGB").save(root_fol+fna+"/"+str(pno)+".jpg")
# %%
# 画像をPDFに変換
for fna in pdfnames:
    pdf_FileName = "output_pdfs/" + fna + ".pdf" # 出力するPDFの名前
    png_Folder = root_fol + fna + "/" # 画像フォルダ
    extension  = ".jpg" # 拡張子がPNGのものを対象
    with open(pdf_FileName,"wb") as f:
        # 画像フォルダの中にあるPNGファイルを取得し配列に追加、バイナリ形式でファイルに書き込む
        f.write(img2pdf.convert([Image.open(png_Folder+j).filename for j in os.listdir(png_Folder) if j.endswith(extension)]))
# %%
