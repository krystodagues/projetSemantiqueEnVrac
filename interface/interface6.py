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
            schema:title ?nom .
    """

    if(len(personArray)>0):
        request += 'FILTER(REGEX(?nom, "' + personArray[0]+'")'
        firstIgnored = False
        for title in personArray:
            if not(firstIgnored):
                firstIgnored=True
                continue
            request+= '|| REGEX(?nom, "' + title +'")'
        request +=")"

    request+="""
        BIND(URI(CONCAT("http://localhost/service/themoviedbapi/findPerson?Person=", ENCODE_FOR_URI(?nom))) AS ?serviceURL)
        
        OPTIONAL {
            SERVICE ?serviceURL {
                ?result a ex:Film;
                    ex:id ?id;
                    ex:genre ?genre;
                    ex:photo ?photo;
                    ex:adulte ?adulte;
                    ex:popularite ?popularite;
                    ex:profession ?profession;
                    ex:nomOriginal ?nomOriginal .
            }
        }
    }
    ORDER BY DESC(?popularity)
    LIMIT 10
    """
    print(request)
    return request
    
def findMovies(filmArray = []): 
    request = """
    prefix schema: <https://schema.org/> 
    prefix ex: <http://example.org/film#> 
    prefix mov: <http://example.org/>
    select ?name ?identifier ?publishDate ?dateSortie ?langueOriginale ?popularite
    where {
    ?film a schema:Movie;
            schema:title ?name ;
            schema:identifier ?identifier;
            schema:datePublished ?publishDate.
    
    """
    
    if(len(filmArray)>0):
        request += 'FILTER(REGEX(?name, "' + filmArray[0]+'")'
        firstIgnored = False
        for title in filmArray:
            if not(firstIgnored):
                firstIgnored=True
                continue
            request+= '|| REGEX(?name, "' + title +'")'
        request +=")"

    request+="""
        BIND(URI(CONCAT("http://localhost/service/themoviedbapi/findMovie?Movie=", ENCODE_FOR_URI(?name))) AS ?serviceURL)

        OPTIONAL {
            SERVICE ?serviceURL {
                ?result a ex:filmReport;
                    ex:dateSortie ?dateSortie;
                    ex:langueOriginale ?langueOriginale;
                    ex:popularite ?popularityRaw .
	                BIND(xsd:decimal(?popularityRaw) AS ?popularite)
            }
        }
    """
    request += """
    }
    ORDER BY DESC(?popularite)
    LIMIT 10
    """
    print(request)
    return request

# Function to execute simple query and display results
def execute_simple_query():
    input = userInput.get().split(",")
    print("Executing federated query")
    results = graph.query(findPersons(input))
    display_results(results, ["nom" ,"nomOriginal" ,"popularite" ,"adulte" ,"genre" ,"photo" ,"id" ,"profession"])
    print("Federated query executed")

# Function to execute federated query and display results 
def execute_federated_query():
    input = userInput.get().split(",")
    print("Executing federated query")
    results = graph.query(findMovies(input))
    print(list(graph.namespaces()))
    display_results(results, ["name","identifier","publishDate","dateSortie","langueOriginale","popularite"])
    print("Federated query executed")

# Function to display query results
def display_results(results, fields):
    # Clear previous results
    for widget in result_frame.winfo_children():
        widget.destroy()

    # Create table header
    for i, field in enumerate(fields):
        result_frame.grid_columnconfigure(i, weight=1)
        result_frame.grid_columnconfigure(i, minsize=150)  # Set minimum column width
        label = tk.Label(result_frame, text=field.capitalize(), anchor="w", bg="lightgray", padx=5, pady=5)
        label.grid(row=0, column=i, sticky="nsew")  # Use grid for the header

    # Display results in table
    for row_idx, row in enumerate(results, start=1):
        for col_idx, field in enumerate(fields):
            print(row)
            value = row[col_idx] if col_idx < len(row) and row[col_idx] is not None else "Not Found"
            label = tk.Label(result_frame, text=value, anchor="w", padx=5, pady=5)
            label.grid(row=row_idx, column=col_idx, sticky="nsew")  # Use grid for rows

# Create GUI
root = tk.Tk()
root.title("Movie Query")

params_section = ttk.Frame(root, padding=10)

# Input field and buttons
tk.Label(params_section, text="Input").grid(row=0, column=0)
userInput = tk.Entry(params_section)
userInput.grid(row=0, column=1)
simple_button = tk.Button(params_section, text="Persons", command=execute_simple_query).grid(row=1, column=0)
federated_button = tk.Button(params_section, text="Movies", command=execute_federated_query).grid(row=1, column=1)

params_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Result frame
result_frame = tk.Frame(root)
result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Display initial results

root.mainloop()