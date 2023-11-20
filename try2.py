import latex2mathml.converter as conv
import mammoth
import re
import json
import base64

def convert_image(image):
    with image.open() as image_bytes:
        encoded_src = base64.b64encode(image_bytes.read()).decode("ascii")

    return {
        "src": "data:{0};base64,{1}".format(image.content_type, encoded_src)
    }


def docx_to_html(path):
    try:
        with open(path, "rb") as docx:
            result = mammoth.convert_to_html(docx)
            html = result.value
        return html
    except Exception as e:
        return None

def add_html_codes(input_data):
    pattern = r'( {6,})'
    underline_pattern = r'\[(\d+)\s+(.*?)\]'
    square_pattern_1 = r'&lt;\[(.*?)\]&gt;'
    square_pattern_2 = r'#\[(.*?)\]#'
    align_pattern = r'&lt;s&gt;(.*?)&lt;/s&gt;'
    img_pattern = r'<p>[ \t]*[<strong>]?<img\s+src=\"(.*?)\"[ ]?/>'
    mml_pattern = r'\$ ?(.*?[^\\]) ?\$'
    
    def convert_to_mml(latex):
        latex = re.sub(r'<.*?>', "", latex)
        latex = latex.replace('&amp;', '&')
        latex = latex.replace('&lt;', '<')
        latex = latex.replace('&gt;', '>')
        latex = latex.replace("&quot", '"')
        mathml_output = conv.convert(latex)
        return mathml_output
    
    def replace_spaces(match):
        return '&nbsp;' * len(match.group(1))

    def replace_with_squares(match):
        extracted_text = match.group(1)
        ending_tag = ''
        if len(extracted_text) > 2:
            ending_tag = '<br>' 
            
        return f"<span class='squareBoxQuestion'>{extracted_text}</span>" + ending_tag

    def replace_with_spaces(match):
        return ('&nbsp;' * 30) + match.group(1)
    
    def convert_table_to_htmlTable(data):
        data = re.sub(r'/e(.*?)/e', r'\1', data) 
        return data.replace('<table>', "<table class='extractedDataTable'>")
    
    def replace_with_S3_url(match):
        img_src = match.group(1)
        img_src = img_src.replace('&nbsp;', ' ')
        img_src = img_src.replace('&#43;', '+')
        img_src = img_src.replace('<br>', '//b')
        img_src = img_src.replace('nbsp;', '')
        return f"<img src='{img_src}' alt=''>" # TODO: Put S3 URL in image src.
    
    try:
        input_data = re.sub(mml_pattern, lambda match: convert_to_mml(match.group(1)), input_data)
    except Exception as e:
        print("Error in add_html_codes: ", e)
        
    
    # for key, value in self.unicode_dict.items():
    #     input_data = input_data.replace(key.lower(), value)
    
    # input_data = re.sub(img_pattern, replace_with_S3_url, input_data)
    
    return input_data


html = mammoth.convert_to_html("Algorithm_Project_Report.docx", convert_image=mammoth.images.img_element(convert_image))
html = add_html_codes(html.value)
print(html)
with open("output2.html", "w") as f:
    f.write("""
            <html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Streamlit App</title>
  <style>
    body {
      font-family: 'Arial', sans-serif;
      margin: 20px;
    }

    h1 {
      color: #0066cc;
    }

    p {
      line-height: 1.5;
    }

    strong {
      color: #0066cc;
    }

    /* Optional: Add some spacing between sections */
    h1 + p {
      margin-top: 10px;
    }

    /* Optional: Add a border to the appendix section */
    h1:last-of-type + p {
      border-top: 1px solid #ccc;
      padding-top: 10px;
    }

    /* Optional: Style the date in a different color */
    p:nth-child(2) {
      color: #888;
    }
  </style>
</head>
<body>""")
    f.write(html)
    f.write("</body></html>")
