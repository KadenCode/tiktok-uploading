import uiautomator2


class Page:
    def __init__(self, device: uiautomator2.Device) -> None:
        self.__device = device
        self.__page_xml_layout = self.__device.dump_hierarchy()

    @property
    def action(self) -> str:
        actions_anchors = {
            'minutes video': 'introducing_n_minutes_video',
            "View your friends' posts": 'view_your_friends_posts',
            'view history turned on': 'view_history_turned_on_page',
            'Want to reach a larger audience?': 'larger_audience_button',
            'Switch account': 'switch_account_popup',
            'Total likes': 'total_likes_popup',
            "Don’t allow": 'some_popup_menu',
            'Everyone can view this post': 'post_video_page',
            'Next': 'video_to_upload_preview',
            'All': 'media_in_gallery_board',
            '15s': 'camera_preview_page',
            'Share to': 'video_deleting_scrollbar',
            'Edit profile': 'profile_page',
            'Guidelines violation': 'guidelines_violation_video',
            'Find related content': 'video_preview_before_deleting',
            'Profile': 'profile_button_exists',
        }

        for action_anchor in actions_anchors:
            if action_anchor in self.__page_xml_layout:
                return actions_anchors[action_anchor]