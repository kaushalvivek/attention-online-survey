import pandas as pd
from scipy.stats import mannwhitneyu, wilcoxon, ttest_ind, normaltest, shapiro

users = pd.read_csv('data/users.csv')
users['id'] = users['u_id']
users = users.set_index('u_id')
transactions = pd.read_csv('data/transactions.csv')
transactions = transactions.set_index('u_id')

# column to find out whether clickbait or non-clicbait clicked
transactions['non-clickbait'] = transactions['article_id']%2
transactions['clickbait'] = 1-transactions['non-clickbait']

joined_table = transactions.join(users, how="left", lsuffix="_trans", rsuffix="_user")
science = joined_table.loc[joined_table['edu_stream']=="Science"]
mass_comm = joined_table.loc[joined_table['edu_stream']=="MassComm"]


def print_analysis_summary(table):
  # Get click by position
  output = table.groupby("position").count()
  print ("Clicks by position on page : ")
  print(output['article_id'])
  
  # Get count of  clickbait clickbed vs non-clickbait clicked
  article_id = table["article_id"].to_list()
  ncb = 0
  cb = 0
  for i in article_id:
    if i%2 == 0:
      cb+=1
    else:
      ncb+=1
  print("Total Clickbaits clicked : " + str(cb))
  print("Total Non-Clickbaits clicked : " + str(ncb))

  # find out likelihood of clickbait being clicked over non-clickbait
  print("T-Test (clicking on clickbait, over non-clickbait) p : " + str(ttest_ind(table['clickbait'], table['non-clickbait'],equal_var=False).pvalue))
  # print("Wilcoxon (clicking on clickbait, over non-clickbait) p : " + str(wilcoxon(table['clickbait'], table['non-clickbait']).pvalue))

  # # First article read
  first_read = table.loc[table['sequence'] == 1]['clickbait']
  print("First Article read counts : ")
  print("Clickbait count : " + str(first_read.tolist().count(1)))
  print("Non-Clickbait count : " + str(first_read.tolist().count(0)))

print("\n ALL :\n")
print_analysis_summary(transactions)
print("\n SCIENCE :\n")
print_analysis_summary(science)
print("\n MASS COMM :\n")
print_analysis_summary(mass_comm)


