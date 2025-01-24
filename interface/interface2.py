import tkinter as tk
from tkinter import ttk, scrolledtext
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, FOAF

class SparqlQueryApp:
    def __init__(self, master):
        self.master = master
        master.title("SPARQL Movie Query App")
        master.geometry("800x600")

        # Load RDF graph
        self.graph = Graph()
        self.graph.parse("output17-b.ttl", format="turtle")

        # Create movie buttons dynamically
        self.create_movie_buttons()

        # Result display area
        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20)
        self.result_text.pack(padx=10, pady=10)

    def create_movie_buttons(self):
        # Query to get unique movie titles
        query = """
        PREFIX schema: <https://schema.org/>
        SELECT DISTINCT ?title 
        WHERE { 
            ?film a schema:Movie; 
                  schema:title ?title 
        }
        """
        
        results = self.graph.query(query)
        
        # Frame for buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(padx=10, pady=10)

        for row in results:
            title = str(row.title)
            btn = tk.Button(button_frame, text=title, 
                            command=lambda t=title: self.execute_movie_query(t))
            btn.pack(side=tk.LEFT, padx=5)

    def execute_movie_query(self, movie_title):
        query = f"""
        PREFIX schema: <https://schema.org/> 
        PREFIX ex: <http://example.org/film#> 
        PREFIX mov: <http://example.org/> 
        SELECT * 
        WHERE {{ 
            ?film a schema:Movie; 
                  schema:title "{movie_title}" . 
            BIND(URI(CONCAT("http://localhost/service/themoviedbapi/findMovie?Movie={movie_title}")) AS ?serviceURL)
            SERVICE ?serviceURL {{ 
                ?result a ex:Film; 
                        schema:name ?title; 
                        ex:genres ?genres; 
                        ex:dateSortie ?dateSortie; 
                        ex:noteMoyenne ?noteMoyenne; 
                        ex:langueOriginale ?langueOriginale. 
            }} 
        }}
        """
        
        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        
        try:
            results = self.graph.query(query)
            
            for row in results:
                result_str = f"""
Film: {row.title}
Genres: {row.genres}
Release Date: {row.dateSortie}
Average Rating: {row.noteMoyenne}
Original Language: {row.langueOriginale}
                """
                self.result_text.insert(tk.END, result_str + "\n\n")
        
        except Exception as e:
            self.result_text.insert(tk.END, f"Error executing query: {str(e)}")

def main():
    root = tk.Tk()
    app = SparqlQueryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()