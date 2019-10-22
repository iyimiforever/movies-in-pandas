import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 从用户表读取用户信息
users = pd.read_table('users.dat', header=None, names=['UserID','Gender','Age','Occupation','Zip-code'],
                      sep='::',engine='python')

# 打印列表长度，共有6040条记录
print(len(users))

# 查看前五条记录
print(users.head(5))

# 同样方法，导入电影评分表
ratings = pd.read_table('ratings.dat', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'],
                        sep='::',engine='python')
# 打印列表长度
print(len(ratings))
print(ratings.head(5))
# 导入电影数据表
movies = pd.read_table('movies.dat', header=None, names=['MovieID', 'Title', 'Genres'],
                       sep='::',engine='python')
print(len(movies))
print(movies.head(5))


# 要进行数据分析，将多张表进行合并才有助于分析
# 先将users与ratings两张表合并再跟movies合并
data = pd.merge(pd.merge(users, ratings), movies)
print(data.head(10))

data.describe()
data.info()

# 合并后的每一条记录反映了每个人的年龄，职业，性别，邮编，电影ID，评分，时间戳，电影信息，电影分类等一系列信息
print('比如我们查看用户id为12的所有信息')
print(data[data.UserID==12])

print('查看每一部电影不同性别的平均评分 data_gender接收')
data_gender=data.pivot_table(index='Title',columns='Gender',values='Rating')
print(data_gender.head())

print('查看电影分歧最大的那部电影，在原数据中体现')
data_gender['diff']=np.abs(data_gender.F-data_gender.M)
print(data_gender.shape)
print(data_gender.head(10))

print('男女电影分歧最大进行排序 data_gender_sorted接收')
data_gender_sorted=data_gender.sort_values(by='diff',ascending=False)
print(data_gender_sorted.head())

print('算出每部电影平均得分并对其进行排序 data_mean_rating 接收')
data_mean_rating=data.pivot_table(index='Title',values='Rating')
data_mean_rating['size'] = data_mean_rating.head()
print(data_mean_rating['size'] )

print('对电影平均得分排序')
data_mean_rating_sorted=data_mean_rating.sort_values(by='Rating',ascending=False)
print(data_mean_rating_sorted.head())

print('查看评分次数多的电影并进行排序   data_rating_num接收')
data_rating_num = pd.crosstab(data.Title, data.Rating)
data_rating_num['count'] = np.sum(data_rating_num, axis=1)
print(data_rating_num.head())

print('进行排序')
data_rating_num_sorted = data_rating_num.sort_values(by='count',ascending=False)
print(data_rating_num_sorted.shape)
print(data_rating_num_sorted.head())

print('过滤掉评分条目数不足250条的电影')
data_rating_num_sorted = data_rating_num_sorted[data_rating_num_sorted['count']>250]
print(data_rating_num_sorted.shape)

print('对评分数量进行排序，并取前20条数据')
print(data_rating_num_sorted.head(20))

print('评分最高的十部电影')
movies_stats=data.groupby('Title').agg({'Rating':[np.size,np.mean]})
print(movies_stats.head(10))
# 被评论的次数>=100
atleast_100=movies_stats['Rating']['size']>=100
movies_stats[atleast_100].sort_values([('Rating','mean')],ascending=False)[:10]
print(movies_stats.head(10))

print('对数据进行规整-movies')
movie_clean_1=pd.DataFrame(movies.Genres.str.split('|').tolist(),index=movies.MovieID)
print(movie_clean_1.head())
movie_clean_2=movie_clean_1.stack().reset_index()
print(movie_clean_2.head())


print('删除level_1列，将columns为0的列重命名为genres,并重新定义数据框为movies_genres')
movies_genres=movie_clean_2.drop('level_1',axis=1).rename(columns={0:'Genres'})
print(movies_genres.head())


print('将原movies数据中的genres列替换成movies_genres，得到规整化处理后的movies数据')
movies=pd.merge(movies.drop('Genres',axis=1),movies_genres)
print(movies.head(10))

print('合并。构建电影评分数据集movie_ratings')
movie_ratings=ratings.merge(movies.drop('Title',axis=1),how='inner',on='MovieID')
print(movie_ratings.head())

print('计算movies_ratings中不同类型电影的频数')
movies_ratings_sorted=movie_ratings.groupby(['Genres'])['MovieID'].size()
movies_ratings_sorted.sort_values(ascending=False).plot(kind='bar')
# movies_ratings_sorted.
plt.xticks(rotation=45)
plt.show()


# print('用户年龄统计')
# labels=['0-9','10-19','20-29','30-39','40-49','50-59','60-69','70-79']
# data['age_group']=pd.cut(data.Age,range(0,81,10),labels=labels)
# data.head()
# data['age_group'].value_counts().plot(kind='bar')
# plt.xticks(rotation=45)
# plt.show()

# print('各年龄段电影观看量')
# users.Age.plot.hist(bins=30)
# plt.title('users_ages')
# plt.xticks(rotation=45)
# plt.xlabel('age')
# plt.ylabel('count of age')
# plt.show()