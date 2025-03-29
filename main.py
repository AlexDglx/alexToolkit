from nicegui import ui, run
from backend import Image, YTDownloader
from multiprocessing import Manager, Queue
import asyncio

import os
import time


def convertImage():

    if input_image.value and output_image.value:
        if os.path.exists(input_image.value):
            print(input_image.value)
            image = Image(input_image.value)
            
            try:
                image.convert(image.directory, output_image.value, selected_chip.value)
                with ui.dialog() as dialog, ui.card():
                    with ui.row().classes('items-center w-full'):
                        ui.image('https://img.icons8.com/?size=100&id=63262&format=png&color=000000').classes('w-8 justify-self-center')

                        ui.label(f'File converted:\n{os.path.join(image.directory)}.{selected_chip.value}')
                    ui.button('Close', on_click=dialog.close).classes('items-center w-full')
                dialog.open()
                input_image.set_value('')
                output_image.set_value('')
                selected_chip.set_value('')

            except Exception as err:
                with ui.dialog() as dialog, ui.card():
                    with ui.row().classes('items-center w-full'):
                        ui.image('https://img.icons8.com/?size=100&id=63262&format=png&color=000000').classes('w-8 justify-self-center')
                        ui.label(f'An error occured:\n{err}')
                    ui.button('Close', on_click=dialog.close).classes('items-center w-full')
                dialog.open()
        else:
            with ui.dialog() as dialog, ui.card():
                with ui.row().classes('items-center w-full'):
                        ui.image('https://img.icons8.com/?size=100&id=63262&format=png&color=000000').classes('w-8')
                        ui.label(f'Input error:\nFile does not exist.')
                ui.button('Close', on_click=dialog.close).classes('items-center w-full')
            dialog.open()
    else:

        with ui.dialog() as dialog, ui.card():
            with ui.row().classes('items-center w-full'):
                ui.image('https://img.icons8.com/?size=100&id=63688&format=png&color=000000').classes('w-8')
                ui.label(f'File input :\nInput or outut missing')
            ui.button('Close', on_click=dialog.close).classes('items-center w-full')
        dialog.open()
        return
    
    if not selected_chip:
        ui.notify('Select a file extension')

def download_song():
    print()

def ytDownloader():
    
    try:
        
        progressbar.visible = True
        
        if media_toggle.value=="Audio" :
            
            if input_image.value !=' ' and media_output_name.value != ' ':
                
                downloader = YTDownloader('/Users/adegallaix/Downloads',youtube_url.value, audio_format.value,media_output_name.value)
                        
                with ui.dialog() as dialog, ui.card():
                    with ui.row().classes('items-center w-full'):
                        ui.image('https://img.icons8.com/?size=100&id=63262&format=png&color=000000').classes('w-8 justify-self-center')
                        ui.label(f'File {media_output_name.value} downloaded')
                    ui.button('Close', on_click=dialog.close).classes('items-center w-full')

                downloader.audio_download()  
                dialog.open()
                
            else:
                with ui.dialog() as dialog, ui.card():
                        with ui.row().classes('items-center w-full'):
                            ui.image('https://img.icons8.com/?size=100&id=63688&format=png&color=000000').classes('w-8 justify-self-center')

                            ui.label(f'Missing input or output file')
                        ui.button('Close', on_click=dialog.close).classes('items-center w-full')
                
                dialog.open()

        if media_toggle.value=="Video":
            downloader = YTDownloader('/Users/adegallaix/Downloads',youtube_url, video_format,media_output_name)
            downloader.video_download()
            
            with ui.dialog() as dialog, ui.card():
                with ui.row().classes('items-center w-full'):
                    ui.image('https://img.icons8.com/`  ?size=100&id=63262&format=png&color=000000').classes('w-8 justify-self-center')
                    ui.label(f'File {media_output_name.value}.{video_format} downloaded')
                ui.button('Close', on_click=dialog.close).classes('items-center w-full')
                
            dialog.open()   
        progressbar.visible = False
        
    except Exception as err:
        
        with ui.dialog() as dialog, ui.card():
            with ui.row().classes('items-center w-full'):
                    ui.image('https://img.icons8.com/?size=100&id=63688&format=png&color=000000').classes('w-8')
                    ui.label(f'Input error:\n{err}.')
            ui.button('Close', on_click=dialog.close).classes('items-center w-full')
        dialog.open()    
    

with ui.tabs().classes('w-full') as tabs:
    tab1 = ui.tab('Image & Video').classes('w-full')
    tab2 = ui.tab('Text').classes('w-full')
    tab3 = ui.tab('Mapping').classes('w-full')
    tab4 = ui.tab('Currency').classes('w-full')
    tab5 = ui.tab('Scanning').classes('w-full')


with ui.tab_panels(tabs, value=tab1):
    with ui.tab_panel(tab1).classes('content-center').style("height: 100vh; width: 100vw;"):
        ui.markdown('###Image converter###')
        
        with ui.card().classes("w-full h-full items-center justify-center"):
            with ui.row():
                input_image = ui.input('Path', placeholder="image path").props('clearable').classes("w-full flex items-center justify-center")
                output_image = ui.input('Output', placeholder="image output name").props('clearable').classes("w-full flex items-center justify-center")
                with ui.row().classes('items-center'):
                    ui.markdown("Format:")
                    selected_chip = ui.select(['bmp','exr', 'jpeg', 'gif','png', 'tiff', 'webm','webp'])
                    result = ui.label()
                               
            ui.button(text='Convert', on_click=convertImage).classes("flex items-center justify-center")
            
        ui.markdown('###Youtube Downloader###')
        with ui.card().props('flat bordered').classes("w-full h-full items-center justify-center"):
            
            media_toggle = ui.toggle(["Audio","Video"], value="Audio")
            
            with ui.grid(columns=2):
                with ui.row().classes('items-center'):
                    ui.label("Audio format:")
                    audio_format = ui.select(['aac','avi', 'flac','mp3','opus','wav','webm'], value=None)
                    
                with ui.row().classes('items-center'):
                    ui.label("Video format:")
                    video_format = ui.select(['avi', 'mkv','mp4', 'mov','mxf', 'wmv'],value=None)
                        
            with ui.row().classes('items-center'):
                    youtube_url = ui.input('url', placeholder="youtube url").props('clearable').classes("w-full flex items-center justify-center")
                    media_output_name = ui.input('output', placeholder="image output").props('clearable').classes("w-full flex items-center justify-center")
           
            progressbar = ui.linear_progress(value=0).props('instant-feedback')
            progressbar.visible = False
            ui.button(text='Download', on_click=ytDownloader)
            
            #progressbar.visible = False                  
                
                # ['aac','avi', 'flac','mp3','wav']
                # ['avi', 'mkv','mp4', 'mov','mxf', 'wmv']
    
        ui.markdown("###Video converter###")

                            
    with ui.row().classes('w-full').style('gap: 10px; flex-wrap: nowrap;'):
        with ui.tab_panel(tab2):
            ui.label('Content for Tab 2')
            with ui.column():
                ui.button('Button inside tab 2')
                ui.markdown('Some **markdown** text')
    with ui.row().classes('w-full').style('gap: 10px; flex-wrap: nowrap;'):
        with ui.tab_panel(tab3):
            ui.label('Content for Tab 3')
            with ui.column():
                ui.button('Button inside tab 3')
                ui.markdown('Some **markdown** text')
    with ui.row().classes('w-full').style('gap: 10px; flex-wrap: nowrap;'):
        with ui.tab_panel(tab4):
            ui.label('Content for Tab 4')
            with ui.column():
                ui.button('Button inside tab 4')
                ui.markdown('Some **markdown** text')
    with ui.row().classes('w-full').style('gap: 10px; flex-wrap: nowrap;'):
        with ui.tab_panel(tab5):
            ui.label('Content for Tab 4')
            with ui.column():
                ui.button('Button inside tab 4')
                ui.markdown('Some **markdown** text')
    
ui.run()

