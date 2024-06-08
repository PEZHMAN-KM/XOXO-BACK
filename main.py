from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal, engine, UserGameResult 

app = FastAPI()

class GameResultModel(BaseModel):
    name: str
    status: str

@app.post("/update_victory_count/")
async def update_victory_count(game_results: List[GameResultModel]):
    db = SessionLocal()
    try:
        for result in game_results:
            existing_user = db.query(UserGameResult).filter(UserGameResult.name == result.name).first()
            if existing_user:
                if result.status == "WIN":
                    existing_user.victories += 1
                else:
                    existing_user.victories -= 1
                db.commit()
            else:
                new_user = UserGameResult(name=result.name)
                db.add(new_user)
                if result.status == "WIN":
                    new_user.victories = 1
                db.commit()
        return {"message": "Victory counts updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()



@app.get("/top_users")
async def get_top_users():
    db = SessionLocal()
    try:
        top_users_query = db.query(UserGameResult).order_by(UserGameResult.victories.desc()).limit(10)
        top_users = db.execute(top_users_query).fetchall()
        return [{"name": user[0].name, "victories": user[0].victories} for user in top_users]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve top users.")
    finally:
        db.close()

