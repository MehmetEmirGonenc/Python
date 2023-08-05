import sqlite3
 
def main():
    con = sqlite3.connect("imdb.db")
    cur = con.cursor()

    
    #Main Loop
    while (True):
        #Main menu
        print("#############################  MAIN MENU  ##################################")
        print("#    1-) LIST of Movies/Series")
        print("#    2-) Browse on LIST")
        print("#    3-) LIST of Actors")
        print("#    4-) LIST of Directors")
        print("#    5-) LIST of Others")
        print("#    0-) EXİT")
        choice = input(">>>")
        if choice == "1":
            List_Mov(cur)
        elif choice == "2":
            Browse(cur)
            



# List movies function
def List_Mov(cur):
    page = 0
    #Main Loop
    while (True):
        page += 1
        place_holder = [(((page - 1)*100) + 1), (page*100)]
        res = cur.execute("SELECT * FROM (SELECT ROW_NUMBER() OVER(ORDER BY ratings.rating * ratings.votes DESC) as id, titles.title_id,primary_title,premiered,ended,type,runtime_minutes,genres,ratings.rating,ratings.votes FROM titles INNER JOIN ratings ON titles.title_id = ratings.title_id) WHERE id BETWEEN ? AND ?;", place_holder)
        values = res.fetchall()

        for row in values:
            print(f"+----------------------------- ( {row[0]} ) -------------------------------------------+")
            print(f"| Name : {row[2]}          {row[3]}/{row[4]}")
            print(f"| Type : {row[5]}          {row[6]}min        Genres : {row[7]}")
            print("+---------------------------------------------------------------------------------------+")
        print(f"\n                                   <{page}>")    
        while (True):
            print("\nN - > Next Page")
            print("P - > Previous Page")
            print("<movie id> - > Detailed information about movie")
            print("E - > Exit")
            choice = input(">>>")
            if choice.upper() == "N" :
                break
            elif choice.upper() == "E":
                return
            elif choice.upper() == "P":
                if page <= 1:
                    page -= 1
                else:
                    page -= 2
                break 
            else:
                if choice.isalpha() == False:
                    for row in values:
                        if (choice == str(row[0])):
                            detail_values = Call_Crew(cur, [row[1]])
                            #Print informations about movie
                            print(f"******************** {row[2]} ********************")
                            print(f"*Votes : {row[9]}              Rating : {row[8]}")
                            print(f"* Type : {row[5]}       {row[3]} / {row[4]}        {row[6]}min")
                            print(f"*Genres : {row[7]}")
                            print("*\n*  /  -  CREW  - /\n*")
                            for crew in detail_values:
                                print(f"*-> {crew[1]} --> {crew[0]}")
                            print(f"*********************************************************")
                else:
                    print("Unexpected input!")


#Browsing
def Browse(cur):
    page = 0
    #Main loop
    while(True):
        page += 1
        print("########################## Movie Browser ##########################")
        print("Plese enter name of movie")
        movie_name = input(">>>")
        args = [movie_name, ((page-1) * 50), (page * 50)]
        browse = cur.execute("SELECT id, title_id, type, primary_title, premiered, ended, runtime_minutes, genres, rating, votes FROM (SELECT ROW_NUMBER() OVER(ORDER BY ratings.rating * ratings.votes DESC) as id, * FROM titles INNER JOIN ratings ON titles.title_id = ratings.title_id WHERE primary_title LIKE '%?%') WHERE id BETWEEN ? AND ?;",args)
        resaults = browse.fetchall()
        for row in resaults:
            print(f"+----------------------------- ( {row[0]} ) -------------------------------------------+")
            print(f"| Name : {row[3]}          {row[4]}/{row[5]}")
            print(f"| Type : {row[2]}          {row[6]}min        Genres : {row[7]}")
            print("+---------------------------------------------------------------------------------------+")
        print(f"\n                                   <{page}>")    


#Call crew details
def Call_Crew(cur, title_id):
    #Get crew information with sql query
    detail_res = cur.execute("SELECT category, people.name FROM crew INNER JOIN people ON crew.person_id = people.person_id WHERE crew.title_id = ? ORDER BY CASE WHEN category = 'director' THEN 1 WHEN category = 'writer' THEN 2 WHEN category = 'actor' THEN 3 ELSE 4 END ASC;", title_id)
    return detail_res.fetchall()


main()