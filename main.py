import pandas
import server as srv

read_books = []

df = pandas.read_csv('read_books', sep=',')
data = df.values
for row in data:
    read_books.append(row[0])

srv.get_recommendations(read_books)
