import tkinter as tk
from tkinter import ttk
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, FOAF
import urllib.parse

# Load RDF graph
graph = Graph()
graph.parse("output17-b.ttl", format="turtle")

# Define SPARQL queries
simple_query = """
prefix schema: <https://schema.org/> 
prefix ex: <http://example.org/film#> 
prefix mov: <http://example.org/>
select ?name
where {
    ?film a schema:Movie;
          schema:title ?name .
}
LIMIT 10
"""

def findPersons(personArray = []): 
    request = """
    prefix schema: <https://schema.org/> 
    prefix ex: <http://example.org/person#> 
    prefix mov: <http://example.org/>
    select ?nom ?nomOriginal ?popularite ?adulte ?genre ?photo ?id ?profession
    where {
        ?film a schema:person;
            schema:title ?name .
    """

    if(len(personArray)>0):
        request += 'FILTER(REGEX(?name, "' + personArray[0]+'")'
        firstIgnored = False
        for title in personArray:
            if not(firstIgnored):
                firstIgnored=True
                continue
            request+= '|| STRSTARTS(?name, "' + title +'")'
        request +=")"

    request+="""
        BIND(URI(CONCAT("http://localhost/service/themoviedbapi/findPerson?Person=", ENCODE_FOR_URI(?name))) AS ?serviceURL)
        
        OPTIONAL {
            SERVICE ?serviceURL {
                ?result a ex:Film;
                    schema:name ?title;
                    ex:gender ?gender;
            }
        }
    }
    ORDER BY DESC(?popularity)
    LIMIT 10
    """
    
    return request

def findMovies(filmArray = []): 
    request = """
    prefix schema: <https://schema.org/> 
    prefix ex: <http://example.org/film#> 
    prefix mov: <http://example.org/>
    select ?name ?title ?genres ?dateSortie ?noteMoyenne ?langueOriginale
    where {
        ?film a schema:Movie;
            schema:title ?name .
    """

    if(len(filmArray)>0):
        request += 'FILTER(REGEX(?name, "' + filmArray[0]+'")'
        firstIgnored = False
        for title in filmArray:
            if not(firstIgnored):
                firstIgnored=True
                continue
            request+= '|| STRSTARTS(?name, "' + title +'")'
        request +=")"

    request+="""
        BIND(URI(CONCAT("http://localhost/service/themoviedbapi/findMovie?Movie=", ENCODE_FOR_URI(?name))) AS ?serviceURL)

        OPTIONAL {
            SERVICE ?serviceURL {
                ?result a ex:Film;
                    schema:name ?title;
                    ex:genres ?genres;
                    ex:dateSortie ?dateSortie;
                    ex:noteMoyenne ?noteMoyenne;
                    ex:langueOriginale ?langueOriginale;
                    ex:popularity ?popularity .
            }
        }
    }
    ORDER BY DESC(?popularity)
    LIMIT 10
    """
    
    return request

# Function to execute simple query and display results
def execute_simple_query():
    results = graph.query(simple_query)
    display_results(results, ["name"])

# Function to execute federated query and display results 
def execute_federated_query():
    input = userInput.get().split(",")
    print("Executing federated query")
    results = graph.query(findMovies(input))
    display_results(results, ["name", "genres", "dateSortie", "noteMoyenne", "langueOriginale"])
    print("Federated query executed")

# Function to display query results
def display_results(results, fields):
    # Clear previous results
    for widget in result_frame.winfo_children():
        widget.destroy()

    # Create table header
    header_frame = tk.Frame(result_frame)
    header_frame.pack(fill=tk.X)
    for field in fields:
        label = tk.Label(header_frame, text=field.capitalize(), anchor="w")
        label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    # Display results in table
    for row in results:
        row_frame = tk.Frame(result_frame)
        row_frame.pack(fill=tk.X)
        for field in fields:
            if field in row:
                value = row[field]
            else:
                value = row.name
            label = tk.Label(row_frame, text=str(value), anchor="w")
            label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

# Create GUI
root = tk.Tk()
root.title("Movie Query")

paramsSection = ttk.Frame(root, padding=10)

tk.Label(paramsSection, text="Input").grid(row=0 ,column=0)
userInput = tk.Entry(paramsSection)
userInput.grid(row=0 ,column=1)
simple_button = tk.Button(paramsSection, text="Persons", command=execute_simple_query).grid(row=1 ,column=0)
federated_button = tk.Button(paramsSection, text="Movies", command=execute_federated_query).grid(row=1 ,column=1)

paramsSection.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


result_frame = tk.Frame(root)

result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()