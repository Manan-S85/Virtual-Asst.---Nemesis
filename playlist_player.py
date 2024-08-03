import os
import vlc
from utilities import takeCommand, speak


#song_path = "VA/MAIN/playlist"
def play_song(song_path):
    """
    Play a song using VLC media player.

    Args:
        song_path (str): Path to the song file.

    Returns:
        None
    """
    try:
        player = vlc.MediaPlayer(song_path)
        player.play()
        speak(f"Now playing: {song_path}")
        return player
    except Exception as e:
        speak(f"Error playing song: {e}")
        return None

def play_playlist(folder_path):
    """
    Play songs from a folder.

    Args:
        folder_path (str): Path to the folder containing music files.

    Returns:
        None
    """
    try:
        songs = [file for file in os.listdir(folder_path) if file.endswith((".mp3", ".wav"))]
        if not songs:
            speak("No music files found in the folder.")
            return
        
        for song in songs:
            song_path = os.path.join(folder_path, song)
            player = play_song(song_path)
            if player:
                speak("Please say 'Next' to play the next song.")
                takeCommand()  # Wait for user command
                player.stop()  # Stop playing the current song
    except Exception as e:
        speak("Error playing playlist")
        print("Error playing playlist:", e)

# Other functions (pause, resume, stop) remain the same
def pause_playlist(player):
    """
    Pause the currently playing song in the playlist.

    Args:
        player (vlc.MediaPlayer): VLC media player instance.

    Returns:
        None
    """
    if player is not None:
        player.pause()
        speak("Playlist paused.")

def resume_playlist(player):
    """
    Resume the paused playlist.

    Args:
        player (vlc.MediaPlayer): VLC media player instance.

    Returns:
        None
    """
    if player is not None:
        player.play()
        speak("Playlist resumed.")

def stop_playlist(player):
    """
    Stop playing the playlist.

    Args:
        player (vlc.MediaPlayer): VLC media player instance.

    Returns:
        None
    """
    if player is not None:
        player.stop()
        speak("Playlist stopped.")

def main():
    """
    Main function to demonstrate the usage of playlist functions.
    """
    player = None
    while True:
        command = takeCommand().lower()
        if "play" in command:
            folder_path = "VA/MAIN/playlist"  # Replace with the path to your music folder
            play_playlist(folder_path)
        elif "pause" in command:
            pause_playlist(player)
        elif "resume" in command:
            resume_playlist(player)
        elif "stop" in command:
            stop_playlist(player)
        elif "exit" in command:
            if player is not None:
                stop_playlist(player)
            break
        else:
            speak("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
