import time
import uiautomator2

import core.buttons_coordinates
from core.pages import Page
from core.utils import Utils


class TikTok:
    def __init__(self, adb_device, device: uiautomator2.Device) -> None:
        self.__device = device
        self.__adb_device = adb_device
        self.__utils = Utils(adb_device=self.__adb_device, device=self.__device)


    def upload_video(self, video_number: int) -> None:
        post_button_was_clicked = False

        actions = {
            'introducing_n_minutes_video': (self.__device.click, core.buttons_coordinates.OK_INTRODUCING_N_MINUTES_VIDEOS),
            'view_your_friends_posts': (self.__device.click, core.buttons_coordinates.VIEW_YOUR_FRIENDS_POSTS),
            'view_history_turned_on_page': (self.__device.click, core.buttons_coordinates.CLOSE_LARGER_AUDIENCE_BUTTON),
            'post_video_page': (self.__device.click, core.buttons_coordinates.POST_BTN),
            'video_to_upload_preview': (self.__device.click, core.buttons_coordinates.NEXT_BTN),
            'media_in_gallery_board': (self.__device.click, self.__utils.get_video_to_upload_coordinates(video_number=video_number)),
            'camera_preview_page': (self.__device.click, core.buttons_coordinates.GO_TO_MEDIA_GALLERY_BOARD_BTN),
            'follow_your_friends_popup': (self.__device.click, core.buttons_coordinates.CLOSE_FOLLOW_YOUR_FRIENDS_BTN),
            'profile_button_exists':  (self.__device.click, core.buttons_coordinates.UPLOAD_BTN),
            'profile_page': (self.__device.click, core.buttons_coordinates.UPLOAD_BTN),
            'some_popup_menu': (self.__device.click, core.buttons_coordinates.DO_NOT_ALLOW_BTN)
        }

        while not post_button_was_clicked:
            page = Page(device=self.__device)
            try:
                if page.action in actions:
                    print(page.action)
                    if page.action == 'media_in_gallery_board':
                        time.sleep(3)
                        if 'Select multiple' not in self.__device.dump_hierarchy():
                            self.__utils.upload_video_in_select_multiple_page()
                            continue


                    action_function = actions[page.action][0]
                    action_function_args = actions[page.action][1]                
                    action_function(*action_function_args)

                    if action_function_args == core.buttons_coordinates.POST_BTN:
                        post_button_was_clicked = True
            except Exception as e: 
                print(e)

    def delete_videos_from_profile(self) -> None:
        while True:
            try:
                actions = {
                    'view_your_friends_posts': (self.__device.click, core.buttons_coordinates.VIEW_YOUR_FRIENDS_POSTS),
                    'view_history_turned_on_page': (self.__device.click, core.buttons_coordinates.CLOSE_LARGER_AUDIENCE_BUTTON),
                    'get_started_in_profile': (),
                    'larger_audience_button': (self.__device.click, core.buttons_coordinates.CLOSE_LARGER_AUDIENCE_BUTTON),
                    'guidelines_violation_video': (self.__utils.delete_blocked_video, ()),
                    'video_deleting_scrollbar': (self.__utils.swipe_deleting_scrollbar_and_delete_video, ()),
                    'video_preview_before_deleting': (self.__device.click, core.buttons_coordinates.THREE_DOTS_BTN),
                    'total_likes_popup': (self.__device.click, core.buttons_coordinates.CLOSE_TOTAL_LIKES_BTN),
                    'follow_your_friends_popup': (self.__device.click, core.buttons_coordinates.CLOSE_FOLLOW_YOUR_FRIENDS_BTN),
                    'profile_button_exists':  (self.__device.click, core.buttons_coordinates.PROFILE_PAGE_BTN),
                    'profile_page': (self.__device.click, self.__utils.get_the_first_video_in_profile_coordinates()),
                    'some_popup_menu': (self.__device.click, core.buttons_coordinates.DO_NOT_ALLOW_BTN),
                }
                page = Page(device=self.__device)

                if page.action in actions:
                    print(page.action)

                    if actions[page.action][1] == None:
                        return

                    if page.action == 'get_started_in_profile':
                        return

                    if page.action == 'profile_page':
                        if 'Get started' in self.__device.dump_hierarchy():
                            break
                        
                    if 'Upload' in self.__device.dump_hierarchy():
                        break

                    action_function = actions[page.action][0]
                    action_function_args = actions[page.action][1]             
                    action_function(*action_function_args)
                    time.sleep(3)

                    if page.action == 'total_likes_popup':
                        return
            except Exception as e: 
                print(e)

    def switch_account_to(self, account_nickname: str) -> None:
        while True:
            try:
                actions = {
                    'view_your_friends_posts': (self.__device.click, core.buttons_coordinates.VIEW_YOUR_FRIENDS_POSTS),
                    'view_history_turned_on_page': (self.__device.click, core.buttons_coordinates.CLOSE_LARGER_AUDIENCE_BUTTON),
                    'switch_account_popup': (self.__device.click, self.__utils.get_account_button_coordinates(nickname=account_nickname)),
                    'follow_your_friends_popup': (self.__device.click, core.buttons_coordinates.CLOSE_FOLLOW_YOUR_FRIENDS_BTN),
                    'profile_button_exists':  (self.__device.click, core.buttons_coordinates.PROFILE_PAGE_BTN),
                    'profile_page': (self.__device.click, core.buttons_coordinates.ACCOUNT_NICKNAME_BTN),
                    'some_popup_menu': (self.__device.click, core.buttons_coordinates.DO_NOT_ALLOW_BTN),
                }
                page = Page(device=self.__device)

                if page.action in actions:
                    print(page.action)
                    if actions[page.action][1] == None:
                        continue

                    action_function = actions[page.action][0]
                    action_function_args = actions[page.action][1]             
                    action_function(*action_function_args)
                
                if page.action == 'switch_account_popup':
                    break
            except Exception as e: 
                print(e)