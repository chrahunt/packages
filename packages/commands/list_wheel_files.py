import click
from pymongo import MongoClient


wheelfile_pipeline = [
    {
        "$match": {
            "urls.filename": {
                "$regex": "\\.whl$"
            }
        }
    }, {
        "$unwind": {
            "path": "$urls",
            "preserveNullAndEmptyArrays": False
        }
    }, {
        "$project": {
            "urls": 1
        }
    }, {
        '$addFields': {
            'urls._id': '$_id'
        }
    }, {
        "$replaceRoot": {
            "newRoot": "$urls"
        }
    }, {
        "$match": {
            "filename": {
                "$regex": "\\.whl$"
            }
        }
    }
]


@click.command("list-wheel-files")
@click.option("--limit", type=int, default=100)
def command(limit):
    client = MongoClient()
    db = client.trash
    result = list(db.projects.aggregate(wheelfile_pipeline))
    urls = [o["url"] for o in result]
    size = sum(o["size"] for o in result)
    print(len(urls))
    print(size)
