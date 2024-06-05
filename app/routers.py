from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user

from app import db
from app.models import Tender, TenderItem, Bidder, Bid, Award, User, Role
from app.forms import TenderForm, TenderItemForm, BidderForm, BidForm, AwardForm, LoginForm, RegistrationForm, \
    UpdateUserForm

bp = Blueprint('main', __name__)


# Tenders
@bp.route('/')
def tender_list():
    tenders = Tender.query.all()
    return render_template('tender_list.html', tenders=tenders)


@bp.route('/tender/<int:id>')
def tender_detail(id):
    tender = Tender.query.get_or_404(id)
    return render_template('tender_detail.html', tender=tender)


@bp.route('/tender/create', methods=['GET', 'POST'])
def tender_create():
    form = TenderForm()
    if form.validate_on_submit():
        tender = Tender(title=form.title.data, description=form.description.data,
                        start_date=form.start_date.data, end_date=form.end_date.data)
        db.session.add(tender)
        db.session.commit()
        flash('Tender created successfully!', 'success')
        return redirect(url_for('main.tender_list'))
    return render_template('tender_form.html', form=form)


@bp.route('/tender/<int:id>/update', methods=['GET', 'POST'])
def tender_update(id):
    tender = Tender.query.get_or_404(id)
    form = TenderForm(obj=tender)
    if form.validate_on_submit():
        form.populate_obj(tender)
        db.session.commit()
        flash('Tender updated successfully!', 'success')
        return redirect(url_for('main.tender_detail', id=id))
    return render_template('tender_form.html', form=form)


@bp.route('/tender/<int:id>/delete', methods=['GET', 'POST'])
def tender_delete(id):
    tender = Tender.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(tender)
        db.session.commit()
        flash('Tender deleted successfully!', 'success')
        return redirect(url_for('main.tender_list'))
    return render_template('tender_confirm_delete.html', tender=tender)


# TenderItems
@bp.route('/tender/<int:tender_id>/items')
def tenderitem_list(tender_id):
    items = TenderItem.query.filter_by(tender_id=tender_id).all()
    tender = Tender.query.get_or_404(tender_id)
    return render_template('tenderitem_list.html', items=items, tender=tender)


@bp.route('/tender/<int:tender_id>/item/<int:id>')
def tenderitem_detail(tender_id, id):
    item = TenderItem.query.get_or_404(id)
    return render_template('tenderitem_detail.html', item=item)


@bp.route('/tender/<int:tender_id>/item/create', methods=['GET', 'POST'])
def tenderitem_create(tender_id):
    form = TenderItemForm()
    if form.validate_on_submit():
        item = TenderItem(name=form.name.data, description=form.description.data,
                          quantity=form.quantity.data, unit=form.unit.data, tender_id=tender_id)
        db.session.add(item)
        db.session.commit()
        flash('Tender Item created successfully!', 'success')
        return redirect(url_for('main.tenderitem_list', tender_id=tender_id))
    return render_template('tenderitem_form.html', form=form)


@bp.route('/tender/<int:tender_id>/item/<int:id>/update', methods=['GET', 'POST'])
def tenderitem_update(tender_id, id):
    item = TenderItem.query.get_or_404(id)
    form = TenderItemForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash('Tender Item updated successfully!', 'success')
        return redirect(url_for('main.tenderitem_detail', tender_id=tender_id, id=id))
    return render_template('tenderitem_form.html', form=form)


@bp.route('/tender/<int:tender_id>/item/<int:id>/delete', methods=['GET', 'POST'])
def tenderitem_delete(tender_id, id):
    item = TenderItem.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash('Tender Item deleted successfully!', 'success')
        return redirect(url_for('main.tenderitem_list', tender_id=tender_id))
    return render_template('tenderitem_confirm_delete.html', item=item)


# Bidders
@bp.route('/bidders')
def bidder_list():
    bidders = Bidder.query.all()
    return render_template('bidder_list.html', bidders=bidders)


@bp.route('/bidder/<int:id>')
def bidder_detail(id):
    bidder = Bidder.query.get_or_404(id)
    return render_template('bidder_detail.html', bidder=bidder)


@bp.route('/bidder/create', methods=['GET', 'POST'])
def bidder_create():
    form = BidderForm()
    if form.validate_on_submit():
        bidder = Bidder(name=form.name.data, contact_info=form.contact_info.data)
        db.session.add(bidder)
        db.session.commit()
        flash('Bidder created successfully!', 'success')
        return redirect(url_for('main.bidder_list'))
    return render_template('bidder_form.html', form=form)


@bp.route('/bidder/<int:id>/update', methods=['GET', 'POST'])
def bidder_update(id):
    bidder = Bidder.query.get_or_404(id)
    form = BidderForm(obj=bidder)
    if form.validate_on_submit():
        form.populate_obj(bidder)
        db.session.commit()
        flash('Bidder updated successfully!', 'success')
        return redirect(url_for('main.bidder_detail', id=id))
    return render_template('bidder_form.html', form=form)


@bp.route('/bidder/<int:id>/delete', methods=['GET', 'POST'])
def bidder_delete(id):
    bidder = Bidder.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(bidder)
        db.session.commit()
        flash('Bidder deleted successfully!', 'success')
        return redirect(url_for('main.bidder_list'))
    return render_template('bidder_confirm_delete.html', bidder=bidder)


# Bids
@bp.route('/tender/<int:tender_id>/bids')
def bid_list(tender_id):
    bids = Bid.query.filter_by(tender_id=tender_id).all()
    tender = Tender.query.get_or_404(tender_id)
    return render_template('bid_list.html', bids=bids, tender=tender)


@bp.route('/tender/<int:tender_id>/bid/<int:id>')
def bid_detail(tender_id, id):
    bid = Bid.query.get_or_404(id)
    return render_template('bid_detail.html', bid=bid)


@bp.route('/tender/<int:tender_id>/bid/create', methods=['GET', 'POST'])
def bid_create(tender_id):
    form = BidForm()
    form.bidder.choices = [(bid.id, bid.name)
                           for bid in Bidder.query.all()]
    if form.validate_on_submit():
        bidder_id = int(form.bidder.data)

        bid = Bid(price=form.price.data, terms=form.terms.data, tender_id=tender_id, bidder_id=bidder_id)
        db.session.add(bid)
        db.session.commit()
        flash('Bid created successfully!', 'success')
        return redirect(url_for('main.bid_list', tender_id=tender_id))
    return render_template('bid_form.html', form=form)


@bp.route('/tender/<int:tender_id>/bid/<int:id>/update', methods=['GET', 'POST'])
def bid_update(tender_id, id):
    bid = Bid.query.get_or_404(id)

    form = BidForm()
    form.bidder.choices = [(bid.id, bid.name)
                           for bid in Bidder.query.all()]

    if form.validate_on_submit():
        bidder_id = int(form.bidder.data)

        bid.price = form.price.data
        bid.terms = form.terms.data
        bid.bidder_id = bidder_id

        db.session.commit()
        flash('Bid updated successfully!', 'success')
        return redirect(url_for('main.bid_detail', tender_id=tender_id, id=id))
    form.price.data = bid.price
    form.terms.data = bid.terms
    form.bidder.data = str(bid.bidder_id)
    return render_template('bid_form.html', form=form)


@bp.route('/tender/<int:tender_id>/bid/<int:id>/delete', methods=['GET', 'POST'])
def bid_delete(tender_id, id):
    bid = Bid.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(bid)
        db.session.commit()
        flash('Bid deleted successfully!', 'success')
        return redirect(url_for('main.bid_list', tender_id=tender_id))
    return render_template('bid_confirm_delete.html', bid=bid)


# Awards
@bp.route('/tender/<int:tender_id>/awards')
def award_list(tender_id):
    awards = Award.query.filter_by(tender_id=tender_id).all()
    tender = Tender.query.get_or_404(tender_id)
    return render_template('award_list.html', awards=awards, tender=tender)


@bp.route('/tender/<int:tender_id>/award/<int:id>')
def award_detail(tender_id, id):
    award = Award.query.get_or_404(id)
    return render_template('award_detail.html', award=award)


@bp.route('/tender/<int:tender_id>/award/create', methods=['GET', 'POST'])
def award_create(tender_id):
    form = AwardForm()
    if form.validate_on_submit():
        award = Award(price=form.price.data, terms=form.terms.data, tender_id=tender_id)
        db.session.add(award)
        db.session.commit()
        flash('Award created successfully!', 'success')
        return redirect(url_for('main.award_list', tender_id=tender_id))
    return render_template('award_form.html', form=form)


@bp.route('/tender/<int:tender_id>/award/<int:id>/update', methods=['GET', 'POST'])
def award_update(tender_id, id):
    award = Award.query.get_or_404(id)
    form = AwardForm(obj=award)
    if form.validate_on_submit():
        form.populate_obj(award)
        db.session.commit()
        flash('Award updated successfully!', 'success')
        return redirect(url_for('main.award_detail', tender_id=tender_id, id=id))
    return render_template('award_form.html', form=form)


@bp.route('/tender/<int:tender_id>/award/<int:id>/delete', methods=['GET', 'POST'])
def award_delete(tender_id, id):
    award = Award.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(award)
        db.session.commit()
        flash('Award deleted successfully!', 'success')
        return redirect(url_for('main.award_list', tender_id=tender_id))
    return render_template('award_confirm_delete.html', award=award)


@bp.route('/login/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.tender_list'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username ==
                                             form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.tender_list'))
        flash("Invalid username/password", 'error')
        return redirect(url_for('main.login'))
    return render_template('login.html', form=form)


@bp.route('/registration/', methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.tender_list'))
    form = RegistrationForm()
    if form.validate_on_submit():
        role_id = db.session.query(Role).filter(Role.name == 'Користувач').first().id
        user = User(
            username=form.username.data,
            role_id=role_id
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.tender_list'))
    return render_template('registration.html', form=form)


@bp.route('/logout/')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('main.tender_list'))
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.tender_list'))


@bp.route('/admin/')
def admin():
    # if not current_user.is_authenticated or current_user.role.name != 'Адміністратор':
    #     return redirect(url_for('main.tender_list'))

    users = User.query.filter(~User.role.has(name='Адміністратор')).all()
    return render_template('admin.html', users=users)


@bp.route('/admin/user/<int:id>/update/', methods=['POST', 'GET'])
def user_update(id):
    # if not current_user.is_authenticated or current_user.role.name != 'Адміністратор':
    #     return redirect(url_for('main.tender_list'))

    user = db.session.query(User).get_or_404(id)
    form = UpdateUserForm()

    form.role.choices = [(role.id, f'{role.name}')
                         for role in Role.query.all()]

    if form.validate_on_submit():
        role_id = int(form.role.data)
        user.username = form.username.data
        user.role_id = role_id
        db.session.commit()

        return redirect(url_for('main.admin'))

    form.username.data = user.username
    form.role.data = str(user.role_id)
    return render_template('user_update.html', form=form)


@bp.route('/admin/user/<int:id>/delete/', methods=['POST', 'GET'])
def user_delete(id):
    # if not current_user.is_authenticated or current_user.role.name != 'Адміністратор':
    #     return redirect(url_for('main.tender_list'))

    user = db.session.query(User).get_or_404(id)

    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
        return redirect(url_for('main.admin'))
    return render_template('user_confirm_delete.html', user=user)

