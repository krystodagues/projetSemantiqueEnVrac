from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, FOAF
import tkinter as tk

# Load RDF graph
graph = Graph()
graph.parse("output17-b.ttl", format="turtle")

# Define SPARQL query
query = """
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

# Function to execute query and display results
def execute_query():
    results = graph.query(query)

    result_text.delete("1.0", tk.END)
    for row in results:
        result_text.insert(tk.END, f"Movie: {row.name}\n")
        result_text.insert(tk.END, f"Genres: {row.genres}\n")
        result_text.insert(tk.END, f"Release Date: {row.dateSortie}\n")
        result_text.insert(tk.END, f"Average Rating: {row.noteMoyenne}\n")
        result_text.insert(tk.END, f"Original Language: {row.langueOriginale}\n\n")

# Create GUI
root = tk.Tk()
root.title("Movie Query")

query_button = tk.Button(root, text="Execute Query", command=execute_query)
query_button.pack(pady=10)

result_text = tk.Text(root, width=80, height=20)
result_text.pack(pady=10)

root.mainloop()