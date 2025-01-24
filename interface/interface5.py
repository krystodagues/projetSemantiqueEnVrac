from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, FOAF
import tkinter as tk
from tkinter import ttk

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
LIMIT 100
"""

federated_query = """
prefix schema: <https://schema.org/> 
prefix ex: <http://example.org/film#> 
prefix mov: <http://example.org/>
select ?name ?genres ?dateSortie ?noteMoyenne ?langueOriginale
where {
    ?film a schema:Movie;
           schema:title ?name .
    
    BIND(URI(CONCAT("http://localhost/service/themoviedbapi/findMovie?Movie=", ?name)) AS ?serviceURL)
    
    SERVICE ?serviceURL {
        ?result a ex:Film;
                schema:name ?title;
                ex:genres ?genres;
                ex:dateSortie ?dateSortie;
                ex:noteMoyenne ?noteMoyenne;
                ex:langueOriginale ?langueOriginale.
    }
}
LIMIT 10
"""

# Function to execute simple query and display results
def execute_simple_query():
    results = graph.query(simple_query)
    display_results(results, ["name"])

# Function to execute federated query and display results 
def execute_federated_query():
    results = graph.query(federated_query)
    display_results(results, ["name", "genres", "dateSortie", "noteMoyenne", "langueOriginale"])

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

simple_button = tk.Button(root, text="Simple Query", command=execute_simple_query)
simple_button.pack(pady=10)

federated_button = tk.Button(root, text="Federated Query", command=execute_federated_query)
federated_button.pack(pady=10)

result_frame = tk.Frame(root)
result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()