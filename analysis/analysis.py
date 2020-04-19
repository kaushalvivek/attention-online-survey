import pandas as pd
from scipy.stats import mannwhitneyu, wilcoxon, ttest_ind, normaltest, shapiro

users = pd.read_csv('data/users.csv')
transactions = pd.read_csv('data/transactions.csv')

# column to find out whether clickbait or non-clicbait clicked
transactions['non-clickbait'] = transactions['article_id']%2
transactions['clickbait'] = 1-transactions['non-clickbait']

# ----------------------------------------------------------

# Get click by position
output = transactions.groupby("position").count()
print ("Clicks by position on page : ")
print(output['article_id'])

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

print("Total Clickbaits clicked : " + str(cb))
print("Total Non-Clickbaits clicked : " + str(ncb))

# # ------------------------------------------------------------
# find out likelihood of clickbait being clicked over non-clickbait
# # print(transactions)
print("T-Test (clicking on clickbait, over non-clickbait) p : " + str(ttest_ind(transactions['clickbait'], transactions['non-clickbait'],equal_var=False).pvalue))

# # ------------------------------------------------------------

# time on page
# cb_time_on_page = transactions.loc[transactions['clickbait'] == 1]['time_on_page']
# ncb_time_on_page = transactions.loc[transactions['clickbait'] == 0]['time_on_page']
# print(ncb_time_on_page)
# print("Clickbait median : " + str(cb_time_on_page.median()))
# print("Clickbait mean : " + str(cb_time_on_page.mean()))
# print("Non-Clickbait median : " + str(ncb_time_on_page.median()))
# print("Non-Clickbait mean : " + str(ncb_time_on_page.mean()))

# print("T-Test (time on article clickbait vs non-clickbait) p : " + str(ttest_ind(cb_time_on_page, ncb_time_on_page,equal_var=False).pvalue))

# print(normaltest(cb_time_on_page).pvalue)
# print(normaltest(ncb_time_on_page).pvalue)

# # # ------------------------------------------------------------

# # First article read
first_read = transactions.loc[transactions['sequence'] == 1]['clickbait']
print("First Article read counts : ")
print("Clickbait count : " + str(first_read.tolist().count(1)))
print("Non-Clickbait count : " + str(first_read.tolist().count(0)))
