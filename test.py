import database

def main():
    db = database.DB()
    data = db.getUser("jacy@gmail.com")

    print(data.get(0))
    print(data["name"])

if __name__ == "__main__":
    main()