from pytube import YouTube

url = input("Enter the URL of the YouTube video: ")
yt = YouTube(url).streams.first().download()

yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

print("Video downloaded successfully!")
