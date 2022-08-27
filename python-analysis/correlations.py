import pandas as pd
from tqdm import tqdm

READING_LANGUAGE = "nl"


from zeeguu.core.model import User, UserActivityData, Language, UserLanguage, Article
from scipy import stats

languages_to_analyze = Language.CODES_OF_LANGUAGES_THAT_CAN_BE_LEARNED # [:-2]

def articles_correlations():
	articles_df = pd.DataFrame(columns=["id", "lang", "difficulty", "word_count", "title_length", "opened", "translated", "spoken", "liked", "closed"])
	all_users = User.find_all()
	print(len(all_users))
	for reading_language in languages_to_analyze:
		print("\nLANGUAGE:", reading_language)
		language_id = Language.find(reading_language).id
		for user in tqdm(all_users):
			if user.learned_language_id == language_id:
				events = UserActivityData.find(user)
				for event in events:
					article_id = event.article_id
					if article_id:
						article_data = Article.find_by_id(article_id)
						if article_data.language_id == language_id:
							if not (articles_df['id'] == article_id).any():
								title_len = len(article_data.title.split())
								df = {"id":article_id, "lang":article_data.language_id, "difficulty":article_data.fk_difficulty, "word_count":article_data.word_count, "title_length":title_len, "opened":0, "translated":0, "spoken":0, "liked":0, "closed":0}
								articles_df = articles_df.append(df, ignore_index = True)
							if event.event == "UMR - OPEN ARTICLE":
								articles_df.loc[articles_df.id == article_id, 'opened'] += 1
							if event.event == "UMR - TRANSLATE TEXT":
								articles_df.loc[articles_df.id == article_id, 'translated'] += 1
							if event.event == "UMR - SPEAK TEXT":
								articles_df.loc[articles_df.id == article_id, 'spoken'] += 1
							if event.event == "UMR - LIKE ARTICLE":
								articles_df.loc[articles_df.id == article_id, 'liked'] += 1
							if event.event == "UMR - ARTICLE CLOSED":
								articles_df.loc[articles_df.id == article_id, 'closed'] += 1

		print("Articles:", len(articles_df))

		correlation_variables = ["word_count", "difficulty", "liked", "translated", "spoken", "opened", "closed", "title_length"]
		# word count & fk_difficulty
		spearman_corr = stats.spearmanr(articles_df[correlation_variables[0]], articles_df[correlation_variables[1]])
		print(correlation_variables[0], correlation_variables[1], spearman_corr[0], spearman_corr[1])
		# liked & fk_difficulty
		spearman_corr = stats.spearmanr(articles_df[correlation_variables[2]], articles_df[correlation_variables[1]])
		print(correlation_variables[2], correlation_variables[1], spearman_corr[0], spearman_corr[1])
		# number of translations & difficulty
		spearman_corr = stats.spearmanr(articles_df[correlation_variables[3]], articles_df[correlation_variables[1]])
		print(correlation_variables[3], correlation_variables[1], spearman_corr[0], spearman_corr[1])
		# number of spoken words & difficulty
		spearman_corr = stats.spearmanr(articles_df[correlation_variables[4]], articles_df[correlation_variables[1]])
		print(correlation_variables[4], correlation_variables[1], spearman_corr[0], spearman_corr[1])
		# number of times article is opened & difficulty
		spearman_corr = stats.spearmanr(articles_df[correlation_variables[5]], articles_df[correlation_variables[1]])
		print(correlation_variables[5], correlation_variables[1], spearman_corr[0], spearman_corr[1])
		# number of times article is closed & difficulty
		spearman_corr = stats.spearmanr(articles_df[correlation_variables[6]], articles_df[correlation_variables[1]])
		print(correlation_variables[6], correlation_variables[1], spearman_corr[0], spearman_corr[1])
		# title length & fk_difficulty
		spearman_corr = stats.spearmanr(articles_df[correlation_variables[7]], articles_df[correlation_variables[1]])
		print(correlation_variables[7], correlation_variables[1], spearman_corr[0], spearman_corr[1])
		# title length & number of times article is opened
		spearman_corr = stats.spearmanr(articles_df[correlation_variables[5]], articles_df[correlation_variables[7]])
		print(correlation_variables[5], correlation_variables[7], spearman_corr[0], spearman_corr[1])


def users_correlations():
	users_df = pd.DataFrame(columns=["id", "reading_lang", "native_lang", "opened", "translated", "spoken", "liked", "closed"])
	all_users = User.find_all()
	print(len(all_users))
	#for reading_language in languages_to_analyze:
	#	print("\nLANGUAGE:", reading_language)
	#	language_id = Language.find(reading_language).id
	for user in tqdm(all_users):
		#if user.learned_language_id == language_id:

		df = {"id":user.id, "reading_lang":str(user.learned_language), "native_lang":str(user.native_language), "opened":0, "translated":0, "spoken":0, "liked":0, "closed":0}
		users_df = users_df.append(df, ignore_index = True)

		# todo: check all possible events
		events = UserActivityData.find(user)
		for event in events:
			article_id = event.article_id
			if article_id:
				if event.event == "UMR - OPEN ARTICLE":
					users_df.loc[users_df.id == user.id, 'opened'] += 1
				if event.event == "UMR - TRANSLATE TEXT":
					users_df.loc[users_df.id == user.id, 'translated'] += 1
				if event.event == "UMR - SPEAK TEXT":
					users_df.loc[users_df.id == user.id, 'spoken'] += 1
				if event.event == "UMR - LIKE ARTICLE":
					users_df.loc[users_df.id == user.id, 'liked'] += 1
				if event.event == "UMR - ARTICLE CLOSED":
					users_df.loc[users_df.id == user.id, 'closed'] += 1

	# keep only users that opened at least 1 article
	users_df.drop(users_df[users_df.opened < 1].index, inplace=True)

	print("Users:", len(users_df))

	print(users_df['native_lang'].value_counts())
	print("---")
	print(print(users_df['reading_lang'].value_counts()))


if __name__== "__main__":
    #articles_correlations()
	users_correlations()
