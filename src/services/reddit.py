from typing import List

import praw
from langchain.schema import Document


class RedditClient:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit_client = praw.Reddit(
            client_id=client_id, client_secret=client_secret, user_agent=user_agent
        )
        self.reddit_search_client = self.reddit_client.subreddit("godot").search

    def search_with_query(
        self, query: str, sort: str = "relevance", limit: int = 10
    ) -> List[Document]:
        """Search for posts relevant to query.

        Args:
            query (str): The search query.
            sort (str): Select one of "relevance", "hot", "top", "new", or "comments"

        Returns:
            List[Documents]: _description_
        """
        all_posts = []
        posts = self.reddit_search_client(
            query,
            sort=sort,
            time_filter="all",
            limit=limit,
        )

        for post in posts:
            title = f"# {post.title}\n"
            content = post.selftext
            comments = "\n".join(
                [
                    f"**Comment {i+1}:**\n{comment.body}"
                    for i, comment in enumerate(post.comments)
                ]
            )
            metadata = {
                "author": post.author,
                "score": post.score,
                "upvote_ratio": post.upvote_ratio,
                "num_comments": post.num_comments,
            }
            all_posts.append(
                Document(page_content=title + content + comments, metadata=metadata)
            )

        return all_posts
