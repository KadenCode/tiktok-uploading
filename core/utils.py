import os
import time
import json
import random
import math

import uiautomator2
import adbutils

import core.buttons_coordinates


class Utils:
    def __init__(self, adb_device, device: uiautomator2.Device) -> None:
        self.device = device
        self.adb_device = adb_device

    def get_quantity_of_media_in_gallery(self) -> int:
        files = self.device.shell('ls sdcard/DCIM/Camera').output.split()
        return len(files)

    def initialize_device(self) -> None:
        self.adb_device.shell('wm size 1080x2400')
        self.adb_device.shell('wm density 420')
        self.adb_device.shell('svc power stayon true')
        self.adb_device.shell('pm grant com.zhiliaoapp.musically android.permission.READ_EXTERNAL_STORAGE')
        self.adb_device.shell('pm grant com.zhiliaoapp.musically android.permission.READ_MEDIA_VIDEO')
        self.adb_device.shell('pm grant com.zhiliaoapp.musically android.permission.READ_MEDIA_VISUAL_USER_SELECTED')
        self.adb_device.shell('pm grant com.zhiliaoapp.musically android.permission.READ_MEDIA_IMAGES')
        self.adb_device.shell('pm grant com.zhiliaoapp.musically android.permission.POST_NOTIFICATION')
        self.adb_device.shell('pm grant com.zhiliaoapp.musically android.permission.CAMERA')
        self.adb_device.shell('pm grant com.zhiliaoapp.musically android.permission.RECORD_AUDIO')

    def get_video_to_upload_coordinates(self, video_number: int) -> tuple:
        videos_count = self.get_quantity_of_media_in_gallery() - video_number
        rows_count = math.ceil(videos_count / 3)
        columns_count = videos_count % 3 if videos_count % 3 != 0 else 3

        return (5 + (columns_count - 1) * 369, 352 + (rows_count - 1) * 369)

    def upload_video_in_select_multiple_page(self) -> None:
        self.device.click(*self.get_video_to_upload_coordinates_in_select_multiple())
        time.sleep(3)
        self.device.click(*core.buttons_coordinates.SELECT_VIDEO_BUTTON)
        time.sleep(2)
        self.device.click(*core.buttons_coordinates.BACK_TO_MEDIA_BOARD_BUTTON)
        time.sleep(3)
        self.device.click(*core.buttons_coordinates.OK_BUTTON_IN_MEDIA_GALLERY)
        
    def get_video_to_upload_coordinates_in_select_multiple(self, video_number: int) -> tuple:
        videos_count = self.get_quantity_of_media_in_gallery() - video_number
        rows_count = math.ceil(videos_count / 4)
        columns_count = videos_count % 4 if videos_count % 4 != 0 else 4

        return (5 + (columns_count - 1) * 260, 352 + (rows_count - 1) * 265)

    def get_the_first_video_in_profile_coordinates(self) -> tuple:
        try:
            text_views = self.device.xpath('//android.widget.TextView').all()[::-1]
            filtered_text_views = [text_view for text_view in text_views if text_view.info['text'].isdigit() or text_view.info['text'] in ['Community Guidelines violation', 'Likes']]
            

            if text_views[0].info['text'] == 'Likes':
                return None

            for i, text_view in enumerate(filtered_text_views): 
                if text_view.info['text'].isdigit():
                    if text_views[i+1] == 'Inbox':
                        continue

                coordinates = text_view.info['bounds']
                x = int(coordinates['left'])
                y = int(coordinates['top'])

                return (x + 20, y + 20)
        except IndexError:
            pass
    
    def swipe_deleting_scrollbar_and_delete_video(self) -> None:
        delete_button = self.device.xpath('//*[@content-desc="Delete"]')

        self.device.swipe(1000, 2216, 5, 2216)
        self.device.swipe(1000, 2216, 5, 2216)

        delete_button.click_exists(1)
        self.device.xpath('//*[@text="Delete"]').click()

    def push_random_video_to_device(self) -> None:
        random_video = random.choice(os.listdir('media/videos'))
        self.adb_device.sync.push(f'media/videos/{random_video}', f'sdcard/DCIM/Camera/{random_video}')
        self.device.shell(
            f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d "file:///sdcard/DCIM/Camera/{random_video}"')

    def get_account_button_coordinates(self, nickname: str) -> tuple:
        if 'Switch account' in self.device.dump_hierarchy():
            account = self.device(text=nickname)
            account_coordinates = account.info['bounds']
            account_coordinates = (account_coordinates['left'] + 10, account_coordinates['top'] + 5)
            return account_coordinates

    def delete_blocked_video(self) -> None:
        self.device.click(959 + 20, 1863 + 20)
        time.sleep(2)
        self.device.click(55 + 30, 2013 + 30)
        time.sleep(2)
        self.device.click(540 + 100, 1345 + 100)

    def delete_every_media_file_from_gallery(self) -> None:
        self.device.shell('cd /sdcard/DCIM/Camera && rm -rf *.mp4')
        self.device.shell('cd /sdcard/DCIM/Camera && rm -rf *.mov')
        self.device.shell('cd /sdcard/DCIM/Camera && rm -rf *.png')
        self.device.shell('cd /sdcard/DCIM/Camera && rm -rf *.jpg')
        self.device.shell('cd /sdcard/DCIM/Camera && rm -rf *.jpeg')