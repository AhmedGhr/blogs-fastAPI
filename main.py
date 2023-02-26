from bson import ObjectId
from fastapi import Body, FastAPI, HTTPException
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# alowing cors origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# connecting to the mongo atlas client and getting the blogs db and collection
client = MongoClient(
    "mongodb+srv://ahmed:ahmed123@cluster0.or386.mongodb.net/?retryWrites=true&w=majority")
db = client["blogs"]
collection = db["blogs"]

# test endpoint


@app.get("/")
async def root():
    return {"message": "Hello World"}

# get all blogs


@app.get("/blogs/")
async def get_all_items():
    items = []
    for item in collection.find():
        # remove the _id field to prevent the iterable error
        item.pop('_id')
        items.append(item)
    return {"items": items}

# post a blog


@app.post("/blog")
async def post_blog(id=Body(...), title: str = Body(...), content: str = Body(...), author: str = Body(...), upvotes: int = Body(...), downvotes: int = Body(...)):
    post = {"id": id, "title": title, "content": content,
            "author": author, "upvotes": upvotes, "downvotes": downvotes}
    result = collection.insert_one(post)
    return {"id": str(result.inserted_id)}

# get one blog using it's id


@app.get("/blogs/{blog_id}")
async def read_blog(blog_id: int):
    blog = collection.find_one({"id": blog_id})
    # remove the _id field to prevent the iterable error
    blog.pop('_id')
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


@app.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: int):
    blog = collection.find_one({"id": blog_id})
    # remove the _id field to prevent the iterable error
    blog.pop('_id')
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    collection.delete_one({"id": blog_id})
    return {"success": "Blog deleted"}
