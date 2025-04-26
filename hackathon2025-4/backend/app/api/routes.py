from fastapi import APIRouter, HTTPException
from app.services.news_service import NewsService
from app.services.ai_service import AIService

router = APIRouter()
news_service = NewsService()
ai_service = AIService()

@router.get("/news")
async def get_news():
    try:
        news = await news_service.get_latest_news()
        return {"status": "success", "data": news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/{news_id}")
async def get_news_by_id(news_id: str):
    try:
        news = await news_service.get_news_by_id(news_id)
        return {"status": "success", "data": news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/{news_id}/summary")
async def get_news_summary(news_id: str):
    try:
        news = await news_service.get_news_by_id(news_id)
        summary = await ai_service.summarize_news(news)
        return {"status": "success", "data": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 