# reading speed is difficult to compute 
# because we don't know whether the user really
# fully read the article 

# strategies 
# - analyze 
#   - only articles that are liked (not a very good approach because there are users who might not use the like button)
#   - only articles that were interacted with for more than a number seconds



STUDY_ONLY_LIKED = False
MIN_ART_DURATION_IN_SEC = 180


USER_ID = 2465 
# 1911
# 2650 = impossibly high speeds

READING_LANGUAGE = 'fr' #'nl'
PRINT_DETAIL = True

import math
from collections import defaultdict

from zeeguu.core.model import User, UserArticle, Language, user_reading_session
from zeeguu.core.model.user_activitiy_data import UserActivityData


class MacroSession(object):

    def __init__(self):
        self.sessions = []
        self.total_time = 0

    def append(self, session):
        self.sessions.append(session)
        self.total_time += session.duration / 1000

    def items(self):
        return self.sessions.items()

    def print_details(self):
        print("\tSessions: ")
        for session in self.sessions:
            print(f"\t{session.start_time}, {session.duration / 1000}s")
        print(" ")



def find_the_like_event(user, article):
    all_events = UserActivityData.find(user, article)
    all_events = [each for each in all_events if each.event == "UMR - LIKE ARTICLE"]
    for each in all_events:
        if PRINT_DETAIL:
            print(f" - {each.time}: LIKE: {each.value}")


def print_sesssions_for_articles(user, article_macro_sessions):

    for user_article in article_macro_sessions.keys():
        article = user_article.article
        macro_session = article_macro_sessions[user_article]

        



        
        reading_speed = int (article.word_count * 60 / macro_session.total_time)


        if PRINT_DETAIL:
            
            print(f"\n *** {article.title}\n")
           
            if user_article.liked:
                print("\tLIKED!")            

            print(f"\tTotal time: {round(macro_session.total_time/60,1)}min")
            print(f"\tWord count: {article.word_count}")
            print(f"\tReading speed: {reading_speed} wpm")
            print("")
            macro_session.print_details()
            input("<Enter to continue>")
            print("")
        
            

    


def macro_sessions_per_article(user, language_id):

    # this is imprecise; there might be multiple
    # macro sessions of the same article; 
    # ... as a solution, we should only be 
    # keeping the first macro reading session 

    macro_sessions = defaultdict(MacroSession)
    
    for session in user.all_reading_sessions(language_id=language_id):

        user_article = UserArticle.find(user, session.article) 
        
        if not user_article:
            continue

        macro_sessions[user_article].append(session)

    return macro_sessions




def filter_sessions(macro_sessions):

    result = {}
    for ua, macro_session in macro_sessions.items():
        
        if STUDY_ONLY_LIKED and not ua.liked:
            continue

        if macro_session.total_time < MIN_ART_DURATION_IN_SEC:
            continue
        
        result[ua] = macro_session
    return result
 
        

if __name__== "__main__":

    user = User.find_by_id(USER_ID)
    language_id = Language.find(READING_LANGUAGE).id
    macro_sessions = macro_sessions_per_article(user, language_id)
    macro_sessions = filter_sessions(macro_sessions)
    print_sesssions_for_articles(user, macro_sessions)


