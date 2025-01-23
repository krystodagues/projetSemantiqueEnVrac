from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

# Création du graphe source
g = Graph()
g.parse("actors4.ttl", format="turtle")

# Requête CONSTRUCT avec URIs complets
construct_query = """
CONSTRUCT {
    ?movie <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Movie> ;
        <https://schema.org/name> ?movieTitle ;
        <https://schema.org/datePublished> ?date ;
        <https://schema.org/identifier> ?code ;
        <https://schema.org/rating> ?rating ;
        <https://schema.org/reviewCount> ?reviews ;
        <https://schema.org/cast> ?actor .
    
    ?actor <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Person> ;
        <https://schema.org/name> ?actorName ;
        <https://schema.org/identifier> ?actorId ;
        <https://schema.org/hasActedIn> ?movie .
}
WHERE {
    ?s <https://schema.org/Movie> ?movieTitle ;
        <https://schema.org/Date> ?date ;
        <https://schema.org/vocab/code> ?code ;
        <https://schema.org/Rating> ?rating ;
        <https://schema.org/reviewCount> ?reviews ;
        <https://schema.org/actor> ?actorName ;
        <https://schema.org/identifier> ?actorId .

    BIND(URI(CONCAT("http://example.org/movies/", REPLACE(?movieTitle, " ", "_"))) AS ?movie)
    BIND(URI(CONCAT("http://example.org/actors/", REPLACE(?actorName, " ", "_"))) AS ?actor)
}
"""

# Exécution de la requête CONSTRUCT
output_graph = g.query(construct_query)

# Sauvegarde du résultat
output_graph.serialize(destination="output5-bis.ttl", format="turtle")