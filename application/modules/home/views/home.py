from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g, jsonify, abort

mod = Blueprint(
    'home',
    __name__,
    template_folder='../templates',
    static_folder='static'
)


@mod.route('/')
def root():
    return render_template("index.html")
