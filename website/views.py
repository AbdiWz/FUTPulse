from flask import Blueprint, render_template, flash, request, redirect, url_for, abort
from flask_login import login_required
from .models import GoldPlayers, Icons
from flask_login import current_user

views = Blueprint("views", __name__)

@views.route('/')
@login_required
def home():
    player_data = GoldPlayers.query.limit(8).all()
    icon_data = Icons.query.limit(8).all()
    all_data = player_data + icon_data
    return render_template("home.html", player_data=player_data, icon_data=icon_data, all_data=all_data, current_user=current_user)

@views.route('/player/<string:player_name>')
def player_detail(player_name):
    player = GoldPlayers.query.filter_by(name=player_name).first()
    player_source = "GoldPlayers" if player else "Icons"

    if not player:
        player = Icons.query.filter_by(name=player_name).first()
        if not player:
            abort(404) 

    return_url = url_for('views.gold_view') if player_source == "GoldPlayers" else url_for('views.icon_view')
    return render_template('player_detail.html', player=player, player_source=player_source, return_url=return_url)

@views.route('/golds')
@login_required
def gold_view():
    player_data = GoldPlayers.query.all()
    return render_template("gold.html", player_data=player_data, current_user=current_user)

@views.route('/update_gold/', methods = ['POST'])
def update_gold():
    if request.method == "POST":
        my_data = GoldPlayers.query.get(request.form.get('id'))

        old_values = {field: getattr(my_data, field) for field in my_data.__table__.columns.keys()}

        my_data.rating = request.form['Rating']
        my_data.club = request.form['Club']
        my_data.price = request.form['Price']

        try:
            my_data.validate()
        except ValueError as e:
            print("Error has occurred")
            flash(str(e), 'error')
            return redirect(url_for('views.gold_view'))

        my_data.save()
        new_values = {field: getattr(my_data, field) for field in my_data.__table__.columns.keys()}
        changed_fields = [field for field in new_values.keys() if new_values[field] != old_values[field]]
        detailed_changes = []
        for field in changed_fields:
            detailed_changes.append(f"{field.title()} changed from {old_values[field]} to {new_values[field]}")
        if detailed_changes:
            flash(f"{', '.join(detailed_changes)} for {my_data.name} ")
        else:
            flash(f"No changes made for {my_data.name}.")
        return redirect(url_for('views.gold_view'))

@views.route('/icons')
@login_required
def icon_view():
    icon_data = Icons.query.all()
    return render_template("icons.html", icon_data=icon_data, current_user=current_user)

@views.route('/update_icon/', methods = ['POST'])
def update_icon():
    if request.method == "POST":
        my_data = Icons.query.get(request.form.get('id'))
        old_values = {field: getattr(my_data, field) for field in my_data.__table__.columns.keys()}
        my_data.rating = request.form['Rating']
        my_data.club = request.form['Club']
        my_data.price = request.form['Price']

        try:
            my_data.validate()
        except ValueError as e:
            print("Error has occurred")
            flash(str(e), 'error')
            return redirect(url_for('views.icon_view'))

        my_data.save()
        new_values = {field: getattr(my_data, field) for field in my_data.__table__.columns.keys()}
        changed_fields = [field for field in new_values.keys() if new_values[field] != old_values[field]]
        detailed_changes = []
        for field in changed_fields:
            detailed_changes.append(f"{field.title()} changed from {old_values[field]} to {new_values[field]}")
        if detailed_changes:
            flash(f"{', '.join(detailed_changes)} for {my_data.name} ")
        else:
            flash(f"No changes made for {my_data.name}.")
        return redirect(url_for('views.icon_view'))

