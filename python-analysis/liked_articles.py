# all articles for a user and language that the usr liked

USER_ID = 534
LANG = "de"

from zeeguu.core.model import User

def print_liked_articles():
    user = User.find_by_id(USER_ID)

    for user_article in user.liked_articles():
        article = user_article.article
        if article.language.code != LANG:
            continue

        print(f"{article.word_count}, {article.fk_difficulty}, {article.title}")


if __name__== "__main__":
    print_liked_articles()
