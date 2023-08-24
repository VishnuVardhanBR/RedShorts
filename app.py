from get_posts import get_top_video_post
from scrape import download_reddit_video
from upload import upload_video

subreddit_name = "HumansBeingBros"

# post_details = {
#     "post_id": post.id,
#     "title": post.title,
#     "url": post.url,
#     "date": str(datetime.datetime.now()),
#     "upvotes": post.score
# }

# get top reddit post
post_details = get_top_video_post(subreddit_name)
if(post_details):
    video_params = {
        'file': post_details['title'],
        'title': '',
        'description': '',
        'category': '22',
        'keywords': '',
        'privacyStatus': 'public'
    }
    print(video_params)


    #download video
    downloaded_video_path = download_reddit_video(post_details['url'])
    print(downloaded_video_path)

    if(downloaded_video_path != 'error'):
        video_params['file'] = downloaded_video_path[1]
        upload_video(video_params)
    else:
        print("Download Error")
