from elasticsearch import Elasticsearch
import os
import json

def categoryConverter(category):
    if category in ["Pantalón", "Leggings", "Vestuario", "Body", "Tenis Mujer", "Zapatos Mujer", "Ropa Mujer", "Ropa Interior Femenina", "Bolsos y Carteras", "Accesorios Mujer", "Maquillaje", "Ropa Deportiva Mujer", "Ropa Niñas" ]:
        return "Moda Mujer"
    elif category in ["Tenis deportes", "Accesorios Deportivos", "Camping", "Disciplinas Deportivas", "Gimnasio en Casa", "Bicicletas", ]:
        return "Deportes"
    elif category in ["Camisa","Tenis Hombre","Ropa Deportiva Hombre","Ropa Hombre","Ropa Interior Masculina","Zapatos Hombre","Cuidado personal hombre"]:
        return "Moda Hombre"
    elif category in ["Accesorios Celulares", "TV", "Computadores", "Gaming", "Smartwatch", "Fotografía", "Parlantes", "Audífonos", "Telefonía", "Wearables", "Promociones Electro"]:
        return "Electronica"
    elif category in ["Mundo Bebé", "Juguetes de Bebé", "Juguetes","Carros a Batería y Go Karts","Juegos de Exterior","Juegos de Mesa","Ropa de Cama Infantil","Dormitorio infantil","Zapatos Infantiles","Ropa Niños","Lactancia y Alimentación","Coches Para Bebes","Cuidado y Salud del Bebé","Paseo y seguridad","Sillas Infantiles","Ropa Bebé"]:
        return "Niños"
    elif category in ["Baño Crate and Barrel", "Cocina Crate and Barrel", "Decoración y Cojines", "Gourmet", "Hogar Inteligente","Electro Cocina","Electro Hogar","Neveras","Lavadoras","Cocinas","Climatización","Muebles","Muebles de Sala","Muebles de Terraza","Muebles de Comedor","Muebles para Niños","Muebles de Oficina","Ropa de cama","Colchones","Complementos de Cama","Camas","Ropa de cama Juvenil","Muebles de Dormitorio","Navidad","Cocina","Vajillas y Cubiertos","Baño","Organización del Hogar","Decoración y Cojines, Marcas Destacadas"]:
        return "Hogar"
    elif category in ["Marcas Accesorios", "Accesorios Hombre", "Relojes","Billeteras y Monederos","Gafas","Bisutería y Joyería","Perfumes","Cuidado Facial","Cuidado Capilar","Dermocosmetica","Cuidado Personal","Maletas de Viaje","Movilidad"]:
        return "Accesorios"
    elif category in ["Mundo mascotas"]:
        return "Mascotas"
    elif category in ["Música", "Instrumentos musicales"]:
        return "Musica"
    elif category in ["Escolar", "Libros"]:
        return "Libros"
    elif category in ["Tenis"]:
        return "Zapatos"
    elif category in ["Marcas Destacadas"]:
        return "Otros"
    else: return category

def localOrElasticsearch(destination, products, provider):
    if destination == "local":
        file = open("/Users/eduardoblandon/Desktop/doioBackend/data/products.json", "a")
        for product in products:
            file.write(f'{{"_source": \n{json.dumps(product)}}},\n')
    else: 
        elasticsearchClient = Elasticsearch(
            [os.environ.get("ELASTICSEARCH_HOST")], 
            scheme="http", 
            port=os.environ.get("ELASTICSEARCH_PORT")
        )
        elasticsearchClient.delete_by_query(index="products", body={"query": {"match": {"provider": provider}}})
        for product in products: elasticsearchClient.index(index="products", document=product)

 