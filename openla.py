#%%
import pandas as pd
import numpy as np
import openLA as la
# %%
course_info = la.CourseInformation(files_dir="data", course_id="1")
# %%
scores = course_info.user_score()
# %%
np.array(scores).mean()
# --> 72.3
# %%
users = course_info.user_id()
high_score_users = course_info.users_in_selected_score(users, top=100, bottom=72.3)
# %%
print(len(users), len(high_score_users))
# %%
event_stream = course_info.load_eventstream()
# %%
user_stream = la.select_user(event_stream, high_score_users)
# %%
contents_df = pd.read_csv("data/Course_1_LectureMaterial.csv")
contents = course_info.contents_id()

# %%
content_index = 10 # 第6回
user_content_stream = la.select_contents(user_stream, contents[content_index])
# %% 滞在時間の多いページを抽出
pagewise_aggregation = la.convert_into_page_wise(
  event_stream=user_content_stream,
  invalid_seconds=10,
  timeout_seconds=10*60,
  count_operation=True
)
# %%
pagewise_aggregation.df.groupby("pageno").mean().sort_values("reading_seconds", ascending=False)
# %%
