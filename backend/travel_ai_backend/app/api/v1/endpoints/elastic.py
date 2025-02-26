from fastapi import APIRouter, Depends, Response
from elasticsearch import AsyncElasticsearch
from fastapi_pagination import Params

from travel_ai_backend.app.schemas.text_vector_schema import (
    ITextVectorCreate,
    ITextVectorSearch,
    ITextVectorBaseRead,
    ITextVectorSearchRead,
)
from travel_ai_backend.app.api.deps import get_elasticsearch_client
from travel_ai_backend.app.schemas.response_schema import (
    IGetResponsePaginated,
    IPostResponseBase,
    create_response,
)

router = APIRouter()


@router.post("/add_vector")
async def add_vector(
    text_vector: ITextVectorCreate,
    es: AsyncElasticsearch = Depends(get_elasticsearch_client),
) -> IPostResponseBase[ITextVectorBaseRead]:
    try:
        item = await es.index(
            index="text_vectors",
            body={"text": text_vector.text, "vector": text_vector.vector},
        )
        return create_response(data=item, message="Вектор добавлен успешно")
    except Exception as e:
        return Response(f"Internal server error. Error: {e}", status_code=500)

@router.post("/search_neighbors")
async def search_neighbors(
    text_vector: ITextVectorSearch,
    es: AsyncElasticsearch = Depends(get_elasticsearch_client),
) -> IGetResponsePaginated[ITextVectorSearchRead]:
    index_name = "text_vectors"
    query = {
        "query": {
            # "script_score": {
            #     "query": {"match_all": {}},
            #     "script": {
            #         "source": "cosineSimilarity(params.vector, 'vector') + 1.0",
            #         "params": {"vector": text_vector.vector},
            #     },
            # }
            "knn": {
                "field": "vector",
                "query_vector": text_vector.vector,
                "k": text_vector.k,
            }
        }
    }
    count_elem = await es.count(index=index_name)
    result = await es.search(index=index_name, body=query, size=text_vector.k)
    print(f"!!! {count_elem=}")
    response = []
    for v in result["hits"]["hits"]:
        response.append(
            ITextVectorSearchRead(
                id=v["_id"],
                index=v["_index"],
                score=v["_score"],
                vector=v["_source"]["vector"],
            )
        )

    # params_dict = {"size": 5, "page": 1}
    params = Params()
    params.page = 1
    params.size = count_elem["count"]
    response = IGetResponsePaginated.create(
        response, total=len(response), params=params
    )
    return create_response(data=response, message="Search Results")
