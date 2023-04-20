from flask import Blueprint, render_template, request, flash, jsonify, Response
from flask_login import login_required, current_user
from fpdf import FPDF
from .models import Todo
from . import db
import json
import io
import csv

todos = Blueprint('todos', __name__)

@todos.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        title = request.form.get('title')#Gets the todo from the HTML 
        description = request.form.get('description')#Gets the todo from the HTML 

        if len(title) < 1:
            flash('Title is too short!', category='warning') 
        elif len(description) < 1:
            flash('Description is too short!', category='warning') 
        else:
            new_todo = Todo(title=title, description=description, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_todo) #adding the note to the database 
            db.session.commit()
            flash('Todo added!', category='success')

    return render_template('home.html',user=current_user)

@todos.route('/delete-todo', methods=['POST'])
@login_required
def delete_todo():
    data = json.loads(request.data)
    todoId = data['noteId']
    todo = Todo.query.get(todoId)

    if todo:
        if todo.user_id == current_user.id:
            db.session.delete(todo)
            db.session.commit()
            return jsonify({})
        

@todos.route('/report-note/pdf')
@login_required
def report_todo_pdf():
    try:
        report = FPDF()
        report.add_page()

        page_width = report.w - 2 * report.l_margin
        col_width = page_width/4
       
        report.set_font('Times','B',14.0)
        report.cell(page_width, 0.0, 'Notes', align='C')
        report.ln(10)
        report.set_font('Courier','',12)
        report.ln(1)

        th = report.font_size

        for todo in current_user.todos:
            report.cell(col_width, th, str(todo.id), border=1)
            report.cell(col_width, th, str(todo.data), border=1)
            report.cell(col_width, th, str(todo.date), border=1)
            report.cell(col_width, th, str(), border=1)
            report.ln(th)
        
        report.ln(10)
        report.set_font('TImes','',10.0)
        report.cell(page_width, 0.0, 'end', align='C')

        return Response(report.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=notes_report.pdf'})

    except Exception as e:
        print(e)

@todos.route('/report-note/csv')
@login_required
def report_note_csv():
    
    try:
        output = io.StringIO()
        report = csv.writer(output)
        #head
        line = ['ID','Data','Date']
        report.writerow(line)

        for note in current_user.todos:
            line = [str(note.id + ',' + note.data + ',' + note.date)]
            report.writerow(line)

        output.seek(0)

        return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=report/notes_report.csv"})

    except Exception as e:
        print(e)

    return render_template('home.html',user=current_user)