import time
import random

import threading
import uiautomator2

from core.pages import Page
from core.tiktok import TikTok
from core.utils import Utils

from adbutils import adb



def main(device_serial: str, index: int) -> None:
    device = uiautomator2.connect(device_serial)
    adb_device = adb.device(serial=device_serial)
    
    accounts = [i.replace('\n', '') for i in open(f'accounts/accounts{index}.txt', 'r', encoding='utf-8').read().split()]
    random.shuffle(accounts)


    utils = Utils(adb_device=adb_device, device=device)
    utils.initialize_device()

    while True:
        for account in accounts:
            utils.delete_every_media_file_from_gallery()

            adb_device.shell('am force-stop com.zhiliaoapp.musically') # Stop TikTok
            adb_device.shell('monkey -p com.zhiliaoapp.musically 1') # Start TikTok

            tiktok = TikTok(adb_device=adb_device, device=device)
            
            tiktok.switch_account_to(account)


            while not 'For You' in device.dump_hierarchy():
                pass
            tiktok.delete_videos_from_profile()
        
            for i in range(0, 6):
                utils.push_random_video_to_device()
            
            adb_device.shell('content call --method scan_volume --uri content://media --arg external_primary')

            for i in range(0, 3):
                tiktok.upload_video(video_number=i)
                time.sleep(10)
        
            time.sleep(15)



if __name__ == '__main__':
    for i, device in enumerate(adb.list()):
        print('Starting:', device.serial)
        threading.Thread(target=main, args=(device.serial, i + 1)).start()