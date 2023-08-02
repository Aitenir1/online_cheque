import pdfkit
from sh import lp

from django.template.loader import render_to_string

from api.models import Order

def print_receipt(order: Order) -> None:
    """
    Function that queues the order receipt to the printer

    :param order: The Order intance on which receipt is created
    """
    generate_html(order)

    html2pdf('media/order_to_print.html', 'media/ready_to_print_order.pdf')

    # lp('media/ready_to_print_order.pdf')


def generate_html(order: Order) -> None:
    """
    Function that creates an HTML template for receipt based on Order

    :param order: The Order instance on which HTML template is generated
    """

    rendered_html = render_to_string('index.html', context={'order': order})

    with open('media/order_to_print.html', 'w+') as f:
        f.write(rendered_html)


def html2pdf(input_file: str, output_file: str) -> None:
    """
    Function that converts HTML file to PDF receipt format

    :param input_file: HTML file path (media/...)
    :param output_file: The path where new PDF receipt is saved
    """

    try:
        options = {
            'page-size': 'A7',
            # 'page-height': '1000mm',
            # 'page-height': '200mm',
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            'encoding': 'UTF-8',
            'no-outline': None,

            "enable-local-file-access": ""
        }

        pdfkit.from_file(input_file, output_file, options=options)
        print('Conversion successful. PDF created:', output_file)

    except Exception as e:
        print('Conversion failed:', e)
