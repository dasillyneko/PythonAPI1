from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from httpx import options
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class posts(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]=None
    

    
my_posts=[{"title": "title of post 1", "content": "content of post 1", "id": 1},
        {"title": "foods", "content": "biryani", "id": 2}]

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

@app.get("/")
def root():
    return {"message": "hello fellas"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: posts):
    post_dict=post.dict()
    post_dict['id']=randrange(3,10000000)
    my_posts.append(post_dict)
    return {"data":post_dict}


    
@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        #return {"message": "post not found"}
    return {"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    index=find_index_post(id)
    
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post:posts):
    index=find_index_post(id)
    
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {"data":post_dict}
