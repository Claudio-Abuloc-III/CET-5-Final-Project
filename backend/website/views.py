from flask import Blueprint, render_template, request, flash, redirect, url_for,abort, current_app, jsonify
from flask_login import login_required, current_user
from .models import Post, Discussions, IMG, UserDiscussionVote, Comment
from . import db
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
import os

views = Blueprint('views', __name__)

UPLOAD_FOLDER = r'backend\website\static\images\UPLOADED IMG'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/')
def home():
    return render_template("Homepage.html", user=current_user)

@views.route('/start-recycling-categories')
def SRCategories():
    return render_template("SRCategories.html", user=current_user)


@views.route('/start-recycling-plastic')
def SRPlastic():
    return render_template("SR-Plastic.html", user=current_user)

@views.route('/start-recycling-paper')
def SRPaper():
    return render_template("SR-Paper.html", user=current_user)

@views.route('/start-recycling-textile')
def SRTextile():
    return render_template("SR-Textile.html", user=current_user)

@views.route('/start-recycling-glass')
def SRGlass():
    return render_template("SR-Glass.html", user=current_user)

@views.route('/forum')
def forum():
    discussions = Discussions.query.all()
    return render_template("Forum.html", user=current_user, discussions=discussions)

@views.route('/createForum', methods=['GET', 'POST'])
@login_required
def forumClicked():
    if request.method == "POST":
        dTitle = request.form.get('discussionTitle')
        dDescription = request.form.get('discussionDescription')
        pic = request.files['pic']

        if not all([dTitle, dDescription]):
            flash('Please fill up all the required forms', category='error')
        elif len(dTitle) > 70:
            flash('Title reached maximum limit of characters', category='error')
        elif pic and allowed_file(pic.filename):
            try:
                filename = secure_filename(pic.filename)
                mimetype = pic.mimetype

                # Save the file to the designated folder
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                pic.save(file_path)

                # Save the filename to the database
                new_image = IMG(img_filename=file_path, name=filename, mimetype=mimetype, user_id=current_user.id)
                db.session.add(new_image)
                db.session.commit()

                # Create a new discussion associated with the uploaded image
                new_discussion = Discussions(
                    dTitle=dTitle, 
                    dDescription=dDescription,
                    user_id=current_user.id,
                    image_id=new_image.id
                )
                db.session.add(new_discussion)
                db.session.commit()

                flash('Discussion created!', category='success')
                return redirect(url_for('views.forumPost', discussion_id=new_discussion.id))
                
            except IntegrityError as e:
                db.session.rollback()
                if 'UNIQUE constraint failed: img.img' in str(e):
                    flash('Image file name is not unique', category='error')
                else:
                    flash('An error occurred during discussion creation', category='error')

    return render_template("Create-Forum.html", user=current_user)


@views.route('/Discussion/<int:discussion_id>')
def forumPost(discussion_id):
    discussion_data = Discussions.query.get(discussion_id)

    if not discussion_data:
        abort(404)

    return render_template("Forum-Clicked.html", user=current_user, discussion_data=discussion_data)

@views.route('/like_dislike/<int:discussion_id>', methods=['POST'])
@login_required
def like_dislike(discussion_id):
    discussion = Discussions.query.get(discussion_id)

    if not discussion:
        return jsonify({'error': 'Discussion not found'}), 404

    is_like = request.json.get('is_like')

    if is_like is None:
        return jsonify({'error': 'Invalid request'}), 400

    # Check if the user has already voted on this discussion
    existing_vote = UserDiscussionVote.query.filter_by(user_id=current_user.id, discussion_id=discussion_id).first()

    try:
        if existing_vote:
            # If the user has already voted, update their vote only if the new vote is different
            if existing_vote.is_like != is_like:
                existing_vote.is_like = is_like
            else:
                # If the user votes the same as their previous vote, remove the vote
                db.session.delete(existing_vote)
        else:
            # If the user hasn't voted, create a new vote
            new_vote = UserDiscussionVote(user_id=current_user.id, discussion_id=discussion_id, is_like=is_like)
            db.session.add(new_vote)

        # Update the discussion likes and dislikes count
        discussion.likes = UserDiscussionVote.query.filter_by(discussion_id=discussion_id, is_like=True).count()
        discussion.dislikes = UserDiscussionVote.query.filter_by(discussion_id=discussion_id, is_like=False).count()

        db.session.commit()

        return jsonify({'likes': discussion.likes, 'dislikes': discussion.dislikes}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': 'Failed to update like/dislike'}), 500

@views.route('/submit_comment/<int:discussion_id>', methods=['POST'])
@login_required
def submit_comment(discussion_id):
    try:
        # Get the comment text from the request
        comment_text = request.form.get('commentText')

        # Validate the comment text (you can add more validation if needed)

        # Create a new comment associated with the discussion
        new_comment = Comment(
            text=comment_text,
            user_id=current_user.id,
            discussion_id=discussion_id
        )
        db.session.add(new_comment)
        db.session.commit()

        # Return a success message
        return jsonify({'message': 'Comment submitted successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to submit comment'}), 500

@views.route('/post')
@login_required
def post():
    return render_template("Post-page.html", user=current_user) 

@views.route('/login')
def login():
    return render_template("Login.html", user=current_user)

@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def CreatePost():
    if request.method == "POST":
        category = request.form.get('chosenCat')
        title = request.form.get('postTitle')
        description = request.form.get('postDescription')
        instruction_title = request.form.get('instructionTitle')
        instruction_description = request.form.get('stepDescription')
        reference = request.form.getlist('references[]')
        pic = request.files['pic']

        if not all([category, title, description, instruction_title, instruction_description, reference]):
            flash('Please fill up all the required forms', category='error')
        elif len(title) > 70:
            flash('Title reached maximum limit of characters', category='error')
        elif len(instruction_title) > 70:
            flash('Instruction title reached maximum limit of characters', category='error')
        elif pic and allowed_file(pic.filename):
            try:
                filename = secure_filename(pic.filename)
                mimetype = pic.mimetype

                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                pic.save(file_path)

                new_image = IMG(img_filename=file_path, name=filename, mimetype=mimetype, user_id=current_user.id)
                db.session.add(new_image)
                db.session.commit()

                new_post = Post(
                    category=category, 
                    title=title,
                    description=description,
                    instruction_title=instruction_title,
                    instruction_description=instruction_description,
                    user_id=current_user.id,
                    image_id=new_image.id)
                db.session.add(new_post)
                db.session.commit()
                flash('Post created!', category='success')
                return redirect(url_for('views.CreatePost'))
            except IntegrityError as e:
                db.session.rollback()
                if 'UNIQUE constraint failed: img.img' in str(e):
                    flash('Image file name is not unique', category='error')
                else:
                    flash('An error occurred during discussion creation', category='error')

    return render_template("Create-Post.html", user=current_user)

@views.route('/account')
@login_required
def account():
    return render_template("Account.html", user=current_user) 