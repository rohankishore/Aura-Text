def generate_python_template():
    template = f'''\
    
    # Welcome to Aura Text
    
def main():
    pass

if __name__ == "__main__":
    main()
'''
    return template


def generate_html_template(title="Welcome to Aura Text"):
    template = f'''\
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
'''
    return template


def generate_java_template(class_name):
    template = f'''\
public class {class_name} {{
    public static void main(String[] args) {{

    }}
}}
'''
    return template


def generate_php_template():
    template = '<?php\n\n?>'
    return template


def generate_tex_template(title="Welcome to Aura Text"):
    template = f'''\
\\documentclass{{article}}
\\title{{{title}}}
\\begin{{document}}
\\maketitle

Hello, World!

\\end{{document}}
'''
    return template


def generate_cpp_template():
    template = f'''\
#include <iostream>

int main() {{

    cout << "Welcome to Aura Text!";
    return 0;
}}
'''
    return template