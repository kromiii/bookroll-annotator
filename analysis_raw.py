# %%
import pandas as pd
import numpy as np
# %% 生データを読み込み
eventstream = pd.read_csv("data/eventstream_raw.csv")
# %% 教材一覧を読み込み
contents = pd.read_csv("data/Course_1_LectureMaterial.csv")
# %% ユーザー一覧を読み込み
users = pd.read_csv("data/Course_1_QuizScore.csv")
# %%
high_score_users = list(users[users.score > 73.5].userid)
# %% 第6回の教材を読み込み
contentsid = contents.contentsid[10]
# %%
def extract_info(eventstream, userid, contentsid):
  es = eventstream.query("ssokid in @userid & contentsid == @contentsid & diftime < 10*60")
  memo = es[(es.memo_text.notnull()) & (es.operationname != "MEMO_TEXT_CHANGE_HISTORY")][["page_no", "operationname", "memo_text"]]
  marker = es.query("operationname == 'ADD MARKER'")[["page_no", "positiontype"]]
  timespent = es.groupby("page_no").sum().sort_values("diftime")["diftime"].reset_index()
  memo.to_csv("output_csv/memo.csv", index=False)
  marker.to_csv("output_csv/marker.csv", index=False)
  timespent.to_csv("output_csv/timespent.csv", index=False)
  return "success"
# %%
extract_info(eventstream, high_score_users, contentsid)
# %%
eventstream_high = eventstream.query("ssokid in @high_score_users.userid")
# %% 第6回の教材を読み込み
contentsid = contents.contentsid[10]
eventstream_filtered = eventstream_high.query("contentsid == @contentsid")
# %%
es = eventstream_filtered.query("diftime > 3 & diftime < 10*60")
# %% 滞在時間の多いページを抽出
es.groupby("page_no").sum().sort_values("diftime")["diftime"]
# %% ページごとにメモの内容を抽出
es[es.memo_text.notnull()][["page_no", "memo_text"]]

# %% ページごとにマーカー箇所を抽出
es.query("operationname == 'ADD MARKER'")[["page_no", "positiontype"]]
# %%
