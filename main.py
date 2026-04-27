from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/download")
async def get_url(video_id: str):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        # KRİTİK AYARLAR: YouTube'u kandıran kısım burası
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'web'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        'http_headers': {
            'User-Agent': 'com.google.ios.youtube/19.08.2 (iPhone16,2; U; CPU iOS 17_4 like Mac OS X; en_US)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # extract_info'da download=False diyerek sadece linki çekiyoruz
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            
            if not download_url:
                raise HTTPException(status_code=404, detail="Link bulunamadı")
                
            return {"download_url": download_url}
    except Exception as e:
        # Hatayı terminalde daha net görmek için yazdırıyoruz
        print(f"HATA OLUŞTU: {str(e)}")
        raise HTTPException(status_code=500, detail="YouTube Bot Korumasina Takildi")
