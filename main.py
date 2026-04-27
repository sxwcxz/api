from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/download")
async def get_download_link(video_id: str):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # yt-dlp ayarları: Sadece sesi en yüksek kalitede bulur
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            
            if not download_url:
                raise HTTPException(status_code=404, detail="Link bulunamadı")
                
            return {"download_url": download_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
