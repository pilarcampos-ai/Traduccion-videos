# 1. Descarga del audio mejorada para evitar el error 403
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'audio_para_traducir.%(ext)s',
                    'nocheckcertificate': True, # Ignora errores de certificado
                    'quiet': True,
                    'no_warnings': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                    }],
                }
