import tkinter as tk
from tkinter import scrolledtext
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON

# Charger le fichier RDF
rdf_file = "output17-b.ttl"
graph = Graph()
graph.parse(rdf_file, format="turtle")

def execute_sparql_query(query):


    # Exécuter la requête
    results = graph.query(query)

    # Afficher les résultats
    result_text.delete(1.0, tk.END)
    for row in results:
        result_text.insert(tk.END, f"Film: {row['title']}, Genres: {row['genres']}, Date: {row['dateSortie']}, Note: {row['noteMoyenne']}, Langue: {row['langueOriginale']}\n")

def clear_results():
    result_text.delete(1.0, tk.END)

# Interface utilisateur
window = tk.Tk()
window.title("SPARQL Query Interface")

# Boutons
query_button = tk.Button(window, text="Exécuter la requête SPARQL", command=execute_sparql_query("""
    prefix schema: <https://schema.org/>
    prefix ex: <http://example.org/film#>
    prefix mov: <http://example.org/>
    select *
    where {
        ?film a schema:Movie;
               schema:title ?name .

        BIND(ENCODE_FOR_URI(?name) AS ?encodedName)

        BIND(URI(CONCAT("http://localhost/service/themoviedbapi/findMovie?Movie=", ?encodedName)) AS ?serviceURL)

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
    """))
query_button.pack(pady=10)

query_button2 = tk.Button(window, text="Exécuter la requête SPARQL", command=execute_sparql_query("""
    prefix schema: <https://schema.org/>
    prefix ex: <http://example.org/film#>
    prefix mov: <http://example.org/>
    select *
    where {
        ?film a schema:Movie;
               schema:title ?name .
    }
    LIMIT 10
    """))
query_button.pack(pady=10)


clear_button = tk.Button(window, text="Effacer les résultats", command=clear_results)
clear_button.pack(pady=10)

# Zone de texte pour afficher les résultats
result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
result_text.pack(pady=10)

window.mainloop()
