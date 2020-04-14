import pandas as pd
from scipy.stats import mannwhitneyu, wilcoxon, ttest_ind, normaltest, shapiro

users = pd.read_csv('users.csv')
transactions = pd.read_csv('transactions.csv')

# ----------------------------------------------------------

# Get click by position
# print(transactions.groupby("position").count())

# ----------------------------------------------------------

# Get count of  clickbait clickbed vs non-clickbait clicked
article_id = transactions["article_id"].to_list()
ncb = 0
cb = 0
for i in article_id:
  if i%2 == 0:
    cb+=1
  else:
    ncb+=1

print("Clickbaits clicked : " + str(cb))
print("Non-Clickbaits clicked : " + str(ncb))

# ------------------------------------------------------------

# Get likelihood of anyone to click clickbait vs non-clickbait
transactions['non-clickbait'] = transactions['article_id']%2
transactions['clickbait'] = 1-transactions['non-clickbait']

print(transactions)

print("T-Test (clicking on clickbait, over non-clickbait) p : " + str(ttest_ind(transactions['clickbait'], transactions['non-clickbait'],equal_var=False).pvalue))

# ------------------------------------------------------------

# time on page
cb_time_on_page = transactions.loc[transactions['clickbait'] == 1]['time_on_page']
ncb_time_on_page = transactions.loc[transactions['clickbait'] == 0]['time_on_page']
print(ncb_time_on_page)
print("Clickbait median : " + str(cb_time_on_page.median()))
print("Clickbait mean : " + str(cb_time_on_page.mean()))
print("Non-Clickbait median : " + str(ncb_time_on_page.median()))
print("Non-Clickbait mean : " + str(ncb_time_on_page.mean()))

print("T-Test (time on article clickbait vs non-clickbait) p : " + str(ttest_ind(cb_time_on_page, ncb_time_on_page,equal_var=False).pvalue))

print(normaltest(cb_time_on_page).pvalue)
print(normaltest(ncb_time_on_page).pvalue)

# # ------------------------------------------------------------

# First article read
first_read = transactions.loc[transactions['sequence'] == 1]['clickbait']
print(first_read)

# summary_data = {
#   'user_id':,
#   'age':final_index,
#   '':final_cb_or_not,
#   'real_or_madeup':final_real_made_up,
#   'mean':mean,
#   'median':median,
#   'mode':mode,
#   'std_deviation': std,
#   'response_count':count
# }