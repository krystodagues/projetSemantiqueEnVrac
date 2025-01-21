from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

# Création des namespaces
SCHEMA = Namespace("https://schema.org/")
EX = Namespace("http://example.org/")

# Création du graphe source
g = Graph()
g.parse("actors4.ttl", format="turtle")

# Création du graphe de destination
output_graph = Graph()

# Lecture du fichier CONSTRUCT SPARQL
construct_query = """
CONSTRUCT {
    # Définition des films
    ?movie a schema:Movie ;
        schema:name ?movieTitle ;
        schema:datePublished ?date ;
        schema:identifier ?movieId ;
        schema:aggregateRating [
            a schema:AggregateRating ;
            schema:ratingValue ?rating ;
            schema:reviewCount ?reviews
        ] .

    # Définition des acteurs
    ?actor a schema:Person ;
        schema:name ?actorName ;
        schema:identifier ?actorId ;
        schema:performerIn ?movie .
}
WHERE {
    ?s schema:Movie ?movieTitle ;
        schema:Date ?date ;
        schema:vocab/code ?movieId ;
        schema:Rating ?rating ;
        schema:reviewCount ?reviews ;
        schema:actor ?actorName ;
        schema:identifier ?actorId .

    BIND(IRI(CONCAT("http://example.org/movies/", ?movieId)) AS ?movie)
    BIND(IRI(CONCAT("http://example.org/actors/", ?actorId)) AS ?actor)
}
"""

# Exécution de la requête CONSTRUCT
output_graph = g.query(construct_query)

# Bind des préfixes pour un fichier plus lisible
output_graph.bind("schema", SCHEMA)
output_graph.bind("ex", EX)

# Sauvegarde du résultat
output_graph.serialize(destination="output.ttl", format="turtle")