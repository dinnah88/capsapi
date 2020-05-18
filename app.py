import flask
import pandas as pd
import requests
import gunicorn
import sqlite3

from flask import Flask, request 
app = Flask(__name__) 

@app.route('/sales')
def sales():
    conn = sqlite3.connect("data/chinook.db")
    data = pd.read_sql_query("""SELECT invoices.InvoiceDate, 
                                invoices.BillingCountry as Country, 
                                invoice_items.Quantity, 
                                invoice_items.UnitPrice,
                                tracks.AlbumId as Album, 
                                tracks.Name as tracks_name, 
                                genres.Name as genre 
                                FROM invoice_items 
                                LEFT JOIN invoices 
                                ON invoices.InvoiceId = invoice_items.InvoiceId 
                                LEFT JOIN tracks 
                                ON tracks.TrackId = invoice_items.TrackId 
                                LEFT JOIN genres 
                                ON tracks.GenreId = genres.GenreId 
                                """, 
                              conn, parse_dates = 'InvoiceDate')
    data['year'] = data["InvoiceDate"].dt.year
    yearly_sales = pd.pivot_table(data= data,
                        index= ['year','Country'],
                        values= 'UnitPrice',
                        aggfunc= 'sum' 
                      ).reset_index().groupby(['year','Country']).UnitPrice.sum()
    sales = pd.DataFrame(yearly_sales).reset_index()
    return (sales.to_json())

@app.route('/country')
def country():
    conn = sqlite3.connect("data/chinook.db")
    data = pd.read_sql_query("""SELECT invoices.InvoiceDate, 
                                invoices.BillingCountry as Country, 
                                invoice_items.Quantity, 
                                invoice_items.UnitPrice,
                                tracks.AlbumId as Album, 
                                tracks.Name as tracks_name, 
                                genres.Name as genre 
                                FROM invoice_items 
                                LEFT JOIN invoices 
                                ON invoices.InvoiceId = invoice_items.InvoiceId 
                                LEFT JOIN tracks 
                                ON tracks.TrackId = invoice_items.TrackId 
                                LEFT JOIN genres 
                                ON tracks.GenreId = genres.GenreId 
                                """, 
                              conn, parse_dates = 'InvoiceDate')
    data['year'] = data["InvoiceDate"].dt.year
    country_genre = data.groupby(['year','Country','genre']).UnitPrice.sum().dropna().reset_index()


    return (pd.DataFrame(country_genre).to_json())

@app.route('/data/get/<genre>', methods=['GET']) 
def get_data(genre): 
    conn = sqlite3.connect("data/chinook.db")
    data = pd.read_sql_query("""SELECT invoices.InvoiceDate, 
                                invoices.BillingCountry as Country, 
                                invoice_items.Quantity, 
                                invoice_items.UnitPrice,
                                tracks.AlbumId as Album, 
                                tracks.Name as tracks_name, 
                                genres.Name as genre 
                                FROM invoice_items 
                                LEFT JOIN invoices 
                                ON invoices.InvoiceId = invoice_items.InvoiceId 
                                LEFT JOIN tracks 
                                ON tracks.TrackId = invoice_items.TrackId 
                                LEFT JOIN genres 
                                ON tracks.GenreId = genres.GenreId 
                                """, 
                              conn, parse_dates = 'InvoiceDate')
    
    data['genre'] = data['genre'].astype('category')
    most_genre = pd.pivot_table(data= data,
                        index= 'genre',
                        columns= 'Country',
                        values= 'Quantity',
                        aggfunc= sum 
                      )
    genre_country = most_genre.reset_index().melt(id_vars='genre',value_name='Total_Qty').dropna()
    cond = genre_country['genre']==str(genre)
    
    return (genre_country[cond].to_json())

@app.route("/docs")
def documentation():
    return '''
        <h1> Documentation </h1>
        <h4> This API created as a submission for Capstone Project Algoritma P4DA Course. The API itself use `chinook` dataset and I did some data wrangling for each of some endpoints so any user can see what returning to each endpoint as the following: </h4>
        <h2> Static Endpoints </h2>
        <ol>
            <li>
                <p> /sales , method = GET </p>
                <p> Returning Annual Sales for each Country ordered by Country Name. </p>
            </li>
            <li>
                <p> /country , method = GET </p>
                <p> Returning List of Country, Genre, and Total Sales based on Year. </p>
            </li>
        </ol>
         
        <h2> Dynamic Endpoints </h2>
        <ol> 
            <li>
                <p> /data/get/&lt;genre&gt; , method = GET </p>
                <p> Return Quantity of &lt;genre&gt; based on each Country. </p>
            </li>

        </ol>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5000)