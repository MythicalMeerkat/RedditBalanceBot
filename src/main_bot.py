# Jeffrey A. Wilson
# Created: Aug. 5, 2018
# Entry point for Running the Reddit Bot


import praw  # Reddit API Wrapper
import config
import time  # For Timer Functions
import os
import datetime  # For Checking Time of Day

phrase = "perfectly balanced"
banned_subreddits = config.banned_subreddits

#######################################################
# Grab profile credentials from the private config file
# return the profile object to the calling routine of
# the script.
#######################################################


def bot_login():
    r = praw.Reddit(username=config.username,
                    password=config.password,
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent="Ensures all comments are perfectly balanced.")

    return r

#######################################################
# This function will be executed on a loop in the
# calling routine. Scans the comments looking for the
# phrase and replies to it. Logs the comment ID to
# make sure we don't reply to the same comment multiple
# times. Takes in the bot's profile (p) and comments
# previously replied to as parameters.
#######################################################


def run_bot(p, comments_replied_to, prev_replies):
    amount_of_comments = 0
    replied = False
    print("\nObtaining comments...")

    for comment in p.subreddit('Test').comments(limit=100):
        if phrase in comment.body.lower() and comment.id not in comments_replied_list and comment.author != p.user.me():
            comment.reply("As all things should be")
            print("Replied to comment " + comment.id)
            replied = True
            amount_of_comments += 1

            comments_replied_to.append(comment.id)

            with open("comments_replied_to.txt", "a") as file:
                file.write(comment.id + "\n")

    if not replied:
        print("Did not reply to any comments")

    # write_number_of_replies_to_file(amount_of_comments, prev_replies)

    return

#######################################################
# Grabs the log of previously replied comments. If the
# file exists stores the data from it into a
# list. If it doesn't, create an empty list. Return the
# list to the calling routine.
#######################################################


def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))

    return comments_replied_to

#######################################################
# Grabs the log of lifetime comment replies. If the
# file exists stores the data from it into a
# list. If it doesn't, create an empty list. Return the
# list to the calling routine.
#######################################################


def get_number_of_replies():
    if not os.path.isfile("lifetime_replies.txt"):
        total_replies = 0

    else:
        with open("lifetime_replies.txt", "r") as f:
            total_replies = f.read()

    return


def write_number_of_replies_to_file(amount, prev_replies):
    # total = (amount + prev_replies)
    # with open("lifetime_replies.txt", "w") as file:
    #    file.write(str(total))

    return


#############################################
# Entry point (Main) for running the script #
#############################################

# Should only be executed once
bot_profile = bot_login()
comments_replied_list = get_saved_comments()
lifetime_replies = get_number_of_replies()

while True:
    run_bot(bot_profile, comments_replied_list, lifetime_replies)

    # Sleep so we can chill a bit and reduce potential spam
    print("Sleeping for 20 seconds")
    time.sleep(20)


#############################################
# End of Script                             #
#############################################
