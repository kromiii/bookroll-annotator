# %%
import pandas as pd
import numpy as np

# %%
def extract_mark_and_memo():
    csv = pd.read_csv("logdata/eventstream.csv")
    ##取り除くイベント名一覧
    rem = ["LINK_CLICK","NEXT","OPEN","CLOSE","QUIZ_ANSWER_CORRECT","TIMER_PAUSE",
        "PAGE_JUMP","BOOKMARK_JUMP","DELETE BOOKMARK","CLOSE_RECOMMENDATION",
        "PREV","OPEN_RECOMMENDATION","REGIST CONTENTS","ADD BOOKMARK",
        "ADD_HW_MEMO"] + ["MEMO_TEXT_CHANGE_HISTORY"]
    # print("marker関係，memo関係のイベントの回数")
    for op in set(csv.operationname):
        if not op in rem:
    #        if len(csv[csv.operationname==op])<100:
    #            display(csv[csv.operationname==op])
            print(op, len(csv[csv.operationname==op]))
    ##marker関係のイベント名
    mas = ["ADD MARKER",
    "DELETE MARKER"]
    ##marker関係のイベント一覧
    csv_mark=csv[csv['operationname'].isin(mas)].sort_values("operationdate").reset_index(drop=True)
    ##memo関係のイベント名，MEMO_TEXT_CHANGE_HISTORYの書いていく履歴は今回使っていない
    mes= ["CHANGE MEMO",
    "DELETE_MEMO",
    "ADD MEMO"]#,"MEMO_TEXT_CHANGE_HISTORY"]
    ##memo関係のイベント一覧
    csv_memo=csv[csv['operationname'].isin(mes)].sort_values("operationdate").reset_index(drop=True)   

    uu=0
    droplist = []
    print("DELETE MARKERの表示")
    for i in csv_mark.index:
        ids = [csv_mark.at[i, "ssokid"],csv_mark.at[i, "contentsid"],csv_mark.at[i, "positiontype"],csv_mark.at[i, "page_no"]]   
        csv0 = csv_mark[(csv_mark["ssokid"]==ids[0]) &
                        (csv_mark["contentsid"]==ids[1]) &
                        (csv_mark["positiontype"]==ids[2]) &
                        (csv_mark["page_no"]==ids[3])]
        ##作成者も，書き込み先も，場所も，ページ番号も同じだが複数行ある場合の操作
        if len(csv0)>1:
            ##もし，ADDとDELETEがセットなら全部削除
            if set(csv0.operationname) == {"ADD MARKER","DELETE MARKER"}:
                droplist+=list(csv0.index)
            else:
                print("複数行あるのに，ADD, DELETEの2種類だけでない場合．ADDだけなら，まぁいい")
                # display(csv0)
        ##もし，DELETE MARKERだけあるときに，目視できるよう確認
        elif csv_mark.at[i,"operationname"]=="DELETE MARKER":
            csv00 = csv_mark[(csv_mark["positiontype"]==ids[2])]
            # display(csv00)

    marks = csv_mark.drop(droplist)

    print("ADDかDELETEしか残っていないのを確認 ")
    print(set(marks.operationname))

    print("まだ残っているDELETE MARKERを念の為，確認")
    # display(marks[marks.operationname=="DELETE MARKER"])
    marks = marks[marks.operationname=="ADD MARKER"]
    memos = csv_memo.drop("text", axis=1).rename({"description": "desc", "memo_text": "text"}, axis=1)
    memos["text"] = memos.text.str.replace(";:::nl:::;", " ")
    memos = memos[memos.text.notnull()]

    marks.to_csv("temp/output_csv/marks.csv",index=False)
    memos.to_csv("temp/output_csv/memos.csv",index=False)

    print("extracted information from logs.")