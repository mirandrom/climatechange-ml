import sqlite3
# we can convert from json (which I think the output is in) to sqllite here 

# assuming data is in format 
# NAME TOPIC ABSTRACT AUTHORS WHATEVER
# ???   ???    ???      ???      ???

# TODO change to actual table
def connect_db():
    con = sqlite3.connect('767db.db') 
    cur = con.cursor()
    return cur, con

# TODO add trending
def trending(cur):
    return "Placeholder\nPlaceholder 2\nPlaceholder 3" 

def main():
    cur, con = connect_db()
    while True:
        print("Welcome to the Living Litreview! Here are some trending topics:")
        print(trending(cur))
        info = input("To see more information on trending topics, type TRENDING. To search, type SEARCH. \n")
        if info == "SEARCH":
            search_info = input("Would you like to search a topic or a paper? If a topic, type TOPIC. If a paper, type PAPER. \n")
            if search_info == "TOPIC":
                topic = input("Enter your topic. \n")
                get_info_topic(cur, topic)
            
            if search_info == "PAPER":
                name = input("Enter the name of the paper. \n")
                get_info_name(cur, name)


        if info == "TRENDING":
            topic = input("Type in the topic you would like to search. \n")
            get_info_topic(cur, topic)

# TODO Change to have a preferred search order
def get_info_topic(cur, topic):
    print("Results for search on topic " + topic)
    counter = 0
    for row in cur.execute('SELECT * FROM tbl WHERE topic=?', (topic,)):
        print("Title: " + row[0] +"\nAuthor: " + row[2] + "\n")
        counter += 1
    
    print("Your search for the topic " + topic + " returned " + str(counter) + " results.")

def get_info_name(cur, name):
    cur.execute('SELECT topic FROM tbl WHERE name=?', (name,))
    topic_searched = cur.fetchone()
    get_info_topic(cur, topic_searched)

if __name__ == "__main__":
    main()