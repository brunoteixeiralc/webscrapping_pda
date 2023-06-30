from enum import Enum

class Product(Enum):
    CERVEJA_ARTESANAL = "semanacompleta_cervejasespeciais"
    DESTILADOS = "semanacompleta_destilados"
    VINHOS = "semanacompleta_vinhosbf"
    ENERGETICOS = "semanacompleta_energetico"
    FRALDAS = "semanacompleta_fraldas"
    
class Product_BETA(Enum):
    CERVEJA_ARTESANAL = "hs_cervejasespeciais"
    DESTILADOS = "hs_destilados"
    WHISKIES = "hs_whiskies"
    VINHOS = "hs_vinhos_tintos"
    ENERGETICOS = "hs_energeticos"
    FRALDAS = "hs_fraldas"
    
class FileName(Enum):
    CERVEJA_ARTESANAL = "descontos_cervejas_artesanais"
    DESTILADOS = "descontos_destilados"
    WHISKIES = "descontos_whiskies"
    VINHOS = "descontos_vinhos_artesanais"
    ENERGETICOS = "descontos_energeticos_artesanais"
    FRALDAS = "descontos_fraldas_artesanais"
    
class EmailBody(Enum):
    CERVEJA_ARTESANAL = "Cervejas Artesanais"
    DESTILADOS = "Destilados"
    WHISKIES = "Whiskies"
    VINHOS = "Vinhos"
    ENERGETICOS = "Energéticos"
    FRALDAS = "Fraldas"