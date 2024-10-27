from website import create_app

app = create_app()

@app.template_filter('comma')
def format_with_commas(value):
    return f"{value:,}"

if __name__ == '__main__':
    app.run(debug=True)