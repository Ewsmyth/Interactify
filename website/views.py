from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash, jsonify, make_response, send_file
from flask_login import login_required, current_user
from website.models import User, Post, Follow, Comment, Like
from website import db
import os

views = Blueprint('views', __name__)
processed_requests = set()

@views.route('/home')
@login_required
def home():
    followed_posts = current_user.get_followed_posts()
    liked_post_ids = [like.post_id for like in current_user.likes]
    return render_template('home.html', followed_posts=followed_posts)

@views.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    viewed_user = User.query.get(user_id)
    if viewed_user:
        is_own_profile = (current_user.id == viewed_user.id)
        user_posts = Post.query.filter_by(author_id=user_id).order_by(Post.created_at.desc()).all()
        number_of_posts = viewed_user.post_count()
        number_of_followers = viewed_user.followers_count()
        number_of_following = viewed_user.following_count()

        if not viewed_user.bio:
            viewed_user.bio = f"About {viewed_user.firstname} {viewed_user.lastname}"

        return render_template('profile.html', user_posts=user_posts, viewed_user=viewed_user, is_own_profile=is_own_profile, number_of_posts=number_of_posts, number_of_followers=number_of_followers, number_of_following=number_of_following, posts=user_posts)

    flash('User not found', 'error')
    return redirect(url_for('views.home'))

@views.route('/accountsettings', methods=['GET', 'POST'])
@login_required
def accountsettings():

    viewed_user = User.query.get(current_user.id)

    if request.method == 'POST':
        new_bio = request.form.get('new_bio')
        new_profile_picture = request.files.get('new_profile_picture')
        new_username = request.form.get('new_username')
        new_firstname = request.form.get('new_firstname')
        new_lastname = request.form.get('new_lastname')
        new_gender = request.form.get('new_gender')

        user = User.query.get(current_user.id)

        if new_bio or new_bio == '':  # Check if new_bio is provided or empty
            user.bio = new_bio if new_bio != '' else f"About {user.firstname} {user.lastname}"  # Set new bio or default bio

        if new_username:
            user.username = new_username

        if new_firstname:
            user.firstname = new_firstname

        if new_lastname:
            user.lastname = new_lastname

        if new_gender:
            user.gender = new_gender

        if new_profile_picture:
            try:
                user.save_profile_picture(new_profile_picture, current_app.config['UPLOAD_FOLDER'])
            except ValueError as e:
                flash(str(e))
                return redirect(url_for('views.accountsettings'))

        db.session.commit()

        return redirect(url_for('views.profile', user_id=current_user.id))

    return render_template('accountsettings.html', viewed_user=viewed_user)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    query = request.args.get('query')
    search_results = User.query.filter(User.username.ilike(f"%{query}%")).all() if query else []
    return render_template('search.html', search_results=search_results)

@views.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        post_content = request.form.get('post_content')
        media_file = request.files.get('media_file')

        if post_content or media_file:
            if media_file:
                if media_file.mimetype.startswith('image/'):
                    upload_folder = current_app.config['UPLOAD_FOLDER']
                    image_post = Post(author_id=current_user.id, post_type='image')
                    try:
                        image_post.author = current_user
                        image_post.save_image(media_file, upload_folder)  # Use 'media_file' here
                        db.session.add(image_post)
                    except ValueError as e:
                        return render_template('error.html', error=str(e))

                elif media_file.mimetype.startswith('video/'):
                    upload_folder = current_app.config['UPLOAD_FOLDER']
                    video_post = Post(author_id=current_user.id, post_type='video')
                    try:
                        video_post.author = current_user
                        video_post.save_video(media_file, upload_folder)  # Use 'media_file' here
                        db.session.add(video_post)
                    except ValueError as e:
                        return render_template('error.html', error=str(e))

            if post_content:
                post = Post(author_id=current_user.id, post_type='text', post_content=post_content)
                db.session.add(post)
            
            db.session.commit()  # Move commit outside the condition to handle all posts

            return redirect(url_for('views.home'))

    return render_template('post.html')

@views.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get(post_id)
    if post:
        comments = post.comments.filter_by(type='comment').all()
        like_count = ost.like_count()
        return render_template('post_detail.html', post=post, comments=comments, like_count=like_count)
    return jsonify({'error': 'Post not found'}), 404

@views.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
    user_to_follow = User.query.get(user_id)

    if user_to_follow:
        current_user.follow(user_to_follow)
        db.session.commit()

    return redirect(url_for('views.profile', user_id=user_id))

@views.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    user_to_unfollow = User.query.get(user_id)

    if user_to_unfollow:
        current_user.unfollow(user_to_unfollow)
        db.session.commit()

    return redirect(url_for('views.profile', user_id=user_id))

@views.route('/profileStats/<int:user_id>')
@login_required
def profile_stats(user_id):
    viewed_user = User.query.get(user_id)
    if viewed_user:
        user = viewed_user

        followers = viewed_user.followers.all()
        following = viewed_user.following.all()

        return render_template('profile_stats.html', user=user, viewed_user=viewed_user, followers=followers, following=following)
    
    flash('User not found', 'error')
    return redirect(url_for('views.home'))

@views.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post_to_like = Post.query.get_or_404(post_id)

    if post_to_like:
        current_user.like(post_to_like.id)
        db.session.commit()

    if 'Referer' in request.headers and 'profile' in request.headers.get('Referer'):
        return redirect(url_for('views.profile', user_id=post_to_like.author_id))
    else:
        return redirect(url_for('views.home'))

@views.route('/unlike/<int:post_id>', methods=['POST'])
@login_required
def unlike_post(post_id):
    post_to_unlike = Post.query.get_or_404(post_id)

    if post_to_unlike:
        current_user.unlike(post_to_unlike)
        like = Like.query.filter_by(user=current_user, post_id=post_id).first()
        if like:
            db.session.delete(like)
            db.session.commit()

    if 'Referer' in request.headers and 'profile' in request.headers.get('Referer'):
        return redirect(url_for('views.profile', user_id=post_to_unlike.author_id))
    else:
        return redirect(url_for('views.home'))

@views.route('/submit_comment/<int:post_id>', methods=['POST'])
@login_required
def submit_comment(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post:
        comment_content = request.form.get('comment_content')
        
        if comment_content:
            new_comment = Comment(author_id=current_user.id, post_id=post_id, comment_content=comment_content)
            db.session.add(new_comment)
            db.session.commit()

            if 'Referer' in request.headers and 'profile' in request.headers.get('Referer'):
                return redirect(url_for('views.profile', user_id=post.author_id))
            else:
                return redirect(url_for('views.home'))

        else:
            return render_template('error.html', error='Comment content is missing'), 400

    else:
        return render_template('error.html', error='Post not found'), 404

@views.route('/delete_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if comment:
        post_owner_id = comment.post.author_id
        if current_user.id == comment.author_id or current_user.id == post_owner_id:
            db.session.delete(comment)
            db.session.commit()

    if 'Referer' in request.headers and 'profile' in request.headers.get('Referer'):
        return redirect(url_for('views.profile', user_id=post_owner_id))
    else:
        return redirect(url_for('views.home'))

@views.route('/get_comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post:
        comments = Comment.query.filter_by(post_id=post_id).all()
        comments_data = [{'comment_content': comment.comment_content} for comment in comments]
        
    return render_template('home.html', followed_posts=followed_posts)

@views.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)

    if post_to_delete:
        # Check if the current user is the author of the post
        if current_user.id == post_to_delete.author_id:
            # Delete associated likes and comments
            Like.query.filter_by(post_id=post_id).delete()
            Comment.query.filter_by(post_id=post_id).delete()

            db.session.delete(post_to_delete)
            db.session.commit()
            flash('Post deleted successfully', 'success')
        else:
            flash('You are not authorized to delete this post', 'error')

    return redirect(url_for('views.home'))  # Redirect to the homepage or any desired page after deletion

@views.route('/media/<path:filename>')
def get_media(filename):
    media_folder = '/var/lib/docker/volumes/interactify_userposts/_data/'
    file_path = os.path.join(media_folder, filename)

    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "File not found", 404