import mammoth

def docx_to_html(path):
    try:
        with open(path, "rb") as docx:
            result = mammoth.convert_to_html(docx)
            html = result.value
        return html
    except Exception as e:
        raise e

with open('output.html', 'w') as f:
    f.write(docx_to_html(r'E:\FifthSem\AlgoProject\GeometricAnalyzer\Algorithm_Project_Report.docx'))
    
    