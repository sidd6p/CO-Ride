from flask import render_template, url_for, redirect, Blueprint
from flaskFile.models import UserReviews
from flask_login import login_required
from flaskFile.feedback.forms import MyFeedback

feedback = Blueprint('feedback', __name__)

@feedback.route('/my-feedback',  methods=['GET', 'POST'])
@login_required
def myFeedback():
    return redirect(url_for('main.error'))
    # form = MyFeedback()
    # userFeedback = UserReviews.query.filter_by(author = current_user).first()
    # if form.validate_on_submit():
    #     if userFeedback != None:
    #         userFeedback.title = form.title.data
    #         userFeedback.content = form.title.data
    #         userFeedback.dateOfReview = form.date.data
    #         db.session.commit()
    #         flash("Thank you for the Feedback!", "info")
    #     else:      
    #         userReview = UserReviews(title=form.title.data, content=form.content.data, author=current_user)
    #         db.session.add(userReview)
    #         db.session.commit()
    #         flash("Thank you for the Feedback!", "info")
    #     return redirect(url_for('feedback.allFeedback'))
    # elif request.method == 'GET' and userFeedback:
    #     form.title.data = userFeedback.title
    #     form.content.data = userFeedback.content
    # return render_template('my-feedback.html', title="My Feedback", form=form)

@feedback.route('/all-feedback')
def allFeedback():
    feedbacks = UserReviews.query.all()
    return render_template('all-feedbacks.html', title="All Feedbacks", feedbacks=feedbacks)

