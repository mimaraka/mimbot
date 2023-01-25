import csv
import discord
import random



# raika
async def proc(itrc, ctx, n=1):
    raika_tweets = []
    # CSVファイルから読み込み
    with open("data/csv/raika_tweets.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            raika_tweets.append(row)
    
    for _ in range(n):
        raika_tweet_pickup = random.choice(raika_tweets)
        for tw in raika_tweet_pickup:
            backslash = False
            for i, ch in enumerate(tw):
                if backslash:
                    if ch == "n":
                        tw = tw[:i - 1] + "\n" + tw[i + 1:]
                    backslash = False
                if ch == "\\":
                    backslash = True
            if itrc:
                try:
                    await itrc.response.send_message(tw)
                except discord.InteractionResponded:
                    await itrc.channel.send(tw)
            elif ctx:
                await ctx.send(tw)