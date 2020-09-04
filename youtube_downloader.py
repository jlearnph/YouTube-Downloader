#JLearn PH

from pytube import Playlist
from pytube import YouTube
import re
import PySimpleGUI as sg

# sg.theme('DarkAmber')  #theme

layout = [[sg.Text('Enter video / playlist link: ')],      
          [sg.Input(key='link')],
          [sg.Text('Download Folder: '), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
          [sg.Button('Download'), sg.Exit()],
          [sg.Text('Downloading:'), sg.Text(size=(15,1), key='-OUTPUT-')]
          ]      

window = sg.Window('YouTube Downloader by Lester', layout)      

while True:                         
    event, values = window.read()
    link = values['link']
    show = ''
    download_folder = values['-FOLDER-']

    #for a playlist
    if event == 'Download':
        try:
            playlist = Playlist(link)
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            show += f'\nStarting download for {len(playlist.video_urls)} videos\n'
            count = 1
            for url in playlist.video_urls:
                try:
                    yt = YouTube(link)
                    yt.streams.first().download(download_folder)
                    show += f'\n[+] Success {count}: {yt.title}'
                except:
                    show += f'\n[+] Failed {count}: {yt.title}'
                count +=1
                window['-OUTPUT-'].update(f'{count-1}/{len(playlist.video_urls)}')

        #for only 1 video
        except:
            show += '\nStarting download for 1 video\n'
            show += f'\n[+] Video: {link}'
            YouTube(link).streams.first().download(download_folder)
        
        sg.popup_scrolled(f'{show}\n\nFinished Downloading\n', size=(100,20))
        

    if event == sg.WIN_CLOSED or event == 'Exit':
        break      

window.close()
