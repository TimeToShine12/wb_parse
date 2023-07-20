from pydantic import BaseModel, model_validator

class Item(BaseModel):
    id: int
    name: str
    salePriceU: float
    brand: str
    sale: int
    rating: int
    volume: int

    @model_validator(mode='before')
    def convert_sale_price_u(cls, values: dict):
        sale_price = values.get('salePriceU')
        if sale_price is not None:
            values['salePriceU'] = sale_price / 100
        return values


class Items(BaseModel):
    products: list[Item]
