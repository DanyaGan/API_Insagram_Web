# API_Insagram_Web

## About the project
The API_Instagram_Web project is a software toolkit
designed to provide convenient interaction with the Instagram API (Application Programming Interface)
via the web interface. This project includes various features that allow users to perform
Various operations with data available through the Instagram API.

One of the main objectives of the project is to provide access to various
data and functions provided by Instagram through its API. This may include receiving
information about users, their profiles, publications, comments, likes, etc. The project can also
provide functionality for performing various actions, such as publishing new posts,
account management, interaction with subscribers.

## Why it's useful
The API_Instagram_Web project has significant utility due to the ability to anonymously retrieve
information about user profiles. This function has many practical uses and can be
useful for various purposes.

## To work with the project 

```python
import Api_instagram_Web

api = Api_instagram_Web.stalker()

api.user_name = 'instagram'
info = api.get_info_profile()

print(info)
```
```python
import Api_instagram_Web, data

api = Api_instagram_Web.stalker()

api.cookies = data.cookies
api.headers = data.headers_info

api.user_name = 'instagram'
api.user_id = api.get_info_profile()['id']
reel = api.get_reel()

print(reel)
```
