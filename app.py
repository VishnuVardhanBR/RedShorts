import argparse
import time
from get_posts import get_top_video_post
from download_video import download_reddit_video
from upload import upload_helper
import os
def main(subreddit_name, number_of_runs, delay_minutes):
    for _ in range(number_of_runs):
        post_details = get_top_video_post(subreddit_name)
        if post_details:
            print(f"Fetched post: \ntitle: {post_details['title']}\nsubreddit: {post_details['subreddit']}\nurl: {post_details['url']}\n")
            video_params = {
                'file': '',
                'title': post_details['title'],
                'description': '',
                'category': '22',
                'keywords': '',
                'privacyStatus': 'public'
            }

            downloaded_video_path = download_reddit_video(post_details['url'])
            print(f"Download successful:\n {downloaded_video_path[1]}\n")

            if downloaded_video_path[0] == 'success':
                video_params['file'] = downloaded_video_path[1]
                upload_helper(video_params)
            elif downloaded_video_path[0] == 'skip':
                print("Video length greater than 1 minute, skipped upload")
            else:
                print("Download error")

            if os.path.exists(downloaded_video_path[1]):
                os.remove(downloaded_video_path[1])
                print("Deleted local video successfully")

        print("Waiting")
        if(_ != number_of_runs-1):
            time.sleep(delay_minutes * 60)  # Convert delay to seconds and wait

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reddit Video Uploader")
    parser.add_argument("--subreddit", default= "0", help="Name of the subreddit")
    parser.add_argument("--number", type=int, required=True, help="Number of times to run the code")
    parser.add_argument("--delay", type=int, default=3, help="Delay between running the code in minutes")

    args = parser.parse_args()
    main(args.subreddit, args.number, args.delay)
