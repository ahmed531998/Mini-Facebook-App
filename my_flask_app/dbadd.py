import psycopg2,csv,time,datetime, re
from collections import Counter

def addUser(cur):
    filename='prj_user_cleaned.csv'
    cur.execute("CREATE TABLE users (userID bigint PRIMARY KEY, name text, screenName text, location text, description text, verified bool, income bigint , age bigint, hobby text);")

    fdr=open(filename,newline='',mode='r',encoding='utf-8')
    reader=csv.reader(fdr,delimiter=';',quotechar=";")
    firstrow=True

    count=0
    for row in reader:
        if firstrow:
            firstrow=False
            continue
        name, screenName, location, description,=row[1],row[2],row[3],row[4]   #Strings
        verified=row[5]=='True' #Bools
        userID, income, age, hobby = int(row[0]),0,0,"None"  #Int
        cur.execute("INSERT INTO users (userID, name, screenName, location, description, verified, income, age, hobby) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(userID, name, screenName, location, description, verified, income, age, hobby))
        count+=1
    fdr.close()
    return("Added {0} rows to user".format(count))

def addTweet(cur):
    filename='prj_tweet_cleaned.csv'
    cur.execute("CREATE TABLE post (postID bigint PRIMARY KEY, userID bigint, createdAt timestamp, message text);")

    fdr=open(filename,newline='',mode='r',encoding='utf-8')
    reader=csv.reader(fdr,delimiter=';',quotechar=";")
    firstrow=True

    count=0
    for row in reader:
        if firstrow:
            firstrow=False
            continue
        postID, userID = int(row[0]), int(row[1])   #int
        createdAt, message = row[2], row[3]     #string
        cur.execute("INSERT INTO post (postID, userID, createdAt, message) VALUES (%s, %s, %s, %s);",(postID, userID, createdAt, message))
        count+=1
    fdr.close()
    return("Added {0} rows to post".format(count))

def addFollowing(cur):
    filename='prj_following_cleaned.csv'
    cur.execute("CREATE TABLE following (userID bigint, followerID bigint, PRIMARY KEY(userID, followerID));")

    fdr=open(filename,newline='',mode='r',encoding='utf-8')
    reader=csv.reader(fdr,delimiter=';',quotechar=";")
    firstrow=True

    count=0
    for row in reader:
        if firstrow:
            firstrow=False
            continue
        userID, followerID = int(row[0]), int(row[1])   #int
        cur.execute("INSERT INTO following (userID, followerID) VALUES (%s, %s);",(userID, followerID))
        count+=1
    fdr.close()
    return("Added {0} rows to following".format(count))

def findRetweets(tweets):
    retweets = []
    for tweet in tweets:
        x = re.findall("\ART @", tweet[0])
        if (x):
            retweets.append(tweet)

    screenNames = []
    for retweet in retweets:
        m = re.search('@(.+?):', retweet[0])
        if m:
            screenNames.append(m.group(1))
    return screenNames

def removeDuplicates(x):
    unique = []
    for el in x:
        if el not in unique:
            unique.append(el)
    return unique


def addRelation(cur):
    cur.execute("SELECT userid FROM users")
    userIDS = cur.fetchall()
    for ID in userIDS:
        cur.execute("SELECT message FROM post WHERE userid= %s", (ID,))
        tweets = cur.fetchall()
        cur.execute("SELECT screenname From users WHERE userid= %s", (ID, ))
        userScreenName = cur.fetchall()
        #print(userScreenName[0][0])
        candidateScreenNames = findRetweets(tweets)

        
        dictA = {}
        for el in candidateScreenNames:
            if el not in dictA:
                dictA[el] = 1
            else:
                dictA[el] += 1
        #print(dictA)
        single = True

        for key in dictA:
            cur.execute("SELECT userid From users WHERE screenname= %s", (key,))
            retweetedUsers = cur.fetchall()
           # print("retweeted users: \n")
            #print(retweetedUsers)
            #print("end retweeted users: \n")
            for user in retweetedUsers:
                count = 0
                notRelated = True
                cur.execute("SELECT message FROM post WHERE userid= %s", (user,))
                retweetedBack = cur.fetchall()
                retweetedBackScreenNames = findRetweets(retweetedBack)
                #print("retweeted back users: \n")
                #print(retweetedBackScreenNames)
                #print("end retweetedback users: \n")
                for retweetedBackScreenName in retweetedBackScreenNames:
                    if (retweetedBackScreenName == userScreenName[0][0]):
                        notRelated = False
                        count+=1                     
                if (not notRelated and user != ID):
                    single = False
                    if (min(count, dictA[key]) == 1):
                        cur.execute("INSERT INTO isrelated (userID, relatedUserID, type) VALUES (%s, %s, %s);",(ID, user, "date"))
                    if (min(count, dictA[key]) > 1):
                        cur.execute("INSERT INTO isrelated (userID, relatedUserID, type) VALUES (%s, %s, %s);",(ID, user, "marriage"))
            
        if (single):
            cur.execute("INSERT INTO isrelated (userID, relatedUserID, type) VALUES (%s, %s, %s);",(ID, ID, "single"))

                
                
        
            
    
#def add

def updateUserAge(cur):
    cur.execute("SELECT userid FROM users")
    userIDS = cur.fetchall()
    for ID in userIDS:
        cur.execute("SELECT createdat FROM post WHERE userid= %s", (ID,))
        tweetDates = cur.fetchall()

        update_command = "UPDATE users set age= %s WHERE userid= %s"
        if (len(tweetDates) == 0):
            cur.execute(update_command, (0, ID,))
        else:
            minTweet = min(tweetDates)
            maxTweet = max(tweetDates)
            oldTime = minTweet[0]
            newTime = maxTweet[0]
            userAge = newTime - oldTime
            cur.execute(update_command, (userAge.days, ID,))
        
        
def updateUserIncome(cur):
    cur.execute("SELECT userid FROM users")
    userIDS = cur.fetchall()
    for ID in userIDS:
        cur.execute("SELECT * FROM post WHERE userid= %s", (ID,))
        tweets = cur.fetchall()
        print(tweets)
        update_command = "UPDATE users set income= %s WHERE userid= %s"
        cur.execute(update_command, (len(tweets), ID,))


def extractHashtags(userTweets):
    hashtags = {}
    for tweet in userTweets:
        for word in tweet[0].split():
            if (word.startswith("#")):
                x = word[1:]
                if (x in hashtags):
                    hashtags[x] += 1
                else:
                    hashtags[x] = 1
    return hashtags

def getMostTweetedHashtags(hashtags):
    counting = Counter(hashtags)
    mostCommonTwo = {}
    if (len(hashtags) >= 2): 
        mostCommonTwo = counting.most_common(2)
    elif (len(hashtags) == 1):
        mostCommonTwo = counting.most_common(1)
    else:
        mostCommonTwo = [('None', 0)]

    hobbies = []
    for key in mostCommonTwo:
        hobbies.append(key[0])
    return hobbies
        
    

def findUserHashtags(cur):
    cur.execute("SELECT userid FROM users")
    userIDS = cur.fetchall()
    for ID in userIDS:
        cur.execute("SELECT message FROM post WHERE userid= %s", (ID,))
        tweets = cur.fetchall()
        hashtags = extractHashtags(tweets)
        hobbies = getMostTweetedHashtags(hashtags)
        userHobbies = ",".join(hobbies)
        update_command = "UPDATE users set hobby= %s WHERE userid= %s"
        cur.execute(update_command, (userHobbies, ID,))
    

#def updateUserHobby(cur):
    

def main():
    conn = psycopg2.connect("dbname=test user=ahmed host=localhost password=123456")
    cursor=conn.cursor()

    #The empty tables
   # cursor.execute("CREATE TABLE createtweet (postID bigint PRIMARY KEY, userID bigint);")
    #cursor.execute("CREATE TABLE isrelated (userID bigint, relatedUserID bigint, type text,PRIMARY KEY(userID, relatedUserID));")
    #cursor.execute("CREATE TABLE likes (postID bigint PRIMARY KEY, userID bigint);")

    #print(addUser(cursor))
    #print(addTweet(cursor))
    #print(addFollowing(cursor))
    #updateUserAge(cursor)
    #updateUserIncome(cursor)

    #cursor.execute("SELECT name FROM users WHERE screenname=%s", ("FafaGroundhog", ))
    #usernames = cursor.fetchall()
    #print(usernames)

    #addRelation(cursor)
    findUserHashtags(cursor)
    conn.commit()
    cursor.close()
    conn.close()

main()
