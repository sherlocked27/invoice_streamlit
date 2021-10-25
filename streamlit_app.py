import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
from PIL import Image, ImageFont, ImageDraw
import urllib.request
import time
import requests
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb
st.set_page_config(
    page_title="Invoice Magic",
    page_icon="🪄",
    menu_items={
        'About': "### This is an *extremely* cool app! Look at footer to contact :)"
    }
)


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
        "Made in Streamlit",
        # image1('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
        #        width=px(25), height=px(25)),
        " with ❤️ by ",
        link("https://www.linkedin.com/in/rishibajargan/", "Rishi Bajargan"),
        " and ",
        link("https://www.linkedin.com/in/tusharmehtani/", "Tushar Mehtani"),
    ]
    layout(*myargs)


def load_model():
    gif1_path = "./images/processing.gif"
    placeholder1 = st.empty()
    col11, col21, col31 = placeholder1.columns([4, 5, 4])

    with col11:
        st.write("")

    with col21:
        st.image(
            gif1_path, caption="Loading model, just a min! We can't have it running 24/7, Please bear ... :)")

    with col31:
        st.write("")

    # Initial Call to Start Servers !
    url = "https://q3d0rlossg.execute-api.us-east-1.amazonaws.com/default/invoiceContainer"
    payload = ""
    headers = {
        'x-api-key': '4KQfn4znnK8caRlTklZrFcUNNJvB6oFuWFKF4dh0',
        'Content-Type': 'text/plain'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    time.sleep(2)
    placeholder1.empty()
    return


def save_labelled(ans):
    new_image = Image.open("input.jpg")
    img1 = ImageDraw.Draw(new_image)
    width, height = new_image.size
    to_add = [width*0.0042,  height*0.0042]

    for k, v in ans["bbox"].items():
        img1.rectangle(v, outline="green", width=3)
        myFont = ImageFont.truetype(
            './FreeMono.ttf', 20)
        img1.text((v[0]-to_add[0]*6, v[1] - to_add[1]*6),
                  k, font=myFont, fill=(255, 0, 0))
    return new_image


st.title('Invoice Extraction')
footer()
if 'load_model' not in st.session_state:
    st.session_state.load_model = True

if(st.session_state.load_model == True):
    load_model()
    st.session_state.load_model = False
# st.write("")


with st.form(key='my_form'):
    uploaded_file = st.file_uploader(
        label='Upload invoice image (.jpg or .png format)')
    submit_button = st.form_submit_button(label='Submit')

st.subheader(" Choose from the demo images for quick view")
with st.form(key='my_form_2'):
    image_demo1 = Image.open(
        "./images/demo/inv-1.jpg")
    image_demo2 = Image.open(
        "./images/demo/inv-2.png")
    image_demo3 = Image.open(
        "./images/demo/inv-3.png")
    col1, col2, col3 = st.columns(3)
    submit_button_2 = col1.form_submit_button(label='Use Demo 1')
    submit_button_3 = col2.form_submit_button(label='Use Demo 2')
    submit_button_4 = col3.form_submit_button(label='Use Demo 3')

if submit_button:
    image = Image.open(uploaded_file)

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
    image = image.convert('RGB')
    image.save("input.jpg")
    with open("input.jpg", "rb") as f:
        img_byte = f.read()

    coll1, coll2 = st.columns(2)
    coll1.header("Invoice")
    coll1.image(image)

    with st.spinner('Model Running...'):
        url = "https://q3d0rlossg.execute-api.us-east-1.amazonaws.com/default/invoiceContainer"

        payload = img_byte
        headers = {
            'x-api-key': '4KQfn4znnK8caRlTklZrFcUNNJvB6oFuWFKF4dh0',
            'Content-Type': 'text/plain'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

    ans = response.json()
    coll2.header("Result")
    if("bbox" in ans):
        coll2.image(save_labelled(ans))
    st.subheader("JSON Response")
    st.write(ans)
