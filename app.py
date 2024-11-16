from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# MySQL configurations
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "obituary_platform"

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        date_of_birth = request.form.get('date_of_birth')
        date_of_death = request.form.get('date_of_death')
        content = request.form.get('content')
        author = request.form.get('author')

        # Check if all fields are filled
        if not all([name, date_of_birth, date_of_death, content, author]):
            return render_template('obituary_form.html', error="All fields are required!")

        # Insert data into the database
        cur = mysql.connection.cursor()
        query = """
            INSERT INTO obituaries (name, date_of_birth, date_of_death, content, author) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(query, (name, date_of_birth, date_of_death, content, author))
        mysql.connection.commit()
        cur.close()

        # Flash success message and redirect to form page
        flash('Form submitted successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('obituary_form.html')

@app.route('/obituaries_list')
def obituaries_list():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM obituaries"
    cur.execute(query)
    obituaries = cur.fetchall()
    cur.close()
    return render_template('obituaries_list.html', obituaries=obituaries)

if __name__ == '__main__':
    app.run(debug=True)
