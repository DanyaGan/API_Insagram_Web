import requests

import data # headers, cookies

    
class stalker:
    def __init__(self):
        self.url = 'https://www.instagram.com/api/v1'
        self.user_id: int

    def get_info_profile(self):
        params = {'username': self.user_name}

        r = requests.get(f'{self.url}/users/web_profile_info/',
            params=params,
            cookies=data.cookies,
            headers=data.headers_info,
        )
        if r.status_code == 200:
            r = r.json()
            if r['status'] == 'ok':
                return {
                    'status': r['status'],
                    'id': r['data']['user']['id'],
                    'links': [link['url'] for link in r['data']['user']['bio_links']],
                    'biography': r['data']['user']['biography_with_entities']['raw_text'],
                    'followed': r['data']['user']['edge_followed_by']['count'],
                    'follow': r['data']['user']['edge_follow']['count'],
                    'media': r['data']['user']['edge_owner_to_timeline_media']['count'],
                    'email': r['data']['user']['business_email'],
                    'phone': r['data']['user']['business_phone_number'],
                    'profile_pic': r['data']['user']['profile_pic_url'],
                }
            else:
                return {
                    'status': r['status']
                }
        else:
            return {
                'status': r.status_code
            }

    def get_post(self):
        params = {'count': '1'}

        r = requests.get(f'{self.url}/feed/user/{self.user_name}/username/',
            params=params,
            cookies=data.cookies,
            headers=data.headers_post,
        )
        if r.status_code == 200:
            r = r.json()
            if r['status'] == 'ok':
                posts = []
                for post in r['items']:
                    posts.append({
                        'status': post['status'],
                        'usertags': [ usertag['user']['username'] for usertag in post['usertags']['in']],
                        'likes': post['like_count'],
                        'text': post['caption']['text'],
                        'video': post['video_versions'][0],
                        'id': post['id'],
                        'time': post['caption']['created_at'],
                    })
            else:
                return {
                    'status': r['status']
                }
        else:
            return {
                'status': r.status_code
            }
    
    def get_reel(self):
        r = requests.get(f'{self.url}/feed/reels_media/?reel_ids={self.user_id}',
            cookies=data.cookies,
            headers=data.headers_info,
        )
        if r.status_code == 200:
            r = r.json()
            if r['status'] == 'ok':
                reels = {
                    'status': r['status'],
                    'items': []
                }
                
                for reel in r['reels'][self.user_id]['items']:
                    reels['items'].append({
                        'id': reel['id'],
                        'image': reel['image_versions2']['candidates'][0]['url']
                    })

                return reels
            
            else:
                return {
                    'status': r['status']
                }
        else:
            return {
                'status': r.status_code
            }
    

bot = stalker()
bot.user_name = 'instagram'
bot.user_id = bot.get_info_profile()['id']
print(bot.user_id)
profile_info = bot.get_reel()
print(profile_info)