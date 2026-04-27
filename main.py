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
    # YouTube bot korumasını aşmak için istemciyi taklit et
    'youtube_include_dash_manifest': False,
    'nocheckcertificate': True,
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://www.youtube.com',
    },
    # PO Token ve diğer bot korumalarını bypass etmek için 'ios' istemcisini zorla
    'extractor_args': {
        'youtube': {
            'player_client': ['ios'],
        }
    }
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
