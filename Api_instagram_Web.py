import requests

    
class stalker:
    def __init__(self):
        self.url = 'https://www.instagram.com/api/v1'
        self.user_id: int

        self.headers: dict
        self.cookies: any

    def get_info_profile(self):
        params = {'username': self.user_name}

        r = requests.get(f'{self.url}/users/web_profile_info/', params=params, cookies=self.cookies, headers=self.headers)

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

    def get_post(self, end_cursor=''):
        data = {
            'av': '17841464967642321',
            '__d': 'www',
            '__user': '0',
            '__a': '1',
            '__req': 'n',
            '__hs': '19796.HYP:instagram_web_pkg.2.1..0.1',
            'dpr': '1',
            '__ccg': 'UNKNOWN',
            '__rev': '1012053868',
            '__s': 'b8tnar:5zmuy6:mho80i',
            '__hsi': '7346193569082335786',
            '__dyn': '7xeUjG1mxu1syUbFp40NonwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO0FE2awpUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U1bobpEbUGdwtU662O0z8c86-3u2WE5B0bK1Iwqo5q1IQp1yUoxeubxKi2K9xi',
            '__csr': 'h42vviky2QZjhfczR25OtN3sGaWmXEWpuqikGlFtIB9bLOzGV4y92uWiRVVoyqbladBGWgCWFdp9VuvCJb-9BWgy8XWjKaBKp2U-uqpmdBAUHXHABBzF8gxtF5z_J4ABK2N39U9USFEyU01jS9B80qa0Ikm0Ly016y072oyikg0wzF5t5gG8l1a2Sqq1wg0OW0nW0qZ12rc0UU0Oy0gS0iKt2F600AmE',
            '__comet_req': '7',
            'fb_dtsg': 'NAcMd006mIFTZv0SoeHCQ30Oec4XSVTuyllK7amQIa-KrGrRIIv1pHA:17853599968089360:1709829496',
            'jazoest': '26114',
            'lsd': 'FiBtataTVKbeTNM7vx2Q1F',
            '__spin_r': '1012053868',
            '__spin_b': 'trunk',
            '__spin_t': '1710418977',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'PolarisProfilePostsQuery',
            'variables': '{"after":"'+end_cursor+'","before":null,"data":{"count":12,"include_relationship_info":true,"latest_besties_reel_media":true,"latest_reel_media":true},"username":"'+self.user_name+'","__relay_internal__pv__PolarisShareMenurelayprovider":false}',
            'server_timestamps': 'true',
            'doc_id': '7094391783991078',
        }

        response = requests.post('https://www.instagram.com/api/graphql', cookies=self.cookies, headers=self.headers, data=data)

        if response.status_code == 200:
            
            response = response.json()
            if response['extensions']['is_final']:
                posts = {
                    'status': 'ok' if response['extensions']['is_final'] else 'Error',
                    'end_cursor': response['data']['xdt_api__v1__feed__user_timeline_graphql_connection']['page_info']['end_cursor'],
                    'items': [],
                }
                
                for post in response['data']['xdt_api__v1__feed__user_timeline_graphql_connection']['edges']:
                    posts['items'].append({
                        'usertags': [[usertag['user']['id'], usertag['user']['username']] for usertag in post['node']['usertags']['in']],
                        'id': post['node']['id'],
                        'text': post['node']['caption']['text'],
                        'img': post['node']['image_versions2']['candidates'][0]['url'],
                        'likes': post['node']['like_count'],
                        'commnet': post['node']['comment_count'],
                        'time': post['node']['caption']['created_at'],
                    })
                return posts
            else:
                return {
                    'status': response['status']
                }
        else:
            return {
                'status': response.status_code
            }
    
    def get_reel(self):
        r = requests.get(f'{self.url}/feed/reels_media/?reel_ids={self.user_id}',
            cookies=self.cookies,
            headers=self.headers,
        )
        if r.status_code == 200:
            r = r.json()
            if r['status'] == 'ok':

                reels = {
                    'status': r['status'],
                    'items': []
                }
                
                if not r['reels']:
                    return {
                        'status': 'unknown issue'
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
    
    def list_popular_history(self):

        params = {
            'query_id': '9957820854288654',
            'user_id': str(self.user_id),
            'include_chaining': 'false',
            'include_reel': 'true',
            'include_suggested_users': 'false',
            'include_logged_out_extras': 'false',
            'include_live_status': 'false',
            'include_highlight_reels': 'true',
        }

        response = requests.get('https://www.instagram.com/graphql/query/', params=params, cookies=self.cookies, headers=self.headers)

        if response.status_code == 200:
            response = response.json()
            if response['extensions']['is_final']:
                list_reels = {
                    'status': 'ok' if response['extensions']['is_final'] else 'Error',
                    'items': [],
                }
                
                for reel in response['data']['user']['edge_highlight_reels']['edges']:
                    list_reels['items'].append({
                        'title': reel['node']['title'],
                        'id': reel['node']['id'],
                        'media': reel['node']['cover_media']['thumbnail_src'],
                    })

                return list_reels
            else:
                return {
                    'status': response['extensions']['is_final']
                }
        else:
            return {
                'status': response.status_code
            }
    
    def get_popular_history_media(self, id):
        data = {
        'av': '17841464967642321',
        '__d': 'www',
        '__user': '0',
        '__a': '1',
        '__req': 'y',
        '__hs': '19797.HYP:instagram_web_pkg.2.1..0.1',
        'dpr': '1',
        '__ccg': 'UNKNOWN',
        '__rev': '1012081461',
        '__s': 'syyxqw:7b3p53:6riitm',
        '__hsi': '7346560445229602364',
        '__dyn': '7xeUjG1mxu1syUbFp40NonwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO0FE2awpUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U1bobpEbUGdwtU662O0z8c86-3u2WE5B0bK1Iwqo5q1IQp1yUoxeubxKi2K9xi',
        '__csr': 'g8YLRr95ijNJ8Bil25ZjldaylQOOUBSbFarll5liZKiWnyuGBBh2JBmV9rDF2k8x96ADFH9GagWVaJe_leuaKdyGLLuiiHDGnJa9yrgF4iBK8yebmbyV98GqEDVppELyFVForxGrzUPDw05erBkw0Be0Ek8xAw0bBU7ox9Ry9kh14MO2h0DzQcEEboe41yg98gBw2O80Tje040o3CwcEwW2l009ea',
        '__comet_req': '7',
        'fb_dtsg': 'NAcPfVeJ9d7HvXqojIP7P59E8eCfsSta_bbPa3sT3UcXaedoajIb8Qg:17853599968089360:1709829496',
        'jazoest': '26336',
        'lsd': 'UjjAtuGAoPSNcPoz4aJxGJ',
        '__spin_r': '1012081461',
        '__spin_b': 'trunk',
        '__spin_t': '1710504397',
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'PolarisStoriesV3HighlightsPageQuery',
        'variables': '{"first":3,"initial_reel_id":"highlight:'+id+'","last":2,"reel_ids":["highlight:'+id+'"]}',
        'server_timestamps': 'true',
        'doc_id': '24934269819551365',
    }

        response = requests.post('https://www.instagram.com/api/graphql', cookies=self.cookies, headers=self.headers, data=data)
        
        if response.status_code == 200:

            response = response.json()
            if response['extensions']['is_final']:
                reels = {
                    'status': 'ok' if response['extensions']['is_final'] else 'Error',
                    'items': [],
                }

                for reel in response['data']['xdt_api__v1__feed__reels_media__connection']['edges'][0]['node']['items']:
                    reels['items'].append({
                        'id':  reel['id'],
                        'image': reel['image_versions2']['candidates'][0]['url'],
                        'video': reel['video_versions'][0]['url'] if reel['video_versions'] else None,
                    })

                return reels
            else:
                return {
                    'status': response['extensions']['is_final']
                }
        else:
            return {
                'status': response.status_code
            }