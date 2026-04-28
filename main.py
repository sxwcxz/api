from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/download")
async def get_url(video_id: str):
    # Linki direkt YouTube Music üzerinden istiyoruz
    video_url = f"https://music.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        # KRİTİK: OpenTune'un yaptığı gibi iOS istemcisini taklit ediyoruz
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        # YouTube Music API'sini tetikleyen User-Agent
        'http_headers': {
            'User-Agent': 'com.google.ios.youtube/19.17.4 (iPhone16,2; U; CPU iOS 17_5 like Mac OS X; en_US)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://music.youtube.com/',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Sadece meta veriyi ve indirme linkini çek
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            
            if not download_url:
                raise HTTPException(status_code=404, detail="Müzik linki ayıklanamadı")
                
            return {"download_url": download_url}
    except Exception as e:
        print(f"Detaylı Hata: {str(e)}")
        # Eğer bu da hata verirse, YouTube sunucu IP'sini tamamen bloklamış demektir
        raise HTTPException(status_code=500, detail="YouTube Music baglantiyi reddetti")
