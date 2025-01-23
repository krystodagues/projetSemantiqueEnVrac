from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

# Création du graphe source
g = Graph()
g.parse("actors4.ttl", format="turtle")

# Requête CONSTRUCT avec URIs complets
construct_query = """
CONSTRUCT {
    # Définition des films
    ?movie <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Movie> ;
        <https://schema.org/name> ?movieTitle ;
        <https://schema.org/datePublished> ?date ;
        <https://schema.org/identifier> ?movieCode ;
        <https://schema.org/rating> ?rating ;
        <https://schema.org/reviewCount> ?reviews ;
        <https://schema.org/cast> ?actor .

    # Définition des acteurs
    ?actor <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Person> ;
        <https://schema.org/name> ?actorName ;
        <https://schema.org/identifier> ?uniqueActorId ;
        <https://schema.org/hasActedIn> ?movie .
}
WHERE {
    # Extraire les informations des triples d'entrée
    ?s <https://schema.org/Movie> ?movieTitle ;
       <https://schema.org/Date> ?date ;
       <https://schema.org/vocab/code> ?movieCode ;
       <https://schema.org/Rating> ?rating ;
       <https://schema.org/reviewCount> ?reviews ;
       <https://schema.org/actor> ?actorName ;
       <https://schema.org/identifier> ?actorId .

    # Générer un URI unique pour chaque film basé sur le code
    BIND(URI(CONCAT("http://example.org/movies/", ?movieCode)) AS ?movie)

    # Générer un URI unique pour chaque acteur basé sur son nom
    BIND(URI(CONCAT("http://example.org/actors/", REPLACE(?actorName, " ", "_"))) AS ?actor)

    # Garder un seul identifiant unique pour chaque acteur
    {
        SELECT ?actorName (MIN(?actorId) AS ?uniqueActorId)
        WHERE {
            ?s <https://schema.org/actor> ?actorName ;
               <https://schema.org/identifier> ?actorId .
        }
        GROUP BY ?actorName
    }
}

"""



# Exécution de la requête CONSTRUCT
output_graph = g.query(construct_query)

# Sauvegarde du résultat
output_graph.serialize(destination="output13-b.ttl", format="turtle")