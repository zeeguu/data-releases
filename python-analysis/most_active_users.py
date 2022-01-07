from zeeguu.core.model import User, UserActivityData


def print_sorted_activity():
	all_users = User.find_all()

	# analyze only the last 100 users
	all_users = all_users[-100:]

	user_activity = {}
	for user in all_users:
		print(f"({user.id}) Analyzing {user.name}... ")
		events = UserActivityData.find(user)
		user_activity[user] = events

	sorted_activity = sorted(user_activity.items(), key=lambda item: len(item[1]))
	for user, activity in sorted_activity:
		print(f"{user.id}, {user.name}, {len(activity)}")

if __name__=='__main__':
	print_sorted_activity()
