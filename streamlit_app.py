import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
from PIL import Image
import urllib.request
import time
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def image1(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "Made in ",
        image1('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
               width=px(25), height=px(25)),
        " with ❤️ by ",
        link("https://www.linkedin.com/in/rishibajargan/", "Rishi Bajargan"),
        " and ",
        link("https://www.linkedin.com/in/tusharmehtani/", "Tushar Mehtani"),
    ]
    layout(*myargs)


st.title('Invoice Extraction')

with st.form(key='my_form'):
    image = st.file_uploader(label='Upload invoice image')
    submit_button = st.form_submit_button(label='Submit')

st.subheader(" Choose from the demo images for quick view")
with st.form(key='my_form_2'):
    urllib.request.urlretrieve(
        'https://raw.githubusercontent.com/sherlocked27/invoice_streamlit/main//images/demo/inv-1.jpg',
        "inv-1.jpg")
    image_demo1 = Image.open(
        "inv-1.jpg")
    urllib.request.urlretrieve(
        'https://raw.githubusercontent.com/sherlocked27/invoice_streamlit/main//images/demo/inv-2.png',
        "inv-2.png")
    image_demo2 = Image.open(
        "inv-2.png")
    urllib.request.urlretrieve(
        'https://raw.githubusercontent.com/sherlocked27/invoice_streamlit/main//images/demo/inv-3.png',
        "inv-3.png")
    image_demo3 = Image.open(
        "inv-3.png")
    col1, col2, col3 = st.columns(3)
    submit_button_2 = col1.form_submit_button(label='Use Demo 1')
    submit_button_3 = col2.form_submit_button(label='Use Demo 2')
    submit_button_4 = col3.form_submit_button(label='Use Demo 3')


if submit_button_2:
    image = image_demo1
    submit_button = True

if submit_button_3:
    image = image_demo2
    submit_button = True

if submit_button_4:
    image = image_demo3
    submit_button = True

if submit_button:
    print(type(image))
    coll1, coll2 = st.columns(2)
    coll1.header("Invoice")
    coll1.image(image)

    coll2.header("Result")
    coll2.image(image)
    st.subheader("JSON Response")
    st.write({"words": {"buyer_address": "Survey # 78/10, A-2-0 Chikkajala Village A2 Bellary Road  Bengaluru, Karnataka, 562157  India", "buyer_gstin": "29AAACL9861H1Z2", "buyer_name": "India Private Limited", "invoice_date": "2/6/2020", "supplier_address": "Address: 3/8 Ground Floor, Opp. MG Infant School, Kodichikkanahalli Road, Bilekahalli,", "supplier_name": "HAPPY EARTH ENTERPRISES",
                        "supplier_email": "orders@happyearth.in"}, "bbox": {"buyer_address": [238, 1248, 1418, 1595], "buyer_gstin": [450, 1665, 1035, 1761], "buyer_name": [747, 1165, 1361, 1262], "invoice_date": [118, 632, 436, 741], "supplier_address": [2671, 290, 3943, 476], "supplier_name": [2718, 198, 3784, 301], "supplier_email": [3280, 540, 3939, 649]}, "width": 4134, "height": 5847})
footer()
# Add a placeholder
# latest_iteration = st.empty()
# bar = st.progress(0)

# for i in range(100):
#     # Update the progress bar with each iteration.
#     latest_iteration.text(f'Iteration {i+1}')
#     bar.progress(i + 1)
#     time.sleep(0.1)
