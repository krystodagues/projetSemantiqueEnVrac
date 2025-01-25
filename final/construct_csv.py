from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

# Création du graphe source
g = Graph()
g.parse("actors_tmp.ttl", format="turtle")

# Requête CONSTRUCT avec URIs complets

construct_query = construct_query = """
CONSTRUCT {
    ?movie <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Movie> ;
        <https://schema.org/title> ?movieTitle ;
        <https://schema.org/datePublished> ?date ;
        <https://schema.org/identifier> ?movieCode ;
        <https://schema.org/rating> ?rating ;
        <https://schema.org/reviewCount> ?reviews ;
        <https://schema.org/cast> ?actor .

    ?actor <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/actor> ;
        <https://schema.org/name> ?actorName ;
        <https://schema.org/identifier> ?uniqueActorId ;
        <https://schema.org/hasActedIn> ?movie .
}
WHERE {
    {
        SELECT ?actorName (MIN(?actorId) AS ?uniqueActorId)
        WHERE {
            ?s <https://schema.org/actor> ?actorName ;
               <https://schema.org/identifier> ?actorId .
        }
        GROUP BY ?actorName
    }

    ?s <https://schema.org/actor> ?actorName ;
       <https://schema.org/identifier> ?uniqueActorId ;
       <https://schema.org/Movie> ?movieTitle ;
       <https://schema.org/Date> ?date ;
       <https://schema.org/vocab/code> ?movieCode ;
       <https://schema.org/Rating> ?rating ;
       <https://schema.org/reviewCount> ?reviews .

    # Générer un URI unique basé sur le titre du film
    BIND(URI(CONCAT("http://example.org/movie/", REPLACE(?movieTitle, " ", "_"))) AS ?movie)

    # Générer un URI unique pour chaque acteur basé sur son nom
    BIND(URI(CONCAT("http://example.org/actor/", REPLACE(?actorName, " ", "_"))) AS ?actor)
}
"""


# Exécution de la requête CONSTRUCT
output_graph = g.query(construct_query)

# Sauvegarde du résultat
output_graph.serialize(destination="film_csv.ttl", format="turtle")