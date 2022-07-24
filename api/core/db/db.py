from typing import List, Union, Iterable
from pymongo import MongoClient
from pymongo.results import (
        UpdateResult, InsertManyResult,
        InsertOneResult, DeleteResult
    )

from core.config import  config

MONGO_DATABASE_URI = config.MONGO_DATABASE_URI
PER_PAGE = config.PER_PAGE

class MongoDBClient:
    def __init__(self, database: str, collection: str) -> None:
        """
            Class to create mongodb client instance.
            Provides methods for common operations.
            :param database: Database to use.
            :param collection: MongoDB database collection t
                 be used
        """
        self.client = MongoClient(MONGO_DATABASE_URI)
        self.database = database
        self._set_collection(collection)
    
    def _set_collection(self, collection: str) -> None:
        self.cursor  = self.client[self.database]
        self.collection = self.cursor[collection]
        return self
    
    def find(self, filter: dict, projection: dict = {},
             skip: int = 0, limit: int = 0, sort: Union[List, str] = None) -> List[dict]:
        """
            Find element matching filter from collection
            :param filter: dictionary of filters to use in query
            :param projection: projections (i.e fields to 
                                            omit or include in result.)
            :param skip: Skip results.
            :param limit: Return limit number of result
            :param sort: field(s) to sort result by
        """
        res = self.collection.find(filter, projection=projection, 
                             skip=skip, limit=limit)
        if sort:
            res.sort(sort)
        return [data for data in res]

    def insert(self, data: Iterable,
                many: bool=False) -> Union[InsertOneResult, InsertManyResult]:
        """
            Insert one or multiple document into collection.
            :param data: Document(s) to insert.
            :param many: Insert more than one document
        """
        if many:
            res = self.collection.insert_many(data)
        else:
            res = self.collection.insert_one(data)
        return res
    
    def update(self, filter: dict, update: dict,
                many: bool=False) -> UpdateResult:
        """
            Update one or multiple document in collection.
            :param filter: Filter.
            :param update: Update to apply.
            :param many: Update more than one document.
        """
        if many:
            res = self.collection.update_many(filter, update)
        else:
            res = self.collection.update_one(filter, update)
        return res
    
    def delete(self, filter: dict, many: bool=False) -> DeleteResult:
        """
            Update one or multiple document in collection.
            :param filter: Filter.
            :param many: Delete more than one document.
        """
        if many:
            res = self.collection.delete_many(filter)
        else:
            res = self.collection.delete_one(filter)
        return res
    
    def paginate_find(self, filter: dict, page: int = 1,
                      per_page: int = PER_PAGE, projection: dict = {},
                      sort: Union[List, str] = None) -> dict:
        """
            :param filter: Filter.
            :param page: Page.
            :param per_page: per page.
            :param projection: projection.
        """
        if per_page == -1 or per_page > PER_PAGE:
            per_page = PER_PAGE
        skip = per_page * (page-1)
        data = self.find(filter, projection=projection, skip=skip,
                         limit=per_page, sort=sort)
        has_next = len(data) == per_page
        result = {"per_page": per_page, "page": page, "data": data,
                  "has_next": has_next}
        return result

        