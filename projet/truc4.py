from rdflib import Graph, Namespace

# Charger le fichier RDF existant
input_file = "actors4.ttl"
output_file = "output.ttl"

g = Graph()
g.parse(input_file, format="turtle")

# Construire la requête CONSTRUCT sans utiliser de préfixes
construct_query = """
CONSTRUCT {
  ?movie <https://schema.org/Movie> ?movieName ;
        <https://schema.org/datePublished> ?date ;
        <https://schema.org/identifier> ?code ;
        <https://schema.org/reviewCount> ?reviewCount ;
        <https://schema.org/ratingValue> ?rating .

  ?actor <https://schema.org/Person> ?actorName ;
         <https://schema.org/identifier> ?actorID .
}
WHERE {
  ?s <https://schema.org/actor> ?actorName ;
     <https://schema.org/identifier> ?actorID ;
     <https://schema.org/Movie> ?movieName ;
     <https://schema.org/Date> ?date ;
     <https://schema.org/reviewCount> ?reviewCount ;
     <https://schema.org/Rating> ?rating ;
     <https://schema.org/vocab/code> ?code .
}
"""

# Exécuter la requête CONSTRUCT
try:
    output_graph = g.query(construct_query)

    # Créer un nouveau graphe pour le résultat
    result_graph = Graph()

    for triple in output_graph:
        result_graph.add(triple)

    # Sauvegarder le graphe résultant dans un fichier Turtle
    result_graph.serialize(destination=output_file, format="turtle")
    print(f"Fichier '{output_file}' créé avec succès.")
except Exception as e:
    print(f"Erreur lors de l'exécution de la requête : {e}")
