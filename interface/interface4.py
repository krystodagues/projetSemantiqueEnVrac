from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, FOAF
import tkinter as tk

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
    display_results(results, "name")

# Function to execute federated query and display results 
def execute_federated_query():
    results = graph.query(federated_query)
    display_results(results, "title")

# Function to display query results
def display_results(results, field_name):
    result_text.delete("1.0", tk.END)
    for row in results:
        if field_name in row:
            result_text.insert(tk.END, f"Movie: {row[field_name]}\n\n")
        else:
            result_text.insert(tk.END, f"Movie: {row.name}\n")
            result_text.insert(tk.END, f"Genres: {row.genres}\n")
            result_text.insert(tk.END, f"Release Date: {row.dateSortie}\n")
            result_text.insert(tk.END, f"Average Rating: {row.noteMoyenne}\n")
            result_text.insert(tk.END, f"Original Language: {row.langueOriginale}\n\n")

# Create GUI
root = tk.Tk()
root.title("Movie Query")

simple_button = tk.Button(root, text="Simple Query", command=execute_simple_query)
simple_button.pack(pady=10)

federated_button = tk.Button(root, text="Federated Query", command=execute_federated_query)
federated_button.pack(pady=10)

result_text = tk.Text(root, width=80, height=20)
result_text.pack(pady=10)

root.mainloop()