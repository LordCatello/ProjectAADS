Readme lista

Modified incident_edges method in graph class to return a list of the incident edges in a vertex, instead of an iterator generator.

Probabilmente non è l'implementazione migliore, perché in pratica prendere gli incident edges ogni volta richiede O(deg(nodo)), visto che la nostra implementazione usa adjacency map, e, nel caso peggiore, questa cosa la faccio un numero di volte pari al grado del nodo, e lo faccio per ogni nodo del grafo, quindi faccio n volte una roba che è O(deg^2)

<a href = 'https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects'>Oggetto restituito da dictionary.values()</a>. E' iterabile ma non indicizzabile, pertano devo trasformarlo in lista prima di restituirlo, e questo non so quanto tempo richiede.