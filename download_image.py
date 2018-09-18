import re
import requests
import requests.auth
import datetime
import yaml


secret = ''
client_id = ''
password = ''
username = ''

with open("passwords.yml", 'r') as stream:
    data_loaded=yaml.load(stream)
    secret = data_loaded['secret']
    client_id = data_loaded['client_id']
    password = data_loaded['password']
    username = data_loaded['username'] 



client_auth = requests.auth.HTTPBasicAuth(client_id,secret)
post_data = {"grant_type":"password","username":username,"password":password}
headers = {"User-Agent":"picture_browser"}

response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
response_dict = response.json()
access_token = 'bearer '+ response_dict['access_token']


#now lets start accessing some of the data that we have set up to grant acess to 
access_headers = {"Authorization":access_token,"User-Agent":"picture_browser"}


response=requests.get('https://oauth.reddit.com/r/EarthPorn/top/',headers=access_headers)

#now lets try and start looking at the html and see if we can pull out some of the pictures
date_string = str(datetime.datetime.now())[0:10]+'_'

def get_image(number_in_page):

    image = response.json()['data']['children'][number_in_page]['data']['preview']['images'][0]['source']
    
    width = image['width']
    height =image['height']
    url = image['url']

    height_setting = 1440 
    width_setting = 2560 
    image_name = re.search('.*.jpg',url).group(0)
    
    d = response.json()['data']['children'][number_in_page]['data']['preview']['images']
    

    if height>height_setting and width>width_setting:
        print('successful size')
        image_request = requests.get(url, stream=True)
        with open(str(date_string+str(number_in_page)+'.jpg'),'wb') as imagefile:
            for chunk in image_request:
                imagefile.write(chunk)
    else:
        print('failed')
        print('height: '+str(height),'width: '+ str(width))
 

for i in range(25):
    get_image(i)

print('done')
