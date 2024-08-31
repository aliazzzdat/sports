import gradio as gr
import yt_dlp
import os
import main as mn

modes = [
    "PITCH_DETECTION",
    "PLAYER_DETECTION",
    "BALL_DETECTION",
    "PLAYER_TRACKING",
    "TEAM_CLASSIFICATION",
    "RADAR"
]

def get_sample_videos():
    return [f for f in os.listdir("data") if (f.endswith(".mp4") & ('rf_downloaded_video.mp4' not in f))]

def process_video(video_path, mode):
    rf_video_path = "data/rf_downloaded_video.mp4"
    mn.main(
        source_video_path=video_path,
        target_video_path=rf_video_path,
        device="gpu",
        mode=mode,
        display=False
    )
    print("The video has been processed")
    return video_path, rf_video_path

def download_and_play_video(sample_input, video_input, mode):
    if video_input:
        print("Youtube video")
        video_path = "data/downloaded_video.mp4"
        # Configure yt-dlp options
        ydl_opts = {
            'outtmpl': video_path,
            'format': 'best[ext=mp4][filesize<100M]',
        }

        # Download the video
        try:
            ydl = yt_dlp.YoutubeDL(ydl_opts)
            ydl.download([video_input])
            print("The video has been downloaded")
        except yt_dlp.utils.DownloadError:
            return "Error: No suitable format found under 100MB", "Error: No suitable format found under 100MB"
        except Exception as e:
            print(e)
            return f"Error: {e}", f"Error: {e}"
    else:
        print("Sample video")
        video_path = os.path.join("data", sample_input)
    
    return process_video(video_path, mode)

# Create the Gradio interface
demo = gr.Interface(
    fn=download_and_play_video,
    inputs=[
        gr.Dropdown(label="Select sample video", choices=get_sample_videos(), value=get_sample_videos()[0]),
        gr.Textbox(label="Or enter YouTube URL", placeholder="https://www.youtube.com/watch?v=_i0IjKSac_0"),
        gr.Dropdown(label="Select Mode", choices=modes, value="PLAYER_DETECTION")
    ],
    outputs=[
        gr.Video(label="Normal"),
        gr.Video(label="with CV")
    ],
    title="Soccer detection",
    description="Select a sample video or enter a YouTube URL to download and play it on two screens. If entering a URL, the video must be less than 100MB. Select a mode for CV processing. Be patient, the processing can be long depending on the video length and the device."
)

# Launch the app
demo.launch()
