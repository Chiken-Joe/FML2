import pytest
from asserts.response_asserts import ResponseAsserts as RA
from asserts.model_asserts import StatsAsserts

def test_stats_initial(stats_client):
    response = stats_client.get_stats()
    RA.assert_status(response, 200)
    data = response.json()
    StatsAsserts.assert_stats(data)
    assert data["total_users"] == 0
    assert data["total_posts"] == 0
    assert data["total_comments"] == 0
    assert data["most_common_reaction"] == "N/A"
    assert data["most_active_procrastinator"] == "N/A"
    assert data["average_comments_per_post"] == 0.0

def test_stats_after_creating_user(stats_client, create_user):
    initial = stats_client.get_stats().json()
    user_id, user_data = create_user
    response = stats_client.get_stats()
    RA.assert_status(response, 200)
    data = response.json()
    assert data["total_users"] == initial["total_users"] + 1

def test_stats_after_creating_post(stats_client, create_post):
    initial = stats_client.get_stats().json()
    post_id, user_id, post_data = create_post
    response = stats_client.get_stats()
    RA.assert_status(response, 200)
    data = response.json()
    assert data["total_posts"] == initial["total_posts"] + 1
    assert data["total_users"] == initial["total_users"]
    assert data["total_comments"] == initial["total_comments"]

def test_stats_after_creating_comment(stats_client, create_post, create_user, random_comment_data):
    from clients.comment_client import CommentClient
    comment_client = CommentClient()
    post_id, owner_id, post_data = create_post
    user_id2, user_data2 = create_user
    initial = stats_client.get_stats().json()
    comment_client.create_comment(post_id, user_id2, random_comment_data["content"])
    response = stats_client.get_stats()
    RA.assert_status(response, 200)
    data = response.json()
    assert data["total_comments"] == initial["total_comments"] + 1
    expected_avg = (initial["average_comments_per_post"] * initial["total_posts"] + 1) / (initial["total_posts"] + 1) if initial["total_posts"] > 0 else 1.0
    assert data["average_comments_per_post"] == expected_avg

def test_stats_with_reactions(stats_client, create_post, create_user):
    post_client = PostClient()
    post_id, owner_id, post_data = create_post
    user2_id, user2_data = create_user
    user3_id, user3_data = create_user
    post_client.react_to_post(post_id, user2_id, "sigh")
    post_client.react_to_post(post_id, user3_id, "sigh")
    user4_id, user4_data = create_user
    post_client.react_to_post(post_id, user4_id, "facepalm")
    response = stats_client.get_stats()
    RA.assert_status(response, 200)
    data = response.json()
    assert data["most_common_reaction"] == "sigh"

def test_stats_most_active_procrastinator(stats_client, create_post, create_user):
    post_client = PostClient()
    comment_client = CommentClient()
    user1_id, user1_data = create_user
    user2_id, user2_data = create_user
    post1 = post_client.create_post(user1_id, "Post1", "Content1")
    post1_id = post1.json()["id"]
    post2 = post_client.create_post(user1_id, "Post2", "Content2")
    post2_id = post2.json()["id"]
    post3 = post_client.create_post(user2_id, "Post3", "Content3")
    post3_id = post3.json()["id"]
    comment_client.create_comment(post1_id, user1_id, "Comment1")
    comment_client.create_comment(post2_id, user1_id, "Comment2")
    comment_client.create_comment(post3_id, user2_id, "Comment3")
    post_client.react_to_post(post1_id, user1_id, "sigh")
    post_client.react_to_post(post2_id, user1_id, "facepalm")
    post_client.react_to_post(post3_id, user2_id, "cringe")
    response = stats_client.get_stats()
    RA.assert_status(response, 200)
    data = response.json()
    assert data["most_active_procrastinator"] == user1_data["username"]