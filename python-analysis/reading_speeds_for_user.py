# reading speed is difficult to compute
# because we don't know whether the user really
# fully read the article

# strategies
# - analyze
#   - only articles that are liked (not a very good approach because there are users who might not use the like button)
#   - only articles that were interacted with for more than a number seconds

ANALYZE_ONLY_LIKED = False
MIN_ART_DURATION_IN_SEC = 180

PRINT_DETAIL = True

USER_ID = 2465
READING_LANGUAGE = "fr"  #'nl'

# 1911
# 2650, fr = impossibly high speeds


from zeeguu.core.model import User, UserArticle, Language
from zeeguu.core.model.user_activitiy_data import UserActivityData
from macro_session import MacroSession


def find_the_like_event(user, article):
    all_events = UserActivityData.find(user, article)
    like_events = [each for each in all_events if each.event == "UMR - LIKE ARTICLE"]
    return like_events


def extract_macro_sessions_from_db(user, language_id):

    # this is a bit imprecise; there might be multiple
    # macro sessions of the same article;
    # ... we should think about a solution for users
    # that read the same article in multiple sessions

    macro_sessions = []

    current_macro = None

    for session in user.all_reading_sessions(language_id=language_id):

        user_article = UserArticle.find(user, session.article)

        if not user_article:
            continue

        if not current_macro or session.article != current_macro.article:
            current_macro = MacroSession(user_article)
            macro_sessions.append(current_macro)

        current_macro.append(session)

    return macro_sessions


def filter_sessions(macro_sessions):

    result = []
    for macro_session in macro_sessions:

        if ANALYZE_ONLY_LIKED and not macro_session.user_article.liked:
            continue

        if macro_session.total_time < MIN_ART_DURATION_IN_SEC:
            continue

        result.append(macro_session)
    return result


if __name__ == "__main__":

    user = User.find_by_id(USER_ID)
    language_id = Language.find(READING_LANGUAGE).id

    macro_sessions = extract_macro_sessions_from_db(user, language_id)
    macro_sessions = filter_sessions(macro_sessions)

    for macro_session in macro_sessions:
        if PRINT_DETAIL:
            macro_session.print_details()
            input("<Enter to continue>")
        else:
            macro_session.print_summary()
