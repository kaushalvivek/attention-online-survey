import pandas as pd
from scipy.stats import mannwhitneyu, wilcoxon, ttest_ind, normaltest, shapiro, binom

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
male = joined_table.loc[joined_table['gender']=="Male"]
female = joined_table.loc[joined_table['gender']=="Female"]
joined_table.to_excel("data/joined.xlsx")
joined_table.to_csv("data/joined.csv")

def print_analysis_summary(table):
  
  # Get click by position
  output = table.groupby("position").count()
  print ("Clicks by position on page : ")
  print(output['article_id'])
  print("")
  
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
  print("")

  # find out likelihood of clickbait being clicked over non-clickbait
  # prob = table.groupby("u_id").sum()
  # clickbait = prob['clickbait'].tolist()
  # clickbait = [i/3 for i in clickbait]
  # non_clickbait = [1-i for i in clickbait]
  # print("Wilcoxon (on probability) p : " + str(wilcoxon(clickbait, non_clickbait).pvalue))
  print("")
  # # First article read
  first_read = table.loc[table['sequence'] == 1]['clickbait']
  print("First Article read counts : ")
  print("Clickbait count : " + str(first_read.tolist().count(1)))
  print("Non-Clickbait count : " + str(first_read.tolist().count(0)))

def wilcox(table1, table2):
  prob1 = table1.groupby("u_id").sum()
  clickbait1 = prob1['clickbait'].tolist()
  clickbait1 = [i/3 for i in clickbait1]
  prob2 = table2.groupby("u_id").sum()
  clickbait2 = prob2['clickbait'].tolist()
  clickbait2 = [i/3 for i in clickbait2]
  print("Wilcoxon (science v masscomm) p : " + str(wilcoxon(clickbait1, clickbait2).pvalue))

def mannwhitney(table1, table2):
  prob1 = table1.groupby("u_id").sum()
  clickbait1 = prob1['clickbait'].tolist()
  clickbait1 = [i/3 for i in clickbait1]
  prob2 = table2.groupby("u_id").sum()
  clickbait2 = prob2['clickbait'].tolist()
  clickbait2 = [i/3 for i in clickbait2]
  print("Mannwhitney (male v female) p : " + str(mannwhitneyu(clickbait1, clickbait2).pvalue))

print("\n ALL :\n")
print_analysis_summary(transactions)
print("\n SCIENCE :\n")
print_analysis_summary(science)
print("\n MASS COMM :\n")
print_analysis_summary(mass_comm)
print("\n FEMALE :\n")
print_analysis_summary(female)
print("\n MALE :\n")
print_analysis_summary(male)
print("\n SIGNIFICANCE :\n")
wilcox(mass_comm, science)
mannwhitney(male, female)