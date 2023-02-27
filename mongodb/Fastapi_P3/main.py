from fastapi import FastAPI,Response,status
import pymongo
import csv
import json
import sys, getopt, pprint
from pymongo import MongoClient
from pprint import pprint
import pandas as pd
from pydantic import BaseModel
from typing import List

client = pymongo.MongoClient("mongodb://root:example@172.24.0.2:27017")
mydb = "Electronic_product"
mycol = "sales"



class Pproduct(BaseModel):
    name: str
    brand: str


class ssales(BaseModel):
	prices_amountmax: int = 15
	prices_amountmin: int = 50
	prices_availability: str = "toto"
	prices_condition: str = "toto"
	prices_currency: str = "toto"
	prices_dateseen: str = "toto"
	prices_issale: str = "toto"
	prices_merchant: str = "toto"
	prices_shipping: str = "toto"
	prices_sourcestrs: str = "toto"
	asins: str = "toto"
	brand: str = "sony"
	categories: str = "toto"
	dateadded: str = "toto"
	dateupdated: str = "toto"
	ean: str = "toto"
	imagestrs: str = "toto"
	keys: str = "toto"
	manufacturer: str = "toto"
	manufacturernumber: str = "toto"
	name: str = "toto"
	primarycategories: str = "toto"
	sourcestrs: str = "toto"
	upc: str = "toto"
	weight: str = "toto"


api = FastAPI()

@api.get('/')
def get_index():
    return {'data': 'hello world'}


@api.get("/status")
def get_status():
    """Get status of messaging server."""
    return {"status": "running"}




@api.get("/products", response_model=List[str])
def get_products():
    """Get all channels in list form."""
    with MongoClient("mongodb://root:example@172.18.0.3:27017") as client:
        msg_collection = client[mydb][mycol]
        distinct_channel_list = msg_collection.distinct("name")
        return distinct_channel_list




@api.get("/productbybrand/{brand}", response_model=List[Pproduct])
def get_productbybrand(brand: str):
	"""Get all messages for the specified channel."""
	with MongoClient("mongodb://root:example@172.18.0.3:27017") as client:
		msg_collection = client[mydb][mycol]
		#msg_list = msg_collection.find({"brand": brand})

		msg_list=msg_collection.aggregate([
		 	{ "$match" : {"brand" : brand }},
			#{"$unwind": {"_id": {"$name","$brand"}} } ,
			{"$group": {
      			"_id": {
				"name": "$name",
				"brand": "$brand",
				}
			}
			},
			{"$project": {
				"_id": 0,
				"name": "$_id.name",
				"brand": "$_id.brand"
			}}
			])

		msg_list
		response_msg_list = []
		for msg in msg_list:
			response_msg_list.append(Pproduct(**msg))
		return response_msg_list

@api.post("/post_message", status_code=status.HTTP_201_CREATED)
def post_message(sales: ssales):
    """Post a new message to the specified channel."""
    with MongoClient("mongodb://root:example@172.18.0.3:27017") as client:
        msg_collection = client[mydb][mycol]
        result = msg_collection.insert_one(sales.dict())
        ack = result.acknowledged
        return {"insertion": ack}
